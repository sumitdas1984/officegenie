# Requirements Document

## Introduction

OfficeGenie is an AI-powered employee support triage system. Employees submit natural language support requests via a web form. The system classifies each request into a department category (e.g., IT, HR, Payroll, Admin), extracts structured entities from the message, generates a personalised acknowledgment response, routes the request to the appropriate team, and logs all activity for analytics. The LLM backbone (OpenAI GPT or Anthropic Claude) drives classification and entity extraction via prompt templates.

---

## Glossary

- **OfficeGenie**: The overall AI-powered employee support triage system described in this document.
- **Request**: A natural language support message submitted by an employee through the web form.
- **Classifier**: The OfficeGenie subsystem responsible for determining the department category and subcategory of a Request.
- **Extractor**: The OfficeGenie subsystem responsible for identifying and returning structured entities from a Request.
- **Router**: The OfficeGenie subsystem responsible for forwarding a classified and extracted Request to the correct department queue or automation endpoint.
- **Responder**: The OfficeGenie subsystem responsible for generating and delivering an automated acknowledgment message to the employee.
- **Logger**: The OfficeGenie subsystem responsible for persisting Request records and processing results for analytics.
- **LLM_Client**: The OfficeGenie subsystem that communicates with the external LLM API (OpenAI or Anthropic Claude).
- **Category**: A top-level department label assigned to a Request (e.g., IT, HR, Payroll, Admin, Facilities).
- **Subcategory**: A second-level label that refines the Category (e.g., "Payslip Access" within "Payroll").
- **Confidence_Score**: A numeric value between 0.0 and 1.0 representing the Classifier's certainty about an assigned Category.
- **Structured_Entities**: A key-value map of domain-specific fields extracted from a Request (e.g., `month`, `error_message`, `system_name`, `urgency`).
- **Acknowledgment**: An auto-generated, human-readable reply sent to the employee confirming receipt and next steps.
- **Request_Record**: A persisted JSON or SQLite row capturing the original Request text, Structured_Entities, Category, Subcategory, Confidence_Score, Acknowledgment, routing destination, and timestamp.
- **Dashboard**: The React frontend view that displays the submission form and Recent Activity list.

---

## Requirements

### Requirement 1: Request Submission

**User Story:** As an employee, I want to submit a support request in plain language via a web form, so that I can get help without knowing which department to contact.

#### Acceptance Criteria

1. THE Dashboard SHALL render a text area that accepts free-text input of between 10 and 2000 characters.
2. THE Dashboard SHALL render a "Submit to Genie" button that is enabled only when the text area contains at least 10 characters.
3. WHEN the employee clicks "Submit to Genie", THE Dashboard SHALL send the Request text to the OfficeGenie backend API within 500ms of the click event.
4. WHILE a Request is being processed, THE Dashboard SHALL display a loading indicator and disable the "Submit to Genie" button.
5. IF the text area contains fewer than 10 characters when submission is attempted, THEN THE Dashboard SHALL display an inline validation message stating the minimum character requirement.
6. IF the text area contains more than 2000 characters, THEN THE Dashboard SHALL prevent submission and display an inline validation message stating the maximum character limit.

---

### Requirement 2: Intent Classification

**User Story:** As a support operations manager, I want every incoming request automatically classified into a department category, so that requests reach the right team without manual triage.

#### Acceptance Criteria

1. WHEN a Request is received by the backend, THE Classifier SHALL assign exactly one Category from the set {IT, HR, Payroll, Admin, Facilities, Other}.
2. WHEN a Request is received by the backend, THE Classifier SHALL assign exactly one Subcategory that refines the assigned Category.
3. WHEN a Request is received by the backend, THE Classifier SHALL produce a Confidence_Score between 0.0 and 1.0 for the assigned Category.
4. WHEN the Classifier produces a Confidence_Score below 0.5, THE Classifier SHALL assign the Category "Other" and include a flag indicating low-confidence classification.
5. THE Classifier SHALL complete classification within 3000ms of receiving the Request, excluding network latency to the LLM API.
6. IF the LLM_Client returns an error or times out, THEN THE Classifier SHALL assign Category "Other", Confidence_Score 0.0, and propagate an error status in the response.

---

### Requirement 3: Entity Extraction

**User Story:** As a support agent, I want structured data extracted from each request, so that I can act on the issue immediately without re-reading the full message.

#### Acceptance Criteria

1. WHEN a Request is classified, THE Extractor SHALL return a Structured_Entities map containing all domain-relevant fields present in the Request text.
2. THE Extractor SHALL recognise and extract the following entity types when present: `system_name`, `error_message`, `urgency`, `date_reference`, `employee_id`, `asset_id`.
3. WHEN an entity type is not present in the Request text, THE Extractor SHALL omit that key from the Structured_Entities map rather than returning a null value.
4. THE Extractor SHALL return Structured_Entities as a valid JSON object.
5. IF the LLM_Client returns malformed JSON for entity extraction, THEN THE Extractor SHALL return an empty Structured_Entities map and log the raw LLM response for debugging.

---

### Requirement 4: Automated Acknowledgment Generation

**User Story:** As an employee, I want to receive an instant, personalised acknowledgment after submitting a request, so that I know my issue has been received and understand the next steps.

#### Acceptance Criteria

1. WHEN a Request is classified and entities are extracted, THE Responder SHALL generate an Acknowledgment that references the assigned Category and at least one extracted entity when available.
2. THE Responder SHALL generate an Acknowledgment of between 20 and 300 characters.
3. WHEN the Acknowledgment is generated, THE Dashboard SHALL display it to the employee within the same response payload as the classification result.
4. THE Responder SHALL generate the Acknowledgment in the same natural language as the submitted Request.
5. IF entity extraction returns an empty Structured_Entities map, THEN THE Responder SHALL generate a generic Acknowledgment that references only the assigned Category.

---

### Requirement 5: Request Routing

**User Story:** As a department team lead, I want classified requests automatically routed to my team's queue, so that my team receives only relevant tickets without manual filtering.

#### Acceptance Criteria

1. WHEN a Request is classified with a Confidence_Score of 0.5 or above, THE Router SHALL forward the Request_Record to the routing destination registered for the assigned Category.
2. WHEN a Request is classified with Category "Other" or a Confidence_Score below 0.5, THE Router SHALL forward the Request_Record to a designated human-review queue.
3. THE Router SHALL complete routing within 1000ms of receiving the classification result.
4. IF the routing destination is unavailable, THEN THE Router SHALL retry the delivery up to 3 times with a 500ms interval between attempts.
5. IF all retry attempts fail, THEN THE Router SHALL mark the Request_Record with a routing status of "failed" and log the failure with the destination identifier and timestamp.

---

### Requirement 6: Request Logging and Persistence

**User Story:** As a data analyst, I want all support requests and their processing results stored, so that I can analyse trends and measure system performance over time.

#### Acceptance Criteria

1. WHEN a Request completes processing, THE Logger SHALL persist a Request_Record containing: original request text, Category, Subcategory, Confidence_Score, Structured_Entities, Acknowledgment text, routing destination, routing status, and UTC timestamp.
2. THE Logger SHALL persist each Request_Record within 500ms of processing completion.
3. THE Logger SHALL store Request_Records in a SQLite database using a schema that supports querying by Category, timestamp range, and routing status.
4. THE Logger SHALL assign each Request_Record a unique identifier upon creation.
5. IF a write operation to the SQLite database fails, THEN THE Logger SHALL write the Request_Record to a local JSON fallback file and log the database error.

---

### Requirement 7: Recent Activity Display

**User Story:** As an employee, I want to see my recent support requests and their statuses on the dashboard, so that I can track the progress of my submissions.

#### Acceptance Criteria

1. THE Dashboard SHALL display a "Recent Activity" list showing the 10 most recent Request_Records for the current session.
2. WHEN the Recent Activity list is rendered, THE Dashboard SHALL display for each entry: a truncated preview of the request text (max 80 characters), the assigned Category, the Confidence_Score, and the UTC timestamp.
3. WHEN a new Request is successfully submitted, THE Dashboard SHALL prepend the new Request_Record to the Recent Activity list without requiring a full page reload.
4. IF no Request_Records exist for the current session, THEN THE Dashboard SHALL display a placeholder message indicating no recent activity.

---

### Requirement 8: LLM Integration and Prompt Management

**User Story:** As a developer, I want the LLM interactions managed through versioned prompt templates, so that I can update classification and extraction behaviour without changing application code.

#### Acceptance Criteria

1. THE LLM_Client SHALL support configuration of either OpenAI GPT or Anthropic Claude as the active LLM provider via an environment variable.
2. THE LLM_Client SHALL load prompt templates from external template files rather than hardcoded strings.
3. WHEN the active LLM provider is changed via environment variable, THE LLM_Client SHALL use the corresponding API credentials and endpoint without requiring a code change.
4. THE LLM_Client SHALL log the model name, prompt token count, completion token count, and response latency in milliseconds for every API call.
5. IF the LLM API returns a rate-limit error, THEN THE LLM_Client SHALL wait 1000ms and retry the request once before returning an error status.
6. IF the LLM API returns a response that does not conform to the expected JSON schema, THEN THE LLM_Client SHALL log the raw response and return a structured error to the calling subsystem.

---

### Requirement 9: API Contract

**User Story:** As a frontend developer, I want a well-defined REST API, so that the React frontend can integrate with the backend reliably.

#### Acceptance Criteria

1. THE OfficeGenie backend SHALL expose a `POST /api/requests` endpoint that accepts a JSON body containing a `text` field and returns a JSON response containing `request_id`, `category`, `subcategory`, `confidence_score`, `structured_entities`, and `acknowledgment`.
2. THE OfficeGenie backend SHALL respond to `POST /api/requests` with HTTP 200 on success, HTTP 422 on validation failure, and HTTP 500 on internal error.
3. THE OfficeGenie backend SHALL expose a `GET /api/requests` endpoint that returns a JSON array of the 10 most recent Request_Records ordered by timestamp descending.
4. WHEN a request to `POST /api/requests` contains a `text` field shorter than 10 characters or longer than 2000 characters, THE OfficeGenie backend SHALL return HTTP 422 with a JSON error body describing the violation.
5. THE OfficeGenie backend SHALL include a `Content-Type: application/json` header in all API responses.
