Change ID: CHG-0008-xianyu-upstream-integration-foundation
Status: IMPLEMENTING
# Tasks

- [x] T1 Obtain explicit project-owner approval for CHG-0008
- [x] T2 Pivot CHG-0008 to upstream pilot and stop unnecessary offline adapter abstraction
- [x] T3 Pin upstream projects and record license and safety audit facts
- [x] T4 Define isolated deployment, test-account, credential, and live-operation boundaries
- [x] T5 Record P0-P7 supervised pilot checklist and stop conditions
- [x] T6 Execute local isolated P0 startup only after operator approves upstream runtime setup
- [ ] T7 Execute supervised account P1-P3 only with a dedicated test account
- [ ] T8 Execute supervised manual operation P4-P7 only after P1-P3 pass
- [ ] T9 Record pilot conclusion and final PR administration

## Current progress

Completed tasks: 6 / 9
Next task: T7 Execute supervised account P1-P3 only with a dedicated test account
Pilot status: WAITING_FOR_OPERATOR_APPROVED_P2_ONLINE

## T7 partial evidence

P1 result: PASSED after supervised QR scan with a dedicated test account. P2 online state remains WAITING_FOR_OPERATOR_APPROVAL and must not start without separate authorization. P3 remains blocked by P2 and a controlled message source.
