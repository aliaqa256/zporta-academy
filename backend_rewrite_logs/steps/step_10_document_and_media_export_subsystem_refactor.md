# Step 10: Document & Media Export Subsystem Refactor

## 1. Objective & Scope
Refactor the document generation and media management subsystem (`lessons/pdf_utils.py`, `export_utils.py`, `media_manager`, `assets`, `user_media`) into a unified Hexagonal export module with strict abstraction over WeasyPrint, python-docx, and storage backends.

### What is being cleaned / refactored:
- Extract pure domain models: `DocumentTemplateEntity`, `ExportRequest`, `ExportResult`, `MediaAssetEntity`.
- Extract use cases:
  - `ExportLessonToPdfUseCase` (fetches lesson $\rightarrow$ formats HTML template $\rightarrow$ renders PDF via WeasyPrint $\rightarrow$ stores file)
  - `ExportLessonToWordUseCase` (renders DOCX via python-docx)
  - `ManageMediaAssetUseCase` (upload, validate MIME type, generate thumbnails, store)
- Define outbound ports:
  - `DocumentRendererPort` (PDF / Word)
  - `MediaStoragePort` (Local `MEDIA_ROOT` fallback / Cloud storage)
  - `AssetRepositoryPort`
- Implement outbound adapters:
  - `WeasyPrintPdfRendererAdapter` (handles typography, CJK fonts, CSS stylesheets)
  - `PythonDocxRendererAdapter`
  - `DjangoStorageAdapter`
- Clean up `lessons/pdf_utils.py` and `lessons/export_utils.py`.

### What MUST NOT break:
- `/api/lessons/{slug}/export/pdf/`, `/api/lessons/{slug}/export/docx/` endpoints.
- PDF visual layout, CJK font rendering (Noto Sans CJK JP), page numbering, and headers/footers.
- `/api/assets/` and `/api/user_media/` endpoints.

---

## 2. Pre-flight Checks
- Verify WeasyPrint system packages:
  ```bash
  python -c "import weasyprint; print('WeasyPrint OK')"
  ```

---

## 3. Planned Changes
- **[NEW]** `core/media_export/domain/entities.py` (ExportJob, MediaFile)
- **[NEW]** `core/media_export/domain/exceptions.py` (RenderingError, UnsupportedFormatError)
- **[NEW]** `core/media_export/application/ports/outbound/document_renderer_port.py`
- **[NEW]** `core/media_export/application/ports/outbound/storage_port.py`
- **[NEW]** `core/media_export/application/use_cases/export_lesson_document.py`
- **[NEW]** `core/media_export/adapters/outbound/weasyprint_adapter.py`
- **[NEW]** `core/media_export/adapters/outbound/docx_adapter.py`
- **[NEW]** `core/media_export/adapters/outbound/local_storage_adapter.py`
- **[NEW]** `core/media_export/composition/container.py`
- **[MODIFY]** `lessons/views.py` (Delegate export actions to use case)

---

## 4. Execution Details
1. Implement pure `DocumentRendererPort` contract.
2. Implement WeasyPrint adapter with error handling and fallback fonts.
3. Wire document export use case to lesson view endpoint.
4. Verify PDF visual fidelity against legacy generated PDFs.

---

## 5. Verification & Tests
- Unit and integration tests for PDF/DOCX generation:
  ```bash
  pytest core/media_export/tests/
  ```
- Generate sample lesson PDF and verify valid binary stream.

---

## 6. Rollback / Backoff Plan
- Reversible by routing export endpoints back to `lessons/pdf_utils.py` legacy helpers.
