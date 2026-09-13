# Step 14: Feed, Social & Gamification Refactor

## 1. Objective & Scope
Refactor the `feed`, `social`, `mentions`, and `gamification` apps into Hexagonal Architecture, decoupling activity stream aggregation, mention parsing, social interactions, and gamification badge award rules from Django views and ORM queries.

### What is being cleaned / refactored:
- Extract pure domain models: `FeedItemEntity`, `ActivityEvent`, `CommentEntity`, `MentionEntity`, `BadgeEntity`, `StreakPolicy`.
- Extract use cases:
  - `GetPersonalizedFeedUseCase` (aggregates social activity + recommended content)
  - `PostCommentWithMentionsUseCase` (parses `@username` mentions $\rightarrow$ creates notification events)
  - `UpdateUserStreakAndAwardBadgesUseCase` (pure gamification rules for daily activity)
  - `GetLeaderboardUseCase`
- Define outbound ports:
  - `FeedRepositoryPort`
  - `SocialRepositoryPort`
  - `GamificationRepositoryPort`
  - `NotificationPublisherPort`
- Implement persistence adapters and clean up views.

### What MUST NOT break:
- `/api/feed/`, `/api/social/`, `/api/mentions/`, `/api/gamification/` endpoints.
- Activity feed ordering and user mentions resolution.

---

## 2. Pre-flight Checks
- Test feed and social comment endpoints.

---

## 3. Planned Changes
- **[NEW]** `feed/domain/entities.py` (FeedItem, ActivityFeed)
- **[NEW]** `social/domain/entities.py` (Comment, Reaction)
- **[NEW]** `gamification/domain/policies.py` (BadgeAwardPolicy, StreakPolicy)
- **[NEW]** `feed/application/use_cases/get_personalized_feed.py`
- **[NEW]** `social/application/use_cases/post_comment.py`
- **[NEW]** `gamification/application/use_cases/award_badges.py`
- **[NEW]** `feed/adapters/outbound/persistence/django_feed_repository.py`
- **[NEW]** `social/adapters/outbound/persistence/django_social_repository.py`
- **[MODIFY]** `feed/views.py`, `social/views.py`, `mentions/views.py`

---

## 4. Execution Details
1. Implement pure streak & badge calculation policies in domain.
2. Implement repository adapters for feed and social models.
3. Wire use cases into composition roots.
4. Refactor DRF viewsets into thin HTTP controllers.
5. Verify zero regression.

---

## 5. Verification & Tests
- Unit tests for streak calculations and mention parsing:
  ```bash
  pytest feed/tests/ social/tests/ gamification/tests/
  ```

---

## 6. Rollback / Backoff Plan
- Reversible via legacy view fallbacks.
