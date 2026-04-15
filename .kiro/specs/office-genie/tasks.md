# Implementation Plan: OfficeGenie

## Overview

Implement OfficeGenie incrementally: project scaffolding first, then each backend subsystem (LLM_Client → Classifier → Extractor → Responder → Router → Logger → API), then the React frontend, wiring everything together at the end.

## Tasks

- [ ] 1. Scaffold project structure and shared types
  - Create `backend/` with `app/`, `prompts/`, and `tests/` sub-directories
  - Create `frontend/` with a Vite + React + TypeScript scaffold
  - Define `RequestRecord` and `ClassificationResult` Pydantic models in `backend/app/models.py`
  - Add backend dependencies to `pyproject.toml`: `fastapi`, `uvicorn`, `openai`, `anthropic`, `hypothesis`, `pytest`, `pytest-asyncio`, `httpx`
  - Add `frontend/package.json` with `vitest`, `@testing-library/react`, `@testing-library/user-event`, `fast-check`
  - Create the three prompt template stubs: `prompts/classification.txt`, `prompts/extraction.txt`, `prompts/acknowledgment.txt`
  - _Requirements: 8.2, 9.1_

- [ ] 2. Implement LLM_Client
  - [ ] 2.1 Implement `backend/app/llm_client.py`
    - Select provider from `LLM_PROVIDER` env var; load API credentials from env
    - Load and cache prompt templates from `prompts/` at startup
    - Log model name, prompt tokens, completion tokens, and latency for every call
    - On rate-limit (429): wait 1000ms and retry exactly once, then return structured error
    - On schema mismatch: log raw response and return structured error
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

  - [ ]* 2.2 Write property test for LLM provider selection invariant
    - **Property 12: LLM provider selection invariant**
    - **Validates: Requirements 8.3, 8.4**
    - Tag: `# Feature: office-genie, Property 12: LLM provider selection invariant`

  - [ ]* 2.3 Write property test for LLM rate-limit retry
    - **Property 13: LLM rate-limit retry**
    - **Validates: Requirements 8.5**
    - Tag: `# Feature: office-genie, Property 13: LLM rate-limit retry`

  - [ ]* 2.4 Write property test for LLM schema error structured response
    - **Property 14: LLM schema error returns structured error**
    - **Validates: Requirements 8.6**
    - Tag: `# Feature: office-genie, Property 14: LLM schema error returns structured error`

- [ ] 3. Implement Classifier
  - [ ] 3.1 Implement `backend/app/classifier.py` with `classify(text, llm_client) -> ClassificationResult`
    - Call LLM_Client with the classification prompt template
    - Parse JSON response into `ClassificationResult`
    - If `confidence_score < 0.5`, override `category` to `"Other"` and set `low_confidence=True`
    - On LLM error: return `ClassificationResult(category="Other", subcategory="Unknown", confidence_score=0.0, error=True)`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_

  - [ ]* 3.2 Write property test for classification output invariant
    - **Property 2: Classification output invariant**
    - **Validates: Requirements 2.1, 2.2, 2.3**
    - Tag: `# Feature: office-genie, Property 2: Classification output invariant`

  - [ ]* 3.3 Write property test for low-confidence override
    - **Property 3: Low-confidence override**
    - **Validates: Requirements 2.4**
    - Tag: `# Feature: office-genie, Property 3: Low-confidence override`

  - [ ]* 3.4 Write property test for LLM error fallback
    - **Property 4: LLM error fallback produces safe classification**
    - **Validates: Requirements 2.6**
    - Tag: `# Feature: office-genie, Property 4: LLM error fallback produces safe classification`

  - [ ]* 3.5 Write example test for classifier with known inputs
    - Test `test_classifier_example_known_inputs` covering Req 2.1–2.3

- [ ] 4. Implement Extractor
  - [ ] 4.1 Implement `backend/app/extractor.py` with `extract(text, llm_client) -> dict[str, str]`
    - Call LLM_Client with the extraction prompt template
    - Parse JSON response; omit keys with null/missing values
    - On malformed JSON: return `{}` and log the raw response
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ]* 4.2 Write property test for entities map never containing null values
    - **Property 5: Entities map never contains null values**
    - **Validates: Requirements 3.3, 3.4, 3.5**
    - Tag: `# Feature: office-genie, Property 5: Entities map never contains null values`

  - [ ]* 4.3 Write example test for extractor with known entity types
    - Test `test_extractor_known_entities` covering Req 3.1–3.2

- [ ] 5. Implement Responder
  - [ ] 5.1 Implement `backend/app/responder.py` with `generate_acknowledgment(category, entities, llm_client) -> str`
    - Call LLM_Client with the acknowledgment prompt template
    - Validate returned string is between 20 and 300 characters
    - Fall back to a generic template if entities are empty or length validation fails
    - _Requirements: 4.1, 4.2, 4.4, 4.5_

  - [ ]* 5.2 Write property test for acknowledgment content and length invariant
    - **Property 6: Acknowledgment content and length invariant**
    - **Validates: Requirements 4.1, 4.2, 4.5**
    - Tag: `# Feature: office-genie, Property 6: Acknowledgment content and length invariant`

- [ ] 6. Checkpoint — Ensure all backend subsystem tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement Router
  - [ ] 7.1 Implement `backend/app/router.py` with `route(record: RequestRecord) -> RoutingResult`
    - Load routing destination config map (category → queue identifier)
    - Route to human-review queue if `confidence_score < 0.5` or `category == "Other"`
    - Retry delivery up to 3 times with 500ms delay on destination failure
    - On total failure: set `routing_status = "failed"` and log the error
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]* 7.2 Write property test for routing destination correctness
    - **Property 7: Routing destination correctness**
    - **Validates: Requirements 5.1, 5.2**
    - Tag: `# Feature: office-genie, Property 7: Routing destination correctness`

  - [ ]* 7.3 Write property test for router retry count and failure status
    - **Property 8: Router retry and failure status**
    - **Validates: Requirements 5.4, 5.5**
    - Tag: `# Feature: office-genie, Property 8: Router retry and failure status`

- [ ] 8. Implement Logger
  - [ ] 8.1 Implement `backend/app/logger.py` with `persist(record: RequestRecord) -> str`
    - Create the SQLite schema (`request_records` table + indexes) on first run
    - Assign a UUID as `request_id` and write the record to SQLite
    - On SQLite write failure: write to a local JSON fallback file and log the DB error
    - Implement `get_recent(limit=10) -> list[RequestRecord]` ordered by timestamp descending
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 8.2 Write property test for persisted record completeness and uniqueness
    - **Property 9: Persisted record completeness and uniqueness**
    - **Validates: Requirements 6.1, 6.4**
    - Tag: `# Feature: office-genie, Property 9: Persisted record completeness and uniqueness`

  - [ ]* 8.3 Write property test for DB failure fallback persistence
    - **Property 10: DB failure triggers fallback persistence**
    - **Validates: Requirements 6.5**
    - Tag: `# Feature: office-genie, Property 10: DB failure triggers fallback persistence`

- [ ] 9. Implement FastAPI RequestsRouter and wire backend subsystems
  - [ ] 9.1 Implement `backend/app/main.py` with FastAPI app and `POST /api/requests` endpoint
    - Validate request body with Pydantic (text 10–2000 chars); return HTTP 422 on failure
    - Orchestrate: Classifier → Extractor → Responder → Router → Logger
    - Return full response payload; return HTTP 500 on unhandled errors
    - Include `Content-Type: application/json` header on all responses
    - _Requirements: 9.1, 9.2, 9.4, 9.5_

  - [ ] 9.2 Implement `GET /api/requests` endpoint
    - Delegate to `Logger.get_recent(10)` and return the list ordered by timestamp descending
    - _Requirements: 9.3_

  - [ ]* 9.3 Write property test for HTTP status code invariant
    - **Property 15: HTTP status code invariant**
    - **Validates: Requirements 9.2, 9.4, 9.5**
    - Tag: `# Feature: office-genie, Property 15: HTTP status code invariant`

  - [ ]* 9.4 Write property test for GET /api/requests ordering and limit
    - **Property 16: GET /api/requests ordering and limit**
    - **Validates: Requirements 9.3**
    - Tag: `# Feature: office-genie, Property 16: GET /api/requests ordering and limit`

  - [ ]* 9.5 Write example tests for API contract
    - `test_api_contract_post_success` (Req 9.1) and `test_api_contract_get_success` (Req 9.3)

- [ ] 10. Checkpoint — Ensure all backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement React frontend — ApiClient and SubmitForm
  - [ ] 11.1 Implement `frontend/src/api/client.ts`
    - `postRequest(text: string)` — POST to `/api/requests`, return typed response
    - `getRequests()` — GET `/api/requests`, return typed array
    - _Requirements: 9.1, 9.3_

  - [ ] 11.2 Implement `frontend/src/components/SubmitForm.tsx`
    - Text area accepting 10–2000 characters with inline validation messages
    - "Submit to Genie" button enabled only when text length is in [10, 2000]
    - Loading indicator and disabled button while request is in flight
    - On success: pass response record to parent callback
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [ ]* 11.3 Write property test for input validation gates submission
    - **Property 1: Input validation gates submission**
    - **Validates: Requirements 1.2, 1.5, 1.6**
    - Use `fast-check` with arbitrary string lengths; assert button state and validation message
    - Tag: `# Feature: office-genie, Property 1: Input validation gates submission`

  - [ ]* 11.4 Write example tests for SubmitForm
    - `test_submit_button_state` (Req 1.2), `test_loading_indicator` (Req 1.4)

- [ ] 12. Implement React frontend — RecentActivity and Dashboard wiring
  - [ ] 12.1 Implement `frontend/src/components/RecentActivity.tsx`
    - Render ordered list of up to 10 `RequestRecord` entries
    - Each entry shows: text preview (max 80 chars), category, confidence score, UTC timestamp
    - Display placeholder message when list is empty
    - _Requirements: 7.1, 7.2, 7.4_

  - [ ] 12.2 Implement `frontend/src/App.tsx` (Dashboard)
    - Fetch recent records on mount via `ApiClient.getRequests()`
    - On successful submission: prepend new record to activity list without full reload
    - Display acknowledgment from the response payload
    - _Requirements: 4.3, 7.1, 7.3_

  - [ ]* 12.3 Write property test for recent activity rendering completeness
    - **Property 11: Recent activity rendering completeness**
    - **Validates: Requirements 7.2**
    - Use `fast-check` to generate arbitrary arrays of `RequestRecord`; assert all fields rendered
    - Tag: `# Feature: office-genie, Property 11: Recent activity rendering completeness`

  - [ ]* 12.4 Write example tests for RecentActivity and Dashboard
    - `test_acknowledgment_displayed` (Req 4.3), `test_recent_activity_prepend` (Req 7.3), `test_empty_activity_placeholder` (Req 7.4)

- [ ] 13. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass (backend: `pytest`, frontend: `vitest --run`), ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Property tests use Hypothesis (backend) and fast-check (frontend); each must include the `# Feature: office-genie, Property N:` comment tag
- Checkpoints ensure incremental validation before moving to the next layer
