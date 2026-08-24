# CHG-0028 GitHub PR, CI, and Scope Checkpoint

Date: 2026-08-25
Status: VERIFYING

## Remote and PR

`GITHUB_TRANSPORT_USED=HTTPS_USING_EXISTING_AUTHENTICATION`

`SSH_KEY_CREATED=NO`

`SHARED_ORIGIN_URL_CHANGED=NO`

`REMOTE_BRANCH=feat/CHG-0028-publish-readiness-owner-convergence`

`REMOTE_SHA=95c4675c5dae785fab801affa85cd1975892cd7e`

`PR_NUMBER=41`

`PR_URL=https://github.com/yuanweizhang94-crypto/XIANYU/pull/41`

`PR_HEAD_SHA=95c4675c5dae785fab801affa85cd1975892cd7e`

`PR_BASE_SHA=dc83ef23603c1725d3babcd8f89f54db0592f075`

## Scope classification

`START_BASE_SHA=02fd7ba8a64ebe56d4366635a478b581a3ae1012`

`LOCAL_IMPLEMENTATION_SHA=95c4675c5dae785fab801affa85cd1975892cd7e`

`MAIN_SHA_AT_PR_OPEN=dc83ef23603c1725d3babcd8f89f54db0592f075`

`TRUSTED_BASELINE_GOVERNANCE_TRANSITION=42d0aa8_docs_archive_CHG0027_and_draft_CHG0028`

`TRUSTED_BRANCH_HISTORY_MAIN_TO_HEAD=42d0aa8,c77533c,02fd7ba,95c4675`

`IMPLEMENTATION_DIFF_FILES=10`

`PR_SCOPE_CLEAN=true`

The main-based PR file list has 17 paths. Six CHG-0027 archive rename paths come from trusted baseline governance transition commit `42d0aa8`, which archived CHG0027 and created the CHG0028 active change. They are not this run's implementation change, are not a CHG0027 business reopen, and were not deleted, rewritten, or modified during this closure. The current implementation commit remains exactly the 10-file diff from `02fd7ba8a64ebe56d4366635a478b581a3ae1012` to `95c4675c5dae785fab801affa85cd1975892cd7e`.

## CI classification

`DETERMINISTIC_SECURITY_SCAN=PASS`

`CHG0028_SPECIFIC_CI=PASS_BY_LOG_CLASSIFICATION`

`GLOBAL_CI_STATUS=FAIL_UNRELATED_PRE_EXISTING_GOVERNANCE_DEBT`

`CHG0020_DEBT_ABSORBED=NO`

Initial PR checks for head `95c4675c5dae785fab801affa85cd1975892cd7e`:

- `deterministic-security-scan`: PASS.
- `quality`: FAIL on pre-existing CHG-0020 archive validation debt, `missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md`.
- `tests`: FAIL globally with 11 failures from existing governance debt: CHG-0020 missing archived files, CHG-0022 active evidence path assumptions, README entrypoint wording drift, and AGENTS upstream-pilot wording drift.

The same test log shows CHG-0028 active acceptance and `tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py` passed. A local focused rerun also passed 12/12:

`pytest changes/active/CHG-0028-publish-readiness-owner-convergence/tests/test_acceptance.py tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py`

## Safety counters

`PRODUCTION_MUTATIONS=0`

`BROWSER_ACTIONS=0`

`REAL_BUSINESS_ACTIONS=0`

`NO_PERSISTED_READINESS_WRITER=true`

`NO_BROWSER_SCOPE=true`

`NO_PRODUCTION_MUTATION=true`

`NO_REAL_BUSINESS_ACTION=true`
