# 2026-08-16 X11 Human Entry + Auto Reply reconnect evidence

## Execution contract

- User outcome: show the same Docker canonical Profile on the real Windows desktop for human official verification, and restore normal Auto Reply socket reconnect without turning Chat PVR into Auto Reply full-auth blocking.
- Confirmed blockers: no usable Docker-to-Windows display transport existed; five Auto Reply sockets later disconnected after their live Token had been cleared when PVR was marked even though heartbeats continued for hours.
- Smallest success test: local-only X11 transport works; a non-account Chromium GUI is visible on Windows; Human Entry accepts only account_id and fixed Goofish homepage; the five offline accounts recover serially through existing cached auth with zero Token API calls; focused tests/compile/patch check pass.
- Reuse decision: `PATCH_UPSTREAM` + existing Windows display transport. Existing canonical Profile resolver, browser slot, account lock, CookieTokenManager, CookieManager, WebSocket owner and Backend auth/ownership are reused. No second browser manager, Token system, verification monitor, Scheduler or Profile copy is introduced.
- Rollback: remove the VcXsrv local firewall rule/service process and revert only the five-file incremental runtime patch; existing Profile/Cookie/database data remain unchanged.

## X11 transport evidence

- VcXsrv source: official `marchaesen/vcxsrv` GitHub release; downloaded package SHA256 matched the Microsoft WinGet manifest (`DF7FED8F49665D0592528AB6BE9D07111EA73C6848283D128B77690E05B8F90B`).
- VcXsrv runs in the logged-in Windows desktop user session, not SYSTEM Session 0.
- Listener: `vcxsrv.exe`, TCP 6000, bind `0.0.0.0`.
- Windows Firewall allow rule is restricted to local Docker/WSL virtual networks only (`172.24.144.0/20`, `192.168.65.0/24`); WLAN/public ranges are not allowed.
- Docker `host.docker.internal` resolved to the Docker Desktop host gateway and TCP 6000 connected successfully.
- A non-account, non-canonical-profile Chromium probe produced a real Session-1 Windows window titled `XIANYU_X11_DISPLAY_PROBE_2...`; therefore `DOCKER_GUI_VISIBLE_ON_WINDOWS=true` before any account Profile use.

## Auto Reply direct evidence

- At about 08:55, the five later-offline accounts received platform-verification responses while their WebSockets were still connected. `_mark_platform_verification_required()` set `current_token=None` even though heartbeats continued normally afterward.
- At the later natural disconnect, the reconnect loop therefore entered `WebSocket连接前获取Token`; PVR state prevented the normal existing-auth socket reconnect path.
- This is a local reconnect semantic regression: Chat/PVR state had destroyed Auto Reply's live in-memory reconnect credential before the socket actually became invalid.
- The five offline accounts were restarted strictly one at a time with the existing account restart owner and `invalidate_token_cache=false`. Each reused the existing expired Token cache, established IM registration, and produced a fresh heartbeat without a local/remote Token API call or CAPTCHA delegation.
- Recovered accounts: `2217936413500`, `2219319284219`, `2196106636`, `1034641456`, `2858469041`. The previously-online `2214313339860` was not reauthenticated.
- After recovery, all six enabled accounts produced fresh heartbeat evidence.

## Minimal source patch

- Runtime base: current production Backend/WebSocket files copied before deployment.
- Changed runtime files: 5.
- Incremental patch: `vendor/patches/xianyu-auto-reply/b75d63b-chg0018-human-verification-reconnect.patch`.
- Patch SHA256: `B87532B67BDF6B7649DB4FAC85C3B5F90D0F425C699FB59E89C5A613643EF8A2`.
- Patch clean-apply check against the recopied production runtime baseline: PASS.
- Human-entry focused runtime tests: 14 passed.
- Existing Auto Reply stability consolidation tests after the reconnect semantic change: 44 passed.
- Modified runtime Python files `py_compile`: PASS.

## Safety boundaries

- Human Entry caller input: `account_id` only.
- Fixed navigation: `https://www.goofish.com/` only.
- No raw punish/captcha/challenge/x5sec URL is accepted or returned.
- Same canonical Profile only; no copy, migration, temp profile or incognito profile.
- The existing global browser slot and per-account browser lock remain held until the human Chromium process exits.
- Browser open does not perform Token, CAPTCHA, Chat Connect, verification completion, or automatic recheck.
- Recheck is a separate explicit POST and performs one canonical Profile health probe only; failed recheck keeps PVR; successful recheck may persist authoritative browser Cookie through the existing writer and clear the existing PVR marker. It does not restart WebSocket.

## Pending production gate

GitHub persistence and targeted Backend/WebSocket deployment are required before the first real account Human Entry. After deployment, only account `2217936413500` may be opened first. Browser-open success must stop at `WAITING_FOR_REAL_USER_OFFICIAL_VERIFICATION=true`; no automatic recheck, Token, Chat Connect or CAPTCHA is permitted before the real user explicitly says verification is complete.
