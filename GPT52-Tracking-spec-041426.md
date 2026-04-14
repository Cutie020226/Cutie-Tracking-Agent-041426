Comprehensive Updated Technical Specification — Agentic AI Regulatory & Dataset Intelligence System (“Regulatory Command Center WOW”)

## 1. Executive Summary

The **Regulatory Command Center WOW** is a **Streamlit application deployed on Hugging Face Spaces** that unifies:

1) **Multi-dataset ingestion, preview, filtering, and analysis** (default `dataset.json` + user-provided datasets),  
2) **Document Operating Room** for PDF/text ingestion with trimming + OCR,  
3) **Agent Studio / Agentic Pipeline** powered by `agents.yaml` across multiple LLM providers (OpenAI, Gemini, Anthropic, Grok/xAI),  
4) A premium **WOW UI** (Light/Dark, English/Traditional Chinese, and 20 painter-inspired visual styles selectable via **Jackslot**),  
5) **AI NoteKeeper** for transforming unstructured notes into organized markdown with colored keywords, plus additional “AI Magics”,  
6) A dedicated **Dataset Report & Infograph Generator** that produces **6 WOW interactive infographs** (including a supply-chain network graph) and a **comprehensive 3000–4000 word markdown report** with **5 tables** and **20 extracted entities**, and  
7) An automated **skill.md generator** (using the “skill creator skill” methodology) to enable consistent future report + infograph generation.

This specification **keeps all original features** (global search, dashboards, document workflow, OCR modes, agent chaining, factory/batch PDFs, agents.yaml editing, dataset studio, export/download, safe key handling), and **adds all requested enhancements**: a new WOW UI system, status indicators/live logs/dashboard, session-based API key entry, model selection + prompt editing for *all* LLM features, dataset.json-driven dataset defaults, dataset upload/paste/preview and filtering, interactive infograph suite, bilingual reporting, report/table/entity generation, and skill.md creation with additional WOW AI features.

---

## 2. Goals, Non-Goals, and Design Principles

### 2.1 Goals
- Deliver a **premium “WOW” command-center UI** with theme, language, and painter-style personalization.
- Provide **secure, user-friendly API key handling**: environment-first; session input only when missing; never display env keys.
- Enable **agentic workflows that are user-controlled**: choose model/provider, edit prompts, run agents **one-by-one**, edit each agent output and pass it as input to the next agent.
- Support **dataset-driven intelligence**:
  - Load **`dataset.json` as default** at startup.
  - Allow user to choose default datasets, limit number of datasets, or provide new datasets via paste/upload.
  - Provide dataset preview controls (default 20 records; user-configurable).
  - Generate 6 interactive infographs and a long-form bilingual report.
- Provide **AI NoteKeeper** for note transformation into structured markdown with **coral-colored keywords**, editing views, and a suite of AI Magics.
- Maintain compatibility with **Hugging Face Spaces + Streamlit + agents.yaml** and **Gemini/OpenAI/Anthropic/Grok APIs**.

### 2.2 Non-Goals
- Not a legal/regulatory authority; outputs require expert review.
- Not implementing multi-user authentication, persistent accounts, or real-time multi-user collaboration in v1.
- Not guaranteeing fully automated dataset schema inference for every arbitrary file; instead offering guided mapping/standardization with transparent diagnostics.

### 2.3 Design Principles
- **Controllability over autonomy**: agents execute stepwise with clear inputs/outputs, editable by users.
- **Transparency & traceability**: display run metadata, prompts, model choice, timestamps, and dataset filters used.
- **Safety by default**: avoid storing secrets; minimize accidental leakage; provide “redaction mode” for exports.
- **Performance-aware UI**: preview/visualize subsets by default; progressive rendering; caching where safe.

---

## 3. System Architecture Overview

### 3.1 High-Level Modules (Navigation)
1. **Home / Command Dashboard (WOW)**  
   Unified status indicators, live log, quick actions, and shortcuts to workflows.

2. **Dataset Studio (Enhanced)**  
   Default `dataset.json` loading, dataset selection, paste/upload (txt/csv/json), preview, filtering, and standardization.

3. **Infograph Lab (New)**  
   Generates **6 interactive infographs** from the currently active dataset selection + filters.

4. **Report Generator (New)**  
   Creates a **3000–4000 word** markdown report in **Traditional Chinese (default) / English**, includes **5 tables** and **20 extracted entities**, supports edit/download.

5. **Document Operating Room (Existing + Improved)**  
   PDF trim, text extraction, OCR (local/cloud), markdown reconstruction, then agent runs.

6. **Agent Studio (Existing + Improved)**  
   Manage `agents.yaml` upload/edit/validate/download; per-run prompt+model overrides.

7. **Factory / Batch PDFs (Existing)**  
   ZIP-based batch summarization into Master ToC; can feed ToC to agents.

8. **AI NoteKeeper (Enhanced)**  
   Paste/upload notes → structured markdown with coral keywords, editable views, “keep prompting,” and 6 AI Magics.

9. **Skill Builder (New)**  
   Generates **skill.md** from prior results using the skill creator methodology; adds 3 additional WOW AI features; supports edit/download.

### 3.2 Execution & State
- **Session state as authoritative runtime store**:
  - UI preferences (theme, language, painter style)
  - API keys (session-only if entered)
  - Dataset registry (default + user-provided + selection)
  - Active filters (supplier/license/model/customer/date/SN/lot)
  - Agent run history (inputs/outputs/metadata)
  - NoteKeeper content + transformations
  - Report drafts + skill.md drafts
  - Live log events

- **Provider abstraction** for LLM calls:
  - OpenAI API (models: `gpt-4o-mini`, `gpt-4.1-mini`)
  - Gemini API (models: `gemini-2.5-flash`, `gemini-3-flash-preview`)
  - Anthropic API (selectable “Anthropic models”, configurable list)
  - Grok/xAI API (models: `grok-4-fast-reasoning`, `grok-3-mini`)
  - Model availability is configurable at runtime (e.g., via settings panel).

---

## 4. WOW UI/UX Specification (New)

### 4.1 Theme System: Light/Dark + i18n + Painter Styles
**User controls (always visible in header):**
- Theme toggle: **Light / Dark**
- Language toggle: **Traditional Chinese (default) / English**
- Painter style selector:
  - Dropdown list of 20 styles
  - **Jackslot** mode: slot-machine interaction that “spins” and lands on a painter style
  - Optional “Auto-style” suggestion from context (document/dataset/note) using an LLM (user-approved before applying)

**20 painter-inspired UI styles** (visual inspiration only; implemented as palettes + typography + background textures):
1. Monet Mist (Impressionist pastel)
2. Van Gogh Starfield (bold contrast)
3. Picasso Cubist Grid (geometric)
4. Klimt Gilded Panel (gold accents)
5. Hokusai Wave (indigo + foam)
6. Rothko Fields (large color blocks)
7. Mondrian Primary (red/blue/yellow)
8. Dali Surreal (high clarity + shadows)
9. Matisse Cutouts (flat vibrant shapes)
10. Turner Atmosphere (foggy gradients)
11. Caravaggio Chiaroscuro (dramatic lighting)
12. Pollock Splash (dynamic speckles)
13. Frida Botanical (warm + floral)
14. Vermeer Pearl (soft light neutrals)
15. Ukiyo-e Paper (warm parchment)
16. Bauhaus Functional (minimalist)
17. Futurist Motion (diagonal energy)
18. Art Nouveau Linework (curves)
19. Ink Wash (monochrome)
20. Pop Art Punch (comic contrast)

**Coral keyword color** remains global: `#FF7F50` (user-adjustable in settings). Keywords in NoteKeeper and reports use coral highlight.

### 4.2 Layout: “Regulatory Command Center”
- **Top bar**: theme/language/style + API status + session health
- **Left navigation**: modules listed above
- **Main canvas**: cards, tabs, interactive charts
- **Right-side “Run Panel”** (contextual): prompts, model selection, agent controls, execution button

### 4.3 WOW Status Indicators (New)
A unified status strip shows:
- **API Provider readiness**: OpenAI/Gemini/Anthropic/Grok
  - State: Environment / Session / Missing
  - No key value is displayed
- **Dataset status**:
  - Active dataset count
  - Total records loaded
  - Current filter summary (e.g., SupplierID=B00079; Date=2025-10-28..2025-11-07)
- **Agent pipeline status**:
  - Current agent index (step-by-step)
  - Last run duration
  - Token/cost estimate if provider returns usage metadata
- **OCR status**:
  - Text-layer present / OCR required / OCR complete

### 4.4 Live Log (New)
A live event stream (in-session) captures:
- Dataset load/parse/validation events
- Filter changes
- Chart generation milestones
- Agent run start/end, model selection, and output length
- Errors with user-friendly messages + a technical “details” disclosure

Users can:
- Pause/resume log
- Download log as text/markdown (with secrets redacted)

### 4.5 Interactive Dashboard (New)
A “Command Dashboard” landing page includes:
- KPIs: record counts, unique suppliers/customers/models, date range coverage
- “Most active” entities
- Quick actions: “Generate Infographs”, “Generate Report”, “Open Agent Studio”, “Open NoteKeeper”
- Snapshot cards: last report draft, last dataset preview, last agent output

---

## 5. API Key Handling & Security (Enhanced)

### 5.1 Environment-first Behavior
- If a provider key exists in environment variables, the UI:
  - Shows **Status = Environment**
  - Does **not** show an input field for that provider
  - Does not reveal any part of the key

### 5.2 Session Key Entry (When Missing)
- If no env key exists, the UI provides an input field:
  - Stored in session state only
  - Never persisted to disk
  - Can be cleared by user (“Forget key”)

### 5.3 Redaction & Export Safety
- Exports (reports/logs/agent history) must:
  - Exclude API keys
  - Optionally redact sensitive identifiers (configurable: supplier/customer IDs, UDID, serial numbers)

---

## 6. Dataset Studio — Default dataset.json + User Datasets (Major Update)

### 6.1 Default Dataset Loading
- System loads **`dataset.json` at startup** as the default dataset pool.
- The shipped default dataset schema includes columns:

`SupplierID, Deliverdate, CustomerID, LicenseNo, Category, UDID, DeviceNAME, LotNO, SerNo, Model, Number`

The sample records provided (e.g., SupplierID B00079/B00051/B00209 etc.) are included as initial content.

### 6.2 Dataset Registry & Selection
Users can decide:
- Use default dataset(s) only
- Add additional datasets (uploaded/pasted)
- Select how many datasets to include in analysis (checkbox selection + “Select All/None”)
- Choose dataset priority (optional ordering) if combining outputs

Each dataset entry stores:
- Dataset name (auto-derived from file name or user label)
- Source type: default / upload / paste
- File type: txt/csv/json
- Row count, column list, inferred types
- Parsing warnings

### 6.3 Dataset Input Methods
1. **Paste**: user pastes txt/csv/json content into text area.
2. **Upload**: user uploads `.txt`, `.csv`, `.json`.
3. **Default**: load from `dataset.json`.

### 6.4 Preview Rules (User-Controlled)
- Default preview: **20 records**
- User can choose preview size (e.g., 10/20/50/100/500) with safeguards for performance.
- Preview includes:
  - Table view
  - Basic profiling: missingness, unique counts, min/max for date/number fields
  - Column mapping hints (if column names differ from canonical)

### 6.5 Standardization & Canonical Field Model
To support consistent filtering and infographs, the system standardizes to canonical fields:

- `supplier_id` (SupplierID)
- `deliver_date` (Deliverdate; parsed as date)
- `customer_id` (CustomerID)
- `license_no` (LicenseNo)
- `category` (Category)
- `udid` (UDID)
- `device_name` (DeviceNAME)
- `lot_no` (LotNO)
- `serial_no` (SerNo / SN)
- `model_no` (Model / Model No)
- `quantity` (Number)

The system keeps original columns accessible, but infographs and reports use canonical fields for reliability.

### 6.6 Filtering (Core for Infographs & Reports)
A unified filter panel supports:
- SupplierID (multi-select + search)
- LicenseNo (multi-select + search)
- Model No (multi-select + search)
- CustomerID (multi-select + search)
- Date zone (range selector on Deliverdate)
- SN/SerialNo (contains/exact)
- Lot No (contains/exact)

Filter summary is displayed in status indicators and embedded into report metadata for traceability.

---

## 7. Infograph Lab — 6 WOW Interactive Infographs (New)

### 7.1 General Requirements
- All 6 infographs are generated **from filtered active datasets**.
- Outputs are interactive (hover, zoom, isolate series) and responsive in Streamlit.
- Each infograph includes:
  - Title + “What this shows” caption
  - Filter snapshot
  - Export: image (where supported) and underlying data table (csv/json)
  - Language toggle: Traditional Chinese (default) / English labels

### 7.2 Infograph #1 — Supply Chain Network Graph (Required)
**Graph structure:**  
`SupplierID → LicenseNo → Model No → CustomerID`

- Node types: Supplier, License, Model, Customer
- Edge represents relationships in filtered records
- Node sizing: frequency (count of records or quantity sum)
- Color coding by node type; hover shows counts, date range, top related nodes
- User can:
  - Filter by any of the canonical fields
  - Choose aggregation: count vs quantity
  - Select layout style: force-directed / hierarchical

### 7.3 Infograph #2 — Time Series Flow (Deliveries Over Time)
- X-axis: Deliverdate (daily/weekly/monthly grouping)
- Y-axis: total quantity or record count
- Breakdown options:
  - by SupplierID
  - by CustomerID
  - by Model No
  - by Category
- Includes anomaly hints (spikes) with configurable sensitivity.

### 7.4 Infograph #3 — Heatmap: Supplier vs Customer Intensity
- Matrix heatmap where:
  - Rows: SupplierID
  - Columns: CustomerID
  - Cell value: count or quantity
- Supports clustering (optional) and sorting by totals.

### 7.5 Infograph #4 — License & Category Distribution
- Multi-panel:
  - LicenseNo frequency distribution
  - Category distribution
- Shows top-N with “Others” bucket; user controls N.

### 7.6 Infograph #5 — Model / Device Portfolio Treemap
- Treemap hierarchy:
  - Category → Model No → Device Name
- Size: quantity sum; color: supplier or license grouping (user choice).

### 7.7 Infograph #6 — Lot & Serial Traceability Explorer
- Interactive table + chart combo:
  - LotNo distribution
  - SerialNo presence rate (missing vs present)
  - Drill-down: select a lot to see associated models, customers, licenses, date ranges
- Includes data quality warnings (e.g., high missing serial numbers).

### 7.8 “WOW” Interactions
- “Spotlight mode”: click an entity (SupplierID/CustomerID/Model) to apply a temporary highlight overlay across all charts.
- “Explain this chart”: LLM-generated explanation of what patterns appear (model selectable, prompt editable).

---

## 8. Report Generator — 3000–4000 Word Markdown Report (New)

### 8.1 Language Output
- Output language selectable: **Traditional Chinese (default)** / English.
- All headings, table titles, and narrative follow chosen language.
- Entities retain original values (IDs, license numbers) unless redaction enabled.

### 8.2 Report Length and Structure Requirements
- Total length: **3000–4000 words** (target range, excluding tables if needed; must be clearly “comprehensive”).
- Must include:
  - **5 tables** embedded in markdown
  - **20 entities** explicitly listed (see §8.4)
  - A methods section describing dataset sources, filters, preview size, standardization, and limitations
  - Visual references section listing the 6 infographs produced and what each supports

### 8.3 Required Report Sections (Template)
1. Title + generated timestamp + language + applied filters
2. Executive Summary
3. Dataset Overview
4. Entity & Relationship Findings (Supplier–License–Model–Customer)
5. Temporal Patterns (Deliverdate)
6. Portfolio Composition (Category/Model/Device)
7. Traceability & Data Quality (Lot/Serial/UDID completeness)
8. Notable Observations & Potential Risks (non-diagnostic; purely data-driven flags)
9. Recommendations / Next Steps (operational and analytical)
10. Appendix:
   - Tables (or tables inline in sections)
   - Entity list
   - Infograph index (links or references)
   - Run metadata (model/provider, prompt hash, dataset versions)

### 8.4 “20 Entities” Definition
The report must extract and list **20 entities** from the filtered dataset. Entities include:
- Top SupplierIDs
- Top CustomerIDs
- Top LicenseNos
- Top Model Nos
- Key Categories
- Key Device Names (normalized display)

The entity list must include frequency/quantity metrics per entity.

### 8.5 Five Required Tables (Minimum)
The report must include at least these 5 tables:
1. Dataset Summary Table (rows, columns, date range, missingness highlights)
2. Top Suppliers Table (count/quantity, unique customers, unique models)
3. Top Customers Table (count/quantity, unique suppliers, unique models)
4. LicenseNo × Model No Cross Table (top combinations)
5. Data Quality Table (missing serial/lot/udid rates, duplicates, suspicious patterns)

### 8.6 Editing & Download
- User can edit report in:
  - Markdown view (rendered + editable)
  - Text view (raw)
- Download options:
  - `.md`
  - (Optional future) `.pdf` export; if included, must preserve headings/tables.

### 8.7 Prompt & Model Control for Report Generation
- Before generating, user can:
  - Edit the report prompt (system + user instructions)
  - Select provider/model from the supported list
  - Set temperature/max tokens (within safe bounds)
- The system stores the prompt/model metadata with the report draft for traceability.

---

## 9. Agentic Execution — Prompt/Model Control + Editable Chaining (Enhanced)

### 9.1 Supported Models (User-Selectable)
- OpenAI: `gpt-4o-mini`, `gpt-4.1-mini`
- Google: `gemini-2.5-flash`, `gemini-3-flash-preview`
- Anthropic: “anthropic models” (configurable list, displayed to user)
- Grok/xAI: `grok-4-fast-reasoning`, `grok-3-mini`

### 9.2 Universal LLM Controls (Applies to All LLM Features)
For every LLM-backed feature (agents, report generation, chart explanations, NoteKeeper magics, skill builder), users can:
- Choose provider/model
- Modify prompt text (system + user prompt)
- Tune parameters: temperature, max tokens (where supported)
- View the exact “input payload” (excluding secrets), including dataset/filter snapshot

### 9.3 Agent-by-Agent Execution
- Agents run **one-by-one** (no forced automation).
- User selects next agent; system suggests typical sequences (optional).
- After each agent run:
  - Output is shown in **Markdown view** and **Text view**
  - User can edit output directly
  - User can set edited output as the input to the next agent
  - Output can be appended into a curated “Final Results” document

### 9.4 Live Agent Run Telemetry
- Status indicator shows: Running / Completed / Failed
- Live log records:
  - Start/end timestamps
  - Selected provider/model
  - Input size and output size
  - Errors and retry suggestions

---

## 10. Document Operating Room (Retained + Integrated)

Retains all original features:
- PDF upload + page trimming + preview
- Text extraction + OCR options:
  - Text-layer extraction
  - Local OCR (Tesseract)
  - Cloud vision OCR (OpenAI/Gemini vision capability if available)
- Markdown reconstruction (conservative formatting)
- Agent execution on extracted/OCR text
- Safe handling of keys and downloads

Enhancements:
- Document outputs can be sent into Report Generator or NoteKeeper as a source.
- Document pipeline steps emit live log events and status chips.

---

## 11. AI NoteKeeper (Enhanced + New AI Magics)

### 11.1 Note Input & Editing
- User can paste or upload:
  - `.txt`, `.md`, and optionally PDF (via extraction/OCR pipeline)
- The NoteKeeper produces an **organized markdown note** with:
  - Title, summary, key points, action items, questions, decisions, and references
  - **Keywords highlighted in coral** (user can customize keyword list and color)

User can edit in:
- Markdown view (rendered + editable)
- Text view (plain)

### 11.2 Keep Prompting (Iterative Refinement)
- Users can “keep prompting” on the note:
  - Model selection + prompt editing supported
  - Outputs can be merged back into the note or saved as an alternate version

### 11.3 Six “AI Magics” (Created for This System)
1. **Structure Wizard**: reorganize into a consistent meeting/review template.
2. **Risk & Compliance Lens**: extract risks, assumptions, missing evidence, and suggested mitigations.
3. **Action Extractor**: produces actionable tasks with owners/placeholders and due-date suggestions.
4. **Concept Map Builder (Textual)**: outputs a markdown mind-map and relationship bullets.
5. **Redaction & Sanitizer**: removes or masks identifiers (SupplierID/CustomerID/SN/Lot) based on user rules.
6. **Bilingual Polisher**: rewrite the note in zh-TW or English while preserving technical terms and IDs.

All magics support prompt editing + model selection.

---

## 12. Skill Builder — skill.md Generation (New)

### 12.1 Purpose
Generate a **`skill.md`** that captures:
- How to create a comprehensive review report and the 6 infographs
- How to apply filters, extract entities, produce the 5 required tables, and draft bilingual narratives
- How to ensure traceability (filters, dataset provenance, prompts/models)

### 12.2 Inputs to Skill Builder
- The latest report draft (or selected sections)
- Infograph metadata (what was generated, filter snapshot)
- Agent run history (selected outputs)
- User-edited guidance (optional)

### 12.3 Skill Creator Methodology Embedded
The skill.md must include:
- Trigger conditions (when to use the skill)
- Required inputs (datasets, filters, language)
- Step-by-step workflow
- Output templates for:
  - Report (3000–4000 words, required sections)
  - Tables (5 required tables)
  - Entities list (20 entities)
  - Infograph generation checklist (6 infographs)
- Quality checks and common failure modes (e.g., missing deliver_date parse, empty serial numbers)

### 12.4 Three Additional WOW AI Features Added to the Skill
The generated skill.md must include instructions for 3 additional AI features usable in future runs:
1. **Narrative Consistency Auditor**: checks that numbers referenced in narrative align with tables and filtered dataset stats.
2. **Entity Disambiguation Assistant**: detects near-duplicate entity labels (e.g., device names with punctuation variations) and proposes normalization mapping.
3. **Insight Prioritizer**: ranks findings by operational significance (volume, growth, concentration risk) and outputs “Top 10 insights” ready for exec summary.

### 12.5 Edit/Download
- Users can edit skill.md in-app (markdown/text views)
- Download as `skill.md`

---

## 13. Export, Versioning, and Traceability

### 13.1 Downloadable Artifacts
- Filtered dataset export (csv/json)
- Infograph data extracts (csv/json per chart)
- Report `.md`
- skill.md
- Agent run bundle (optional zip):
  - prompts (redacted)
  - model/provider selection
  - outputs
  - run timestamps
  - filter snapshots

### 13.2 Provenance Metadata (Required)
Every report/skill export includes:
- Dataset list (names + source types)
- Row counts before/after filtering
- Filter definitions
- Standardization mapping summary
- Model/provider and prompt version identifiers (hash or timestamp-based label)

---

## 14. Deployment on Hugging Face Spaces

### 14.1 Runtime Expectations
- Streamlit app as the primary entrypoint
- Bundled files:
  - `agents.yaml`
  - `dataset.json` (default datasets)
  - Optional default prompt templates and keyword lists

### 14.2 External Dependencies
- LLM APIs: Gemini / OpenAI / Anthropic / Grok
- OCR tools: local (if supported on Space) and/or cloud vision endpoints

### 14.3 Operational Constraints
- Must handle rate limits and transient API failures gracefully:
  - clear errors, retry guidance, and fallback options
- Token usage awareness:
  - warn when report generation may be expensive/long

---

## 15. Performance, Reliability, and QA Requirements

### 15.1 Performance
- Default preview is small (20 rows) to keep UI fast.
- Infographs operate on filtered dataset; warn if record count exceeds a configurable threshold.
- Caching strategy (non-persistent) for:
  - parsed datasets
  - computed aggregations for charts
  - previously generated report drafts (per session)

### 15.2 Reliability
- Robust parsing with clear errors for malformed csv/json.
- Date parsing diagnostics for Deliverdate.
- Duplicate chart ID avoidance (unique keys per chart render).
- “Safe rerun” behavior: changing theme/language should not wipe datasets or report drafts.

### 15.3 Quality Checks (Built-in)
- Data quality panel: missing values, duplicates, suspicious outliers.
- Report validator:
  - word count estimate
  - confirms presence of 5 tables and 20 entities
  - confirms language selection applied consistently
- Skill validator:
  - confirms required sections and the 3 additional WOW features included

---

## 16. Acceptance Criteria (Definition of Done)

1. **WOW UI** supports light/dark, zh-TW/en, and 20 painter styles, with Jackslot selection.
2. Status indicators show API readiness (env/session/missing), dataset stats, OCR status, agent pipeline status.
3. Live log records major events; downloadable with redaction.
4. If API key exists in environment, UI does not show key input; if missing, user can input key in session.
5. For all LLM features, user can edit prompts and choose models from the provided list.
6. Agents run one-by-one; user can edit each output and pass forward.
7. System loads `dataset.json` by default; user can choose default datasets or add more via paste/upload.
8. Dataset preview defaults to 20 records; user can adjust preview count.
9. Filters include supplier/license/model/customer/date zone/SN/lot; applied globally to infographs and reports.
10. Generates 6 interactive infographs including the required supply chain network graph.
11. Generates a bilingual markdown report (zh-TW default) of 3000–4000 words with 5 tables and 20 entities; editable and downloadable.
12. Generates skill.md using the skill creator approach and includes 3 extra WOW AI features; editable and downloadable.

---

## 20 Comprehensive Follow-up Questions

1. For the **20 painter styles**, do you want them to affect only colors/typography, or also chart themes (palette, background, gridlines) and card textures?
2. Should **Jackslot** be purely random, or allow weighting (e.g., “prefer high-contrast styles for dark mode”)?
3. Do you want the **language toggle** to instantly re-render *all* existing outputs (charts, reports, logs), or only apply to newly generated outputs?
4. For **Anthropic models**, should the UI list a fixed curated set (safer), or allow users to type arbitrary model IDs (more flexible but riskier)?
5. Should **Grok/xAI** be treated as OpenAI-compatible only, or do you need a separate provider configuration panel (base URL, headers, org/project fields)?
6. For API keys entered in-session, should the system support a **“lock/unlock”** UX (hide input after saving) even though the key wasn’t from environment?
7. Do you want a **cost estimator** per action (report generation, note magic, agent run) showing approximate tokens and $ range before execution?
8. Should the dataset filtering support **regex** and advanced boolean logic (e.g., (Supplier=A OR Supplier=B) AND Category contains “E.3610”)?
9. Do you want the system to allow **multiple simultaneous filter presets** (saved filter sets) that users can toggle between quickly?
10. For Deliverdate parsing, should the system enforce a strict `YYYYMMDD` format, or accept multiple formats with an explicit “date parsing rules” panel?
11. In the **supply chain network graph**, do you want edges to represent record counts only, or also support a dual-metric view (count + quantity sum)?
12. Should the infographs support **cross-filtering** (click a node/bar to apply filters globally), or remain “view-only + manual filters” for v1 stability?
13. For the **3000–4000 word report**, should the system prioritize narrative depth (interpretation) or operational utility (procedural next steps, checklists)?
14. Do you want the report to include a dedicated **“Regulatory/Compliance framing”** section even though the dataset is supply-chain style (not FDA events)?
15. Should the “20 entities” list be strictly top-20 overall, or should it ensure diversity (e.g., at least 5 suppliers, 5 customers, 5 models, 5 licenses)?
16. For **keyword highlighting in coral**, do you want a user-editable dictionary per project, and should it apply to reports as well as notes?
17. Should users be able to **download the 6 infographs** as a single bundled artifact (zip with images + underlying data + chart configs)?
18. Do you want a **versioning system** inside the session (Report v1/v2, Note v1/v2, Skill v1/v2) with diff comparison?
19. For agent chaining, should the UI support an optional **“pipeline template”** mode that auto-suggests the next agent based on current output type?
20. What level of **data redaction** should be default for exports: none, mask serial/lot only, or a configurable policy that can be saved as a preset?
