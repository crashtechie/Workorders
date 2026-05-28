# Documentation Templates

This folder contains reusable templates for writing consistent project documentation.

## Purpose

- Standardize issue reports, planning docs, and wiki pages.
- Reduce formatting overhead and improve readability.

## Recommended Template Types

- Issue template
    - File name should be 'ISS<date format yyyyMMddHHMM>-<service>-<short description>.md', for example, 'ISS202304011230-auth-service-login-bug.md'.
    - This template should include sections for summary, impact, reproduction steps, expected vs actual behavior, environment details, root cause (if known), and resolution steps.
- Incident report template
    - File name should be 'INC<date format yyyyMMddHHMM>-<short description>.md', for example, 'INC202304011230-database-outage.md'.
    - This template should include sections for incident summary, timeline of events, impact assessment, root cause analysis, resolution steps, and post-incident review notes.
- Feature plan template
    - File name should be 'FEAT<date format yyyyMMddHHMM>-<service>-<short description>.md', for example, 'FEAT202304011230-frontend-new-dashboard.md'.
    - This template should include sections for feature overview, user stories, acceptance criteria, implementation plan, and potential risks.
- Architecture decision record template
    - File name should be 'ADR<date format yyyyMMddHHMM>-<short description>.md', for example, 'ADR202304011230-use-fastapi-for-backend.md'.
    - This template should include sections for decision context, considered options, decision outcome, and rationale.
- Wiki article template
    - File name should be 'WIKI<date format yyyyMMddHHMM>-<short description>.md', for example, 'WIKI202304011230-deployment-process.md'.
    - This template should include sections for article overview, detailed content, references, and update history.

## Usage

- Copy a template into the target docs folder.
- Rename the file to a descriptive, date-friendly name.
- Keep section headers consistent unless a section is not applicable.
docs