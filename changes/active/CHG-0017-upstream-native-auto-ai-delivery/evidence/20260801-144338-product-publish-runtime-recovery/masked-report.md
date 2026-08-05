# CHG-0017 Product Publish Runtime Recovery Masked Report

## Execution Contract

- User outcome: recover upstream-native product publish automation for ACCOUNT-A and prove any result with one controlled publish attempt at most, while ACCOUNT-B uses only official interactive login recovery.
- Confirmed blocker: ACCOUNT-A reached the publish URL but the publish form did not render.
- Smallest success test: render form without submit, rebuild the candidate image reproducibly, verify runtime hashes, pass duplicate checks, run at most one submit, sync catalog, and confirm exactly one created item or a precise platform rejection.

## Upstream Evidence

- Pinned candidate source: `D:/xianyu-upstream-delivery-chg0017`
- Pinned candidate HEAD: `4c5e1ac5f532c7313365d70409ae115305de8a55`
- Upstream native functions used:
  - `backend-web/app/services/xianyu_publisher.py`
  - `common/services/xianyu_publish_service.py`
  - `common/services/publish_execution_service.py`
  - `backend-web/app/api/routes/product_publish.py`
  - `backend-web/app/api/routes/qr_login.py`
  - `backend-web/app/services/qr_login/manager.py`
- Latest upstream main was checked for an existing publish/login-state fix. No directly transplantable fix was found in the relevant publish/cookie/browser route set.

## Root Cause

- Root cause confirmed: the publish page could return an official passport quick-enter iframe instead of the publish form.
- Previous behavior: the publisher did not handle this official quick-enter state and later misclassified the outcome as a generic field/page problem.
- Current non-submit validation after fix:
  - publish page loaded: true
  - publish form rendered: true
  - input count: 9
  - button count: 2
  - file input count: 1
  - upload-like controls: 5
  - login iframe: false
  - risk verification: false
  - request failures: 0
  - JavaScript page errors: 0

## Runtime Deployment

- Rebuilt service: `backend-web`
- Candidate image rebuilt: true
- Runtime hotpatch: false
- Runtime container updated: true
- Runtime health: healthy
- Container image: `sha256:bd04ae49ca47225686f048c52a422e3b677677d781dfa3eb7835941dcca678d7`
- Runtime code hash matches host candidate source:
  - `xianyu_publisher.py`: `de7088d8e0a4288166ddaa63e17146b30d8e76bfb2df2436cf92e70de54c1f64`
  - `publish_execution_service.py`: `e8e1a70314ca41072708d077d8e12e36e5cebb3a9d448b40b2795d48b9649e81`
- Browser version: Chromium `151.0.7922.34`
- Publish User-Agent aligned to Chromium 151: true

## Controlled Publish Attempt

- Duplicate check before submit: pass
- One allowed real publish attempt was consumed.
- Publish log id: 11
- Publish result: failed
- Failure classification: `platform_validation_error`
- Publish request sent: false
- Item id present in publish result: false
- Item URL present in publish result: false
- Platform catalog after checks contains a product row, but the failed publish log has no item id or URL, so this row is not attributed to the controlled attempt.
- Publish retest verdict: fail

## ACCOUNT-B

- Login method: QR scan / official verification.
- Username/password configured: false.
- Existing QR login API: available as generic upstream `qr-login` session.
- Safe target binding to a preselected ACCOUNT-B: not available in the QR generate request.
- A generic QR session was not created because it could expire unseen and could be associated with whichever account is scanned.
- Required owner action: use the upstream account management page QR login flow for ACCOUNT-B, then verify the resulting account identity before starting any ACCOUNT-B publish action.

## Validation

- Targeted publish tests: 11 passed.
- `scripts/validate_change.py`: passed.
- `scripts/verify_repository.py`: passed, 599 tests passed with 1 pre-existing Starlette/httpx warning.
- Frontend build: not required; no frontend source was changed in this recovery step.

## Security

- Plaintext Cookie exposed: false
- Token exposed: false
- API key exposed: false
- Cross-account Cookie used: false
- Verification bypassed: false
- Proxy password logged: false
- Commit created: false
- Push performed: false
- PR merged: false
- Change archived: false
