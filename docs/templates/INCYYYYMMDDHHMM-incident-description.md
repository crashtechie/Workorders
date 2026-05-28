# Incident Report Template

> **How to use this template:**
> 1. Copy this file to the appropriate docs subfolder (e.g., `docs/logs/backend/`)
> 2. Rename the file following the pattern: `INC<date>-<short-description>.md`
>    - Example: `INC202605271230-database-outage.md`
> 3. Fill in each section below with detailed incident information
> 4. Delete this instruction block when done

---

## Incident Summary

**Overview of what happened**

Provide a concise summary of the incident, including what service/system was affected and the general nature of the problem.

---

## Timeline of Events

**Chronological record of the incident**

Use the format: **[HH:MM UTC] - Description**

- **[10:15 UTC]** - Incident started; alerts triggered
- **[10:20 UTC]** - On-call team notified
- **[10:35 UTC]** - Root cause identified
- **[10:50 UTC]** - Mitigation steps implemented
- **[11:05 UTC]** - Service restored and verified
- **[11:30 UTC]** - Full recovery confirmed

---

## Impact Assessment

**Who was affected and to what extent?**

- **Duration:** Start time - End time (total duration)
- **Services affected:** List all impacted services or systems
- **Users impacted:** Estimated number of users and percentage of user base
- **Data loss/corruption:** Was any data lost or corrupted? Specify scope
- **Financial impact:** If applicable, estimate the business impact
- **SLA violation:** Did this exceed any SLA commitments?

---

## Root Cause Analysis

**Why did this incident occur?**

Provide a detailed analysis of the underlying cause(s):

### Primary Cause
Describe the main factor that led to the incident.

### Contributing Factors
List any secondary factors that made the situation worse or delayed resolution:
- Factor 1
- Factor 2
- Factor 3

### Failure Points
Identify what monitoring/alerting/safeguards failed to prevent this.

---

## Resolution Steps

**Actions taken to resolve the incident**

1. Initial response action
2. Investigation step
3. Mitigation measure
4. Verification step
5. Communication to stakeholders

---

## Post-Incident Review Notes

**Lessons learned and preventive measures**

### What Went Well
- Point 1
- Point 2

### What Could Be Improved
- Improvement 1
- Improvement 2

### Action Items to Prevent Recurrence
- [ ] Action item 1 (Owner: [Name], Due: [Date])
- [ ] Action item 2 (Owner: [Name], Due: [Date])
- [ ] Action item 3 (Owner: [Name], Due: [Date])

**Incident severity:** Sev-1 / Sev-2 / Sev-3 / Sev-4  
**Review date:** [Date]  
**Reviewed by:** [Team/Person]
