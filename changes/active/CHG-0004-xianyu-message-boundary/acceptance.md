# CHG-0004 Acceptance

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## T6 acceptance criteria

1. CHG-0004 remains APPROVED.
2. T1-T6 are complete.
3. T7-T9 remain incomplete.
4. PROJECT_STATE reports 6/9.
5. Next task is `T7 Add unit, contract, security, and active-change acceptance tests`.
6. Message Package contains exactly six approved files.
7. No forbidden Message module exists.
8. Domain import uses no SQLAlchemy.
9. Package import does not register ORM metadata.
10. Migration 0003 exists.
11. Migration down_revision is 0002.
12. Alembic has one linear head.
13. Three approved tables exist after upgrade.
14. No create_all is used.
15. Conversation rows are Profile-scoped.
16. Message rows are Profile-scoped.
17. Delivery Attempt rows are Profile-scoped.
18. Message Content maximum length is 4096.
19. Generic JSON/BLOB/raw frame columns do not exist.
20. NEW creates one Message and one Attempt.
21. DUPLICATE creates no second Message.
22. DUPLICATE creates another Attempt.
23. INDETERMINATE creates a separate Message.
24. CONFLICT rolls back and overwrites nothing.
25. Platform Message Identifier alone is not a dedupe key.
26. Message Content hash is not a dedupe key.
27. Service owns transaction commit/rollback.
28. Repository does not commit.
29. Worker starts STOPPED.
30. Explicit start reaches RUNNING.
31. Only RUNNING accepts Delivery.
32. Worker ownership is immutable.
33. Cross-Profile Delivery blocks Worker.
34. One Worker allows one In-flight Delivery.
35. Busy failure starts no transaction.
36. Invalid content may leave valid Worker RUNNING.
37. Deduplication conflict blocks Worker.
38. Persistence failure fails Worker.
39. Reset is explicit.
40. Stop is graceful.
41. Automatic reconnect count is zero.
42. Automatic retry count is zero.
43. No Thread, Subprocess, Scheduler, DNS, HTTP or WebSocket is created.
44. Only Synthetic Message Fixtures are used.
45. CAP-XY-MESSAGE remains planned.
46. Registry implementation_paths remain empty.
47. Registry test_paths remain empty.
48. active_change remains null.
49. last_verified_commit remains null.
50. Capability Specification remains unchanged.
51. No real customer data exists.
52. PR remains Draft/open/unmerged.
53. Auto-merge remains disabled.
54. Complete verification passes.
55. Conversation is exposed through the import-safe package surface.
56. Package import still does not register Message ORM metadata.
57. Delivery Identity compatibility includes Platform Conversation Identifier.
58. A Platform Conversation Identifier mismatch causes Deduplication Conflict.
59. Conversation conflict writes no additional Conversation, Message, or Delivery Attempt.
60. Invalid Message input may leave a valid Worker RUNNING.
61. Authorization violations block the Worker.
62. Risk violations block the Worker.
63. Protocol violations block the Worker.
64. Deduplication Conflict blocks the Worker.
65. Persistence failures fail the Worker.
66. Internal failures fail the Worker.
67. Unexpected exceptions are converted to sanitized MessageInternalError.
68. stop() cannot transition BLOCKED directly to STOPPED.
69. stop() cannot transition FAILED directly to STOPPED.
70. BLOCKED and FAILED require explicit reset.
71. The five retained permanent-test edits are Migration-head compatibility changes only.
72. Those compatibility changes added no test functions.
73. Tasks remain 6 / 9 and T7 remains incomplete.

## Current authorization

T1 through T6 are complete.

The local, synchronous, Profile-scoped, Synthetic Message receiving boundary is implemented.

T7 is the next executable task and must be performed separately.

CAP-XY-MESSAGE remains planned and unbound pending T8.

This execution does not authorize real WebSocket access, external network access, real Credential access, real account access, real customer-message processing, message sending, API, Web UI, capability binding, Ready-for-review, reviewer requests, auto-merge, or merge.

## T7 acceptance criteria

55. T7 adds exactly 42 new permanent Message tests.
56. `tests/unit/test_message_domain.py` contains exactly 12 explicit top-level tests.
57. `tests/unit/test_message_service.py` contains exactly 9 explicit top-level tests.
58. `tests/unit/test_message_worker.py` contains exactly 8 explicit top-level tests.
59. `tests/contract/test_message_persistence.py` contains exactly 8 explicit top-level tests.
60. `tests/contract/test_message_security.py` contains exactly 5 explicit top-level tests.
61. Existing Import Safety coverage remains exactly three test functions and includes the Message Package import-safe boundary.
62. NEW, DUPLICATE, INDETERMINATE, Content Conflict, and Conversation Conflict behavior are covered.
63. UUID version 4 generation, transaction ownership, rollback, Profile scope, and Account scope are covered.
64. Worker lifecycle, failure-state mapping, explicit reset, one in-flight delivery, re-entry protection, and graceful stop are covered.
65. The three-table schema, Migration lineage, Foreign Keys, database constraints, Repository no-commit behavior, empty downgrade, and non-empty downgrade fail-closed behavior are covered.
66. Import isolation, absence of external integrations, blocked network/subprocess/Home/thread entry points, sanitized errors, and Synthetic Fixture-only evidence are covered.
67. Persistence and Security Contract tests pass in both orders.
68. Account and Message Contract tests pass in both orders.
69. No global SQLAlchemy mapper or metadata cleanup escape hatch is added.
70. No Runtime, Migration, Registry, Capability Specification, dependency, or CI file is modified.
71. `CAP-XY-MESSAGE` remains planned and unbound with empty implementation_paths and test_paths.
72. CHG-0004 remains APPROVED, T1 through T7 are complete, and T8 is the next executable task.
73. T8 is not started by T7.

## T7 corrective acceptance criteria

74. Worker re-entry is triggered from inside an active Service operation.
75. Inner Worker re-entry fails with `WorkerBusy` before a second Service operation begins.
76. The outer Worker operation completes successfully and leaves the Worker `RUNNING`.
77. Graceful stop is covered with deterministic Events and finite-timeout test threads.
78. The Worker enters `STOPPING`, rejects new delivery during `STOPPING`, waits for the in-flight operation, and reaches `STOPPED` only after completion.
79. Repository add methods are tested directly and do not commit.
80. Explicit rollback removes uncommitted Conversation, Message, and Delivery Attempt rows.
81. Repository ownership and UTC timestamp round-trip are covered.
82. Real SQLite evidence covers NEW, DUPLICATE, INDETERMINATE, Content Conflict, and Conversation Conflict.
83. Conflict operations preserve row counts and existing Message Content.
84. Schema evidence covers approved types, lengths, nullable rules, primary keys, foreign keys, unique constraints, check constraints, and prohibited fields.
85. Database evidence covers Profile and Account ownership, Delivery Identity scope, nullable Delivery Identities, Platform Message Identifier reuse, Message Content constraints, decision constraints, Attempt outcomes, and Attempt numbers.
86. Message-only downgrade explicitly targets `0002_xianyu_account_boundary`.
87. Empty Message downgrade preserves Account table/data and supports re-upgrade.
88. Non-empty Message downgrade fails closed and preserves revision, tables, and rows.
89. Security evidence runs Message Service and Message Worker in an isolated process while network, DNS, subprocess, Home-directory, and production thread-start entry points are blocked.
90. Package lazy-import evidence verifies Persistence, Service, and Worker are initially unloaded.
91. Synthetic Fixture and cleanup escape-hatch scans cover all dedicated Message test files and active acceptance evidence.
92. Test counts remain unchanged: 42 permanent Message tests, three Import Safety tests, four active acceptance tests, and 322 full collection.
93. No Runtime, Migration, Registry, Capability Specification, dependency, CI, task count, or generated project state file is modified.
94. T8 remains the next executable task and is not started.

## T7 final evidence follow-up acceptance criteria

95. All approved Message Check Constraint names are covered.
96. UUID length, Account normalization, platform identifiers, Delivery Identity, participant, Message Content, persisted decisions, Attempt outcomes, Attempt numbers, reason codes, and correlation identifiers are covered by Check Constraint semantics.
97. Foreign Key evidence covers constrained columns, referred tables, referred columns, and `ON DELETE RESTRICT`.
98. Migration evidence covers source restrictions, Alembic CLI online upgrade, and offline SQL without creating the offline database file.
99. Remaining Profile, Account, Delivery Identity, Attempt uniqueness, nullable-value, reason, correlation, and scope constraints are covered.
100. Public package evidence verifies initially unloaded Service, Persistence, and Worker modules and actual lazy Domain, Transport, Service, Persistence, and Worker resolution.
101. Security evidence runs a complete isolated Worker flow covering NEW, DUPLICATE, INDETERMINATE, Content Conflict, Conversation Conflict, reset, restart, and stop while network, DNS, subprocess, Home-directory, and production thread-start entry points are blocked.
102. Every dedicated Message test file and active acceptance test is independently checked for UTF-8, BOM absence, Synthetic Fixtures, sensitive values, customer data, and cleanup escape hatches.
103. Test counts remain unchanged: 42 permanent Message tests, three Import Safety tests, four active acceptance tests, and 322 full collection.
104. No Runtime, Migration, Registry, Capability Specification, dependency, CI, task count, or generated project state file is modified.
105. T8 remains the next executable task and is not started.

## T7 exact contract evidence completion acceptance criteria

106. Every expected database IntegrityError case is isolated in its own Connection and Transaction.
107. Empty, blank, and padded Conversation Account References are rejected.
108. Empty, blank, and padded Message Account References are rejected.
109. Empty, blank, and padded Attempt Account References are rejected.
110. Empty, blank, padded, and over-limit Participant References are rejected.
111. Empty, blank, and over-limit Message Content is rejected.
112. DUPLICATE, CONFLICT, and unknown persisted decisions are rejected.
113. CONFLICT and unknown Attempt outcomes are rejected.
114. Zero and negative Attempt numbers are rejected.
115. Blank, padded, and over-limit Reason Codes are rejected.
116. Blank, padded, and over-limit Correlation Identifiers are rejected.
117. Duplicate Delivery Identity is directly rejected in the same Profile and Account.
118. The same Delivery Identity is directly allowed for the same Profile in another Account.
119. Duplicate Attempt Number is directly rejected.
120. Offline SQL contains no external URL, Credential, browser-profile, or customer-data text.
121. The isolated Content Conflict preserves Conversation, Message, and Attempt counts.
122. The isolated Conversation Conflict preserves Conversation, Message, and Attempt counts.
123. The isolated final row counts are one Conversation, two Messages, and three Attempts.
124. Every dedicated Message evidence file is checked for plus-phone and standalone long-number values.
125. Every dedicated Message evidence file is checked for Credential-like values.
126. Every dedicated Message evidence file is checked for real-customer, customer-message, customer-data, raw-frame, production-account, live-account, and real-account text.
127. Test counts remain 42 permanent Message tests and 322 total tests.
128. Tasks remain 7 / 9 and T8 remains incomplete.

## T7 sensitive-scan correction acceptance criteria

129. Per-file sensitive checks scan complete Source without deleting or filtering lines.
130. No target file or forbidden phrase is allowlisted.
131. Plus-phone detection supports spaces, hyphens, periods, and parentheses.
132. Plus-phone detection requires at least eight digits.
133. Standalone long-number detection begins at eleven digits.
134. UUID-like embedded numeric segments are not treated as standalone phone values.
135. Bearer values are detected.
136. Authorization Header values are detected without matching MessageAuthorizationViolation.
137. API Key forms are detected.
138. Access Token forms are detected.
139. Refresh Token forms are detected.
140. Session Cookie forms are detected.
141. Password assignment forms are detected.
142. Secret assignment forms are detected.
143. Real-customer, customer-message, and customer-data phrases are detected.
144. Raw-frame spaced and underscored forms are detected.
145. Production-account and live-account spaced and hyphenated forms are detected.
146. Real-Xianyu-account forms are detected.
147. Positive controls prove every sensitive scanner category is active.
148. Scanner failure messages do not expose matched sensitive values.
149. Six approved Message evidence files remain the exact scan target.
150. Permanent Message test count remains 42.
151. Full collection remains 322.
152. Tasks remain 7 / 9 and T8 remains incomplete.

## T7 quoted-phrase bypass removal acceptance criteria

153. The quoted forbidden-phrase bypass is removed.
154. Forbidden phrases are detected inside single-quoted strings.
155. Forbidden phrases are detected inside double-quoted strings.
156. Forbidden phrases are detected when embedded in surrounding text.
157. Forbidden phrases are detected through direct complete-Source matching.
158. No quote-aware lookbehind or lookahead is used.
159. No forbidden phrase is ignored because it is a Python string literal.
160. Phrase positive controls use the same detector as real file scanning.
161. Failure diagnostics expose no matched phrase.
162. Persistence scanner definitions use runtime string composition.
163. Persistence Offline SQL scanning semantics remain unchanged.
164. Permanent Message test count remains 42.
165. Full collection remains 322.
166. Tasks remain 7 / 9 and T8 remains incomplete.

## T8 evidence candidate criteria

1. Exact seven implementation paths registered.
2. Exact ten test paths registered.
3. All paths safe, relative, existing and duplicate-free.
4. Status implementing.
5. active_change CHG-0004-xianyu-message-boundary.
6. last_verified_commit null.
7. Counts planned 5, implementing 1, verified 4.
8. Tasks remain 7/9.
9. next_task remains T8.
10. Full collection remains 322.
11. PR remains Draft/open/unmerged.
12. No Runtime, Migration, dependency or CI changes.

## T8 acceptance criteria

1. T1-T8 complete.
2. T9 incomplete.
3. PROJECT_STATE completed = 8.
4. PROJECT_STATE next_task = T9.
5. CAP-XY-MESSAGE status verified.
6. active_change null.
7. last_verified_commit equals Candidate SHA.
8. Candidate SHA exists and is HEAD ancestor.
9. Exact seven implementation paths preserved.
10. Exact ten test paths preserved.
11. Paths exist, safe and duplicate-free.
12. Specification lists every path.
13. Specification records Candidate SHA.
14. Counts planned 5 and verified 5.
15. No implementing Capability.
16. Unit 225.
17. Contract 78.
18. Permanent acceptance 15.
19. Active acceptance 4.
20. Full collection 322.
21. Complete verification and offline gate pass.
22. No Runtime, Migration, dependency or CI changes.
23. PR remains Draft/open/unmerged.
24. T9, Ready, Reviewer request, auto-merge and merge are not authorized.
