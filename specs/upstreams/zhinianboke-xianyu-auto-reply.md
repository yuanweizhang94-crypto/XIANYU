# zhinianboke/xianyu-auto-reply

- Repository: zhinianboke/xianyu-auto-reply
- Pinned commit: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Local lab path: `D:/xianyu-upstream-pilot`
- License: AGPL-3.0
- Role: primary upstream pilot candidate

## Static audit summary

The pinned checkout exists outside the main repository and was inspected without running services or scripts. Static audit found deploy and update scripts, Docker Compose defaults, prebuilt image defaults, services binding to all interfaces by default, database and Redis credentials that must be changed, Cookie/Token/session handling modules, CAPTCHA/slider/face verification modules, WebSocket modules, and publish/delete services.

## Safe pilot requirement

Before P0 runtime execution, an operator must approve a localhost-only setup, change all default credentials, prevent public port exposure, avoid remote update scripts and unverified prebuilt images, and use isolated volumes not mounted from `D:/xianyu` or browser profile directories.
