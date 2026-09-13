"""
Django ORM implementations of AI Core repository ports.
"""
import io
from typing import Optional, Dict, Any, List, Tuple
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from ai_core.models import AiMemory, AiUsageLog, AiProviderConfig
from ai_core.domain.entities import AiMemoryEntity, AiUsageLogEntity, AiProviderConfigEntity
from ai_core.application.ports.outbound.ai_memory_repository_port import AiMemoryRepositoryPort
from ai_core.application.ports.outbound.ai_usage_log_port import AiUsageLogRepositoryPort
from ai_core.application.ports.outbound.ai_provider_config_port import AiProviderConfigRepositoryPort


class DjangoAiMemoryRepository(AiMemoryRepositoryPort):
    def get_by_hash(self, request_type: str, prompt_hash: str) -> Optional[AiMemoryEntity]:
        try:
            m = AiMemory.objects.filter(
                request_type=request_type,
                prompt_hash=prompt_hash
            ).order_by('-user_rating', '-created_at').first()

            if m:
                m.mark_as_used()
                return self._to_entity(m)
            return None
        except Exception:
            return None

    def save_text_response(
        self,
        request_type: str,
        prompt_hash: str,
        prompt_text: str,
        prompt_options: Dict[str, Any],
        generated_text: str,
        provider: str,
        model: str,
        tokens_used: int,
        cost_estimate: float,
        latency_ms: int
    ) -> AiMemoryEntity:
        memory, created = AiMemory.objects.get_or_create(
            request_type=request_type,
            prompt_hash=prompt_hash,
            defaults={
                'prompt_text': prompt_text,
                'prompt_options': prompt_options,
                'generated_text': generated_text,
                'provider': provider,
                'model': model,
                'tokens_used': tokens_used,
                'cost_estimate': cost_estimate,
                'latency_ms': latency_ms,
            }
        )
        if not created:
            memory.generated_text = generated_text
            memory.provider = provider
            memory.model = model
            memory.tokens_used = tokens_used
            memory.cost_estimate = cost_estimate
            memory.latency_ms = latency_ms
            memory.save()

        return self._to_entity(memory)

    def save_audio_response(
        self,
        text_hash: str,
        text: str,
        audio_bytes: bytes,
        provider: str,
        language: str,
        voice_id: str,
        cost_estimate: float,
        latency_ms: int
    ) -> AiMemoryEntity:
        audio_file = InMemoryUploadedFile(
            io.BytesIO(audio_bytes),
            None,
            f"{text_hash[:12]}.mp3",
            'audio/mpeg',
            len(audio_bytes),
            None
        )
        memory, created = AiMemory.objects.get_or_create(
            request_type='tts_audio',
            prompt_hash=text_hash,
            defaults={
                'prompt_text': text,
                'prompt_options': {'language': language, 'voice_id': voice_id},
                'generated_audio_file': audio_file,
                'audio_metadata': {
                    'language': language,
                    'voice_id': voice_id,
                    'format': 'mp3'
                },
                'provider': provider,
                'model': voice_id or 'default',
                'cost_estimate': cost_estimate,
                'latency_ms': latency_ms,
            }
        )
        if not created and not memory.generated_audio_file:
            memory.generated_audio_file = audio_file
            memory.save()

        return self._to_entity(memory)

    def get_audio_by_hash(self, text_hash: str) -> Optional[Tuple[bytes, AiMemoryEntity]]:
        try:
            m = AiMemory.objects.filter(
                request_type='tts_audio',
                prompt_hash=text_hash,
                generated_audio_file__isnull=False
            ).first()

            if m and m.generated_audio_file:
                m.mark_as_used()
                with m.generated_audio_file.open('rb') as f:
                    audio_bytes = f.read()
                return audio_bytes, self._to_entity(m)
            return None
        except Exception:
            return None

    @staticmethod
    def _to_entity(m: AiMemory) -> AiMemoryEntity:
        return AiMemoryEntity(
            id=m.id,
            request_type=m.request_type,
            prompt_hash=m.prompt_hash,
            prompt_text=m.prompt_text,
            prompt_options=m.prompt_options or {},
            generated_text=m.generated_text,
            audio_file_path=m.generated_audio_file.url if m.generated_audio_file else None,
            audio_metadata=m.audio_metadata or {},
            provider=m.provider,
            model=m.model,
            tokens_used=m.tokens_used,
            cost_estimate=float(m.cost_estimate) if m.cost_estimate is not None else None,
            latency_ms=m.latency_ms,
            is_verified_good=m.is_verified_good,
            user_rating=m.user_rating,
            usage_count=m.usage_count,
            use_for_training=m.use_for_training
        )


class DjangoAiUsageLogRepository(AiUsageLogRepositoryPort):
    def log_usage(self, entry: AiUsageLogEntity) -> None:
        try:
            AiUsageLog.objects.create(
                request_type=entry.request_type,
                endpoint=entry.endpoint,
                user_id=entry.user_id,
                provider=entry.provider,
                model=entry.model,
                tokens_used=entry.tokens_used,
                cost_estimate=entry.cost_estimate,
                latency_ms=entry.latency_ms,
                cache_hit=entry.cache_hit,
                memory_item_id=entry.memory_id,
                selection_mode=entry.selection_mode,
                success=entry.success,
                error_message=entry.error_message
            )
        except Exception:
            pass

    def get_cost_summary(self, days: int = 30) -> Dict[str, Any]:
        cutoff = timezone.now() - timedelta(days=days)
        logs = AiUsageLog.objects.filter(timestamp__gte=cutoff)
        summary = logs.aggregate(
            total_requests=Count('id'),
            total_cost=Sum('cost_estimate'),
            total_tokens=Sum('tokens_used'),
            cache_hits=Count('id', filter=models.Q(cache_hit=True)),
            avg_latency=Avg('latency_ms')
        )
        by_provider = list(
            logs.values('provider', 'model').annotate(
                requests=Count('id'),
                cost=Sum('cost_estimate'),
                tokens=Sum('tokens_used')
            ).order_by('-cost')
        )
        total_req = summary.get('total_requests') or 0
        cache_hits = summary.get('cache_hits') or 0
        hit_rate = (cache_hits / total_req * 100) if total_req > 0 else 0.0

        return {
            'summary': summary,
            'by_provider': by_provider,
            'cache_hit_rate': round(hit_rate, 2)
        }


class DjangoAiProviderConfigRepository(AiProviderConfigPort := AiProviderConfigRepositoryPort):
    def get_best_model_for_tier(self, tier: str) -> Optional[Tuple[str, str]]:
        config = AiProviderConfig.objects.filter(
            tier=tier,
            is_active=True
        ).order_by('cost_per_million_tokens', '-quality_score').first()

        if config:
            return config.provider, config.model_name
        return None

    def list_active_configs(self) -> List[AiProviderConfigEntity]:
        qs = AiProviderConfig.objects.filter(is_active=True)
        return [
            AiProviderConfigEntity(
                id=m.id,
                provider=m.provider,
                model_name=m.model_name,
                tier=m.tier,
                cost_per_million_tokens=float(m.cost_per_million_tokens) if m.cost_per_million_tokens is not None else None,
                cost_per_request=float(m.cost_per_request) if m.cost_per_request is not None else None,
                avg_latency_ms=m.avg_latency_ms,
                quality_score=m.quality_score,
                is_active=m.is_active,
                is_default=m.is_default,
                max_tokens=m.max_tokens,
                capabilities=m.capabilities or {}
            )
            for m in qs
        ]
