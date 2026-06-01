## Summary

The Django admin page is not loading in the backend container because the request path fails during template rendering when Django tries to resolve the active timezone. The traceback shows the container is missing timezone data, which prevents the admin response from completing.

---

## Impact

- **Affected users/systems:** Backend developers and anyone using the Django admin interface in the containerized environment
- **Severity level:** High
- **Business impact:** Admin users cannot access the management UI, which blocks operational work such as reviewing models, editing records, and validating backend data

---

## Reproduction Steps

1. Start the backend stack with Docker Compose.
2. Open the Django admin route at `/admin/`.
3. Let the request proceed through the login/redirect flow.
4. Observe the admin request failing with a server-side traceback instead of rendering the admin UI.

---

## Expected vs Actual Behavior

### Expected Behavior
Django admin should load normally and render the login or admin dashboard page depending on authentication state.

### Actual Behavior
The admin request crashes during response rendering. The logs show `ModuleNotFoundError: No module named 'tzdata'` followed by `zoneinfo._common.ZoneInfoNotFoundError: 'No time zone found with key UTC'`.

---

## Environment Details

- **Service/Component:** Backend / Django admin
- **Environment:** Development
- **Version/Branch:** `develop`
- **Browser/Client:** Web browser hitting `/admin/`
- **OS/System:** Windows host running the backend in Docker; container runtime shows Python 3.14.5 on Linux musl
- **Relevant logs/errors:**
  - `ModuleNotFoundError: No module named 'tzdata'`
  - `zoneinfo._common.ZoneInfoNotFoundError: 'No time zone found with key UTC'`
  - Traceback originates from `django.utils.timezone.get_default_timezone()` while rendering the admin template

---

## Root Cause (if known)

The backend container does not have the `tzdata` package available, but Django is configured to use `TIME_ZONE = UTC`. When the admin template renders and calls timezone helpers, Python's `zoneinfo` module cannot resolve the `UTC` timezone without tzdata installed in the image.

---

## Resolution Steps

- [x] Add `tzdata` to the backend runtime dependencies.
- [x] Rebuild the backend container image so the package is present in the Docker environment.
- [x] Re-test `/admin/` and confirm the page loads without a timezone traceback.

## Validation

The fix was manually validated in the running backend environment. The Django admin page now loads successfully and no longer raises the timezone-related traceback in the container logs.

**Assigned to:** Backend team  
**Target resolution date:** 2026-05-31