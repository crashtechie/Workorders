# ADR-006: Reporting and Export

**Date:** 2026-05-28  
**Status:** Accepted  
**Deciders:** Project team

---

## Decision Context

**What is the problem we are trying to solve?**

- **Problem statement:** Business staff need to extract operational data (workorder lists, billing summaries, inventory status) for use outside the application — for bookkeeping, reconciliation, or management review. The MVP must support at least one export format while keeping delivery scope manageable.
- **Driving factors:** The business has an immediate need for data portability. However, implementing multiple rich export formats (PDF formatted invoices, XLSX workbooks) carries significant development and layout complexity that would delay the initial release.
- **Deadline:** Export capability must ship in MVP; the format decision must be made before reporting UI work begins.
- **Affected components:** Backend report endpoints, frontend reporting views, CSV generation logic.

---

## Considered Options

### Option 1: CSV Export in MVP — Defer PDF and XLSX

**Description:** All MVP reports support on-screen display and CSV export. PDF and XLSX export formats are deferred to a post-MVP phase. The backend generates CSV directly from query results; no external library dependency is required.

**Pros:**
- CSV is universally importable (Excel, Google Sheets, accounting tools)
- Zero layout complexity — no templating, pagination, or font rendering
- Fast to implement: Python's standard `csv` module requires no additional dependencies
- Meets immediate business need for data portability and bookkeeping
- Leaves room for richer formats when layout requirements are better understood

**Cons:**
- CSV cannot represent formatted invoices or customer-facing documents
- Requires the business to use a spreadsheet tool for any formatted output in the interim

### Option 2: PDF Export in MVP

**Description:** Reports are exportable as formatted PDFs using a library such as ReportLab or WeasyPrint.

**Pros:**
- Customer-ready formatted output from day one
- Professional appearance for invoices and summaries

**Cons:**
- Significant template design and layout effort
- PDF generation libraries add dependency weight and render complexity
- Layout and pagination edge cases are a common source of bugs
- Delays MVP delivery for a feature that can be added post-launch

### Option 3: XLSX Export in MVP

**Description:** Reports export as Excel workbooks using a library such as openpyxl or xlsxwriter.

**Pros:**
- Rich formatting, multiple sheets, formulas possible

**Cons:**
- Library dependency; more complex than CSV for equivalent tabular data
- Overkill for the initial export requirement — the data is what matters, not formatting
- Offers no meaningful advantage over CSV for the MVP operational use case

---

## Decision Outcome

> **Decided:** We will ship **CSV export only in the MVP** for all operational reports. PDF and XLSX export formats are explicitly deferred to a post-MVP phase (Phase 2 per the release plan).

---

## Rationale

1. **Best fit for requirements:** CSV satisfies the immediate need for data portability and bookkeeping without introducing layout risk.
2. **Long-term scalability:** The backend report query layer is format-agnostic; adding PDF/XLSX renderers post-MVP requires only a new output adapter.
3. **Team expertise:** Python's built-in CSV support requires no additional expertise or dependency evaluation.
4. **Maintenance & support:** No additional library to version, audit, or maintain in MVP.
5. **Integration:** CSV output is importable by virtually every business tool the shop might use (QuickBooks, Excel, Google Sheets).
6. **Risk mitigation:** Removing format complexity from MVP scope reduces delivery risk and keeps the initial release focused on operational correctness.

---

## Implementation Notes

- **First steps:** Define the standard report list (workorder summary, billing summary, inventory status); implement backend `/reports/{name}/export?format=csv` endpoints; add export buttons to frontend report views.
- **Dependencies:** ADR-003 (Domain Model) for the data available in each report; ADR-002 (Authorization Model) — `admin` role required for most reports; `sales_staff` and `technician` may access operationally relevant report subsets.
- **Success criteria:** All MVP report views have a working CSV export; exported files open correctly in Excel and Google Sheets; sensitive fields (per ADR-005) are excluded from all exports.
- **Migration path:** Post-MVP, add PDF and XLSX as additional format options on the same endpoints without changing the report query logic.

---

## Consequences

### Positive Consequences
- MVP delivers data portability immediately with minimal implementation risk
- Report query layer is cleanly separated from output format, enabling easy post-MVP expansion
- No external PDF/XLSX library risk or maintenance burden in MVP

### Negative Consequences / Trade-offs
- Business cannot generate formatted customer invoices from the system in MVP — a manual step or workaround will be needed
- PDF export is a Phase 2 commitment that must be tracked in the release plan
