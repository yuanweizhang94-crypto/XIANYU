Change ID: CHG-0008-xianyu-upstream-integration-foundation
Status: VERIFYING
# Tasks

- [x] T1 Obtain explicit project-owner approval for CHG-0008
- [x] T2 Pivot CHG-0008 to upstream pilot and stop unnecessary offline adapter abstraction
- [x] T3 Pin upstream projects and record license and safety audit facts
- [x] T4 Define isolated deployment, test-account, credential, and live-operation boundaries
- [x] T5 Record P0-P7 supervised pilot checklist and stop conditions
- [x] T6 Execute local isolated P0 startup only after operator approves upstream runtime setup
- [x] T7 Execute supervised account P1-P3 only with a dedicated test account
- [x] T8 Execute supervised manual operation P4-P7 only after P1-P3 pass
- [x] T9 Record pilot conclusion and final PR administration

## Current progress

Completed tasks: 9 / 9
Next task: null
Pilot status: P2_P6_PASSED_WITH_OPERATOR_DELISTED_CLEANUP

## T7 evidence

T7 is complete. P1 manual scan login passed after supervised QR scan with a dedicated test account and operator-completed official mobile-side verification. P2 online WebSocket validation passed with `xianyu_pilot_websocket` bound to `127.0.0.1:18090`, one connected instance, and a controlled stop/start recovery. P3 read-only message verification passed after a controlled second account sent a test message; the Pilot recorded the inbound marker while automatic reply remained skipped and no outgoing message occurred.

## T8 evidence

T8 is complete for supervised manual operations. P4 passed after the project owner manually replied in the official client and the Pilot observed the event without automated sending. P5 passed by operator attestation and side-effect audit after the project owner manually published one controlled test listing. P6 passed as operator-delisted cleanup, not deletion; the project owner took the listing off sale in the official client. P7 one-time schedule was not executed and remains outside CHG-0008 runtime evidence.

## T9 evidence

T9 final administration is complete for the Draft PR state. Final recommendation is `WRAP`. PR #9 remains Draft, open, and unmerged. No Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, CHG-0009, upstream code copy, main-repository runtime adoption, scheduler, crawler, promotion, updater, automatic message sending, automatic publishing, automatic deletion, Cookie/Token/Session output, or credential commit was performed.
