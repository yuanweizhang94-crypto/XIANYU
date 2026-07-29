Change ID: CHG-0009-xianyu-upstream-wrapper-mvp
Status: IMPLEMENTING
# CHG-0009 Xianyu upstream wrapper MVP

## Owner authorization

The project owner explicitly authorizes CHG-0009 after CHG-0008 PR #9 was merged and archived. This change starts from latest `main` and may implement only a minimal wrapper around the independently running pinned upstream Pilot service.

## Goal

Allow `D:/xianyu` to use a controlled localhost-only Wrapper for the independent upstream Pilot to complete exactly one supervised message loop: read one real test message and send one explicitly authorized test reply.

The only authorized live validation strings are:

- inbound marker: `XIANYU-WRAPPER-TEST-001`
- reply text: `XIANYU-WRAPPER-ACK-001`

## Non-goals

CHG-0009 does not implement product publishing, product delisting, order handling, refunds, ratings, AI automatic replies, automatic delivery, scheduled tasks, bulk messages, multi-account scheduling, cloud deployment, public services, protocol rewriting, upstream source copying, or CHG-0010.

## Credential boundary

Cookie, Token, Session, Authorization values, browser Profile data, upstream database passwords, Redis passwords, administrator passwords, complete account identifiers, and contact information must remain outside Git and outside the main repository runtime objects. The Wrapper may call localhost APIs and may use a local untracked configuration file, but it must not copy or persist real platform credentials.

## Runtime boundary

The default upstream base URL is `http://127.0.0.1:18089`. Loopback hosts only are allowed by default. Live writes are fail-closed unless both local configuration enables live writes and the CLI command includes `--confirm`.

## Progress

Completed tasks: 6 / 9
Next task: T7 Run complete local verification
