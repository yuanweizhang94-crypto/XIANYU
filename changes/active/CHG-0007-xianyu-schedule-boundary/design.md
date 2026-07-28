# CHG-0007 Design

Status: APPROVED
Change ID: CHG-0007-xianyu-schedule-boundary

## Draft design posture

DRAFT records design intent only. It does not authorize implementation.

## Proposed boundary

The proposed Schedule boundary will reuse xianyu_system.core.scheduler as infrastructure and will keep business facts in a Schedule Repository. APScheduler MemoryJobStore may only be an in-process wakeup adapter and never the business fact source.

## Proposed exclusions

The design excludes recurring schedules, distributed scheduling, persistent APScheduler JobStores, platform access, browser automation, Credential handling, WeCom, AI, Redis, Celery, and external queues.

## Review focus

T2 through T5 must approve terminology, safety boundaries, deterministic decision behavior, and ownership before Runtime code appears.


## T1 approval record

This instruction is the explicit project-owner authorization for CHG-0007 T1 through T9, executed in order.

T6 may implement only the approved local deterministic Schedule boundary. It does not authorize real Xianyu access, browser automation, Playwright, Credential handling, WeCom, AI, operations-console work, recurring schedules, Redis, Celery, or external queues.

Merge, archive, and branch deletion remain gated by the later exact CI, PR, merge, post-merge, and archive checks in this change.
