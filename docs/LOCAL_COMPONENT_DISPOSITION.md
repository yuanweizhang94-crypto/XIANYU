# Local Component Disposition

Change: CHG-0011-upstream-first-product-direction-freeze

This document records how local components created during CHG-0009 and CHG-0010 are positioned after the upstream-first direction freeze. No files are deleted in CHG-0011.

| Local component | Source | Current disposition | Allowed use | Forbidden use | Retirement path |
|---|---|---|---|---|---|
| CHG-0009 upstream Wrapper | `app/xianyu_system/upstream/` | KEEP_DIAGNOSTIC_ONLY | localhost health, account status, listener status, recent-message diagnostics, and supervised manual send diagnostics | formal automatic reply execution, business rule ownership, protocol rewrite | keep operations surface; narrow if upstream native APIs cover diagnostics |
| Wrapper health/account/listener commands | `python -m xianyu_system upstream ...` | KEEP_OPERATIONS | start/stop/status checks when explicitly authorized | hiding a second business executor behind operations commands | keep under operations governance |
| Wrapper manual send capability | CHG-0009 send boundary | KEEP_FOR_SUPERVISED_DIAGNOSTICS | one-off operator-approved diagnostic send only | production automatic reply sender | restrict further in CHG-0015 if upstream native validation passes |
| CHG-0010 deterministic autoreply worker | `app/xianyu_system/worker/autoreply/` | FREEZE_AND_DEPRECATE | historical evidence and possible controlled diagnostic comparison only | formal automatic reply executor, second worker, new rule features | CHG-0015 evaluate and retire after CHG-0012/CHG-0013 |
| Local YAML rule engine | `.local/autoreply.yaml` and example config | DEPRECATE | disabled examples and historical tests | copying upstream keyword/default/AI rules into YAML | remove or archive in CHG-0015 |
| Local rule matcher | CHG-0010 matcher code | DEPRECATE | unit-test evidence only | production keyword/default matching | retire after upstream native keyword validation |
| Local background worker | CHG-0010 process manager | DEPRECATE | stopped by default; no scheduled startup | long-running production executor | remove service path in CHG-0015 if safe |
| Local listener ownership helper | wrapper/listener helper | KEEP_OPERATIONS | operational start/stop/status of owned listener when no native executor is active | second message-receiving business engine | keep only for diagnostics and wrapper health |
| Local idempotency | CHG-0010 state/audit | FREEZE | historical duplicate-safety evidence | parallel production dedup authority | evaluate archival/retirement in CHG-0015 |
| Local audit | CHG-0010 audit state | FREEZE | historical validation evidence | formal upstream auto-reply log replacement | defer to upstream `xy_auto_reply_message_logs` |
| Local CLI | `python -m xianyu_system` | KEEP_OPERATIONS | governance, diagnostics, verification, redacted status | hidden business feature entry point | continue as control-layer CLI |

## Final positioning

- CHG-0009 Wrapper: operations and diagnostics only.
- CHG-0010 worker: frozen, deprecated, not a formal executor.
- Formal automatic reply sole executor: upstream native automatic reply service, after validation in CHG-0012 and CHG-0013.
