from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from xianyu_system.worker.account.domain import (
    AccountReference,
    InvalidAccountInput,
    InvalidLifecycleTransition,
    Profile,
    ProfileLifecycleStatus,
)

PROFILE_ID = "11111111-1111-4111-8111-111111111111"
OTHER_PROFILE_ID = "22222222-2222-4222-8222-222222222222"


def test_account_reference_normalizes_and_is_immutable() -> None:
    reference = AccountReference(
        profile_id=PROFILE_ID.upper(),
        account_alias=" synthetic-profile-alpha ",
        external_account_identifier=" synthetic-external-reference-alpha ",
        credential_reference=" synthetic-credential-reference-alpha ",
    )

    assert reference.profile_id == PROFILE_ID
    assert reference.account_alias == "synthetic-profile-alpha"
    assert reference.external_account_identifier == "synthetic-external-reference-alpha"
    assert reference.credential_reference == "synthetic-credential-reference-alpha"
    with pytest.raises(FrozenInstanceError):
        reference.account_alias = "synthetic-mutated"  # type: ignore[misc]

    renamed = reference.with_account_alias(" synthetic-profile-beta ")
    with_external = reference.with_external_account_identifier(
        " synthetic-external-reference-beta "
    )
    with_credential = reference.with_credential_reference(
        " synthetic-credential-reference-beta "
    )

    assert renamed is not reference
    assert with_external is not reference
    assert with_credential is not reference
    assert renamed.profile_id == reference.profile_id
    assert with_external.profile_id == reference.profile_id
    assert with_credential.profile_id == reference.profile_id
    assert reference.account_alias == "synthetic-profile-alpha"


def test_account_reference_rejects_invalid_profile_identifier() -> None:
    with pytest.raises(InvalidAccountInput) as error:
        AccountReference(profile_id="not-a-profile-id", account_alias="synthetic-profile")

    assert "synthetic-profile" not in str(error.value)


def test_account_reference_validates_required_and_optional_text_boundaries() -> None:
    AccountReference(profile_id=PROFILE_ID, account_alias="a" * 120)
    AccountReference(
        profile_id=PROFILE_ID,
        account_alias="synthetic-profile",
        external_account_identifier="e" * 256,
        credential_reference="c" * 512,
    )
    AccountReference(
        profile_id=PROFILE_ID,
        account_alias="synthetic-profile",
        external_account_identifier=None,
        credential_reference=None,
    )

    invalid_inputs = [
        {"account_alias": ""},
        {"account_alias": "   "},
        {"account_alias": "a" * 121},
        {
            "account_alias": "synthetic-profile",
            "external_account_identifier": "e" * 257,
        },
        {
            "account_alias": "synthetic-profile",
            "external_account_identifier": "   ",
        },
        {"account_alias": "synthetic-profile", "credential_reference": "c" * 513},
        {"account_alias": "synthetic-profile", "credential_reference": "   "},
    ]

    for invalid_input in invalid_inputs:
        with pytest.raises(InvalidAccountInput):
            AccountReference(profile_id=PROFILE_ID, **invalid_input)


def test_profile_create_builds_owned_pending_account_reference() -> None:
    profile = Profile.create(
        profile_id=PROFILE_ID.upper(),
        account_alias=" synthetic-profile-alpha ",
        external_account_identifier=" synthetic-external-reference-alpha ",
    )

    assert profile.profile_id == PROFILE_ID
    assert isinstance(profile.account_reference, AccountReference)
    assert profile.account_reference.profile_id == profile.profile_id
    assert profile.account_alias == "synthetic-profile-alpha"
    assert profile.external_account_identifier == "synthetic-external-reference-alpha"
    assert profile.credential_reference is None
    assert profile.lifecycle_status is ProfileLifecycleStatus.PENDING
    assert profile.row_version == 1


def test_profile_rejects_mismatched_account_reference_owner() -> None:
    reference = AccountReference(
        profile_id=PROFILE_ID,
        account_alias="synthetic-profile-alpha",
        external_account_identifier="synthetic-external-reference-alpha",
        credential_reference="synthetic-credential-reference-alpha",
    )

    with pytest.raises(InvalidAccountInput) as error:
        Profile(
            profile_id=OTHER_PROFILE_ID,
            account_reference=reference,
            lifecycle_status=ProfileLifecycleStatus.PENDING,
            row_version=1,
        )

    text = str(error.value)
    assert "synthetic-profile-alpha" not in text
    assert "synthetic-external-reference-alpha" not in text
    assert "synthetic-credential-reference-alpha" not in text


def test_profile_rejects_invalid_row_version() -> None:
    reference = AccountReference(profile_id=PROFILE_ID, account_alias="synthetic-profile")

    for row_version in [0, -1, "1"]:
        with pytest.raises(InvalidAccountInput):
            Profile(
                profile_id=PROFILE_ID,
                account_reference=reference,
                lifecycle_status=ProfileLifecycleStatus.PENDING,
                row_version=row_version,  # type: ignore[arg-type]
            )


def test_profile_metadata_updates_are_immutable_and_preserve_owner() -> None:
    profile = Profile.create(
        profile_id=PROFILE_ID,
        account_alias="synthetic-profile-alpha",
        external_account_identifier="synthetic-external-reference-alpha",
    )

    renamed = profile.with_account_alias(" synthetic-profile-beta ")
    with_external = renamed.with_external_account_identifier(
        " synthetic-external-reference-beta "
    )
    with_credential = with_external.with_credential_reference(
        " synthetic-credential-reference-beta "
    )

    assert renamed is not profile
    assert renamed.account_reference is not profile.account_reference
    assert renamed.profile_id == profile.profile_id
    assert renamed.account_reference.profile_id == profile.profile_id
    assert renamed.account_alias == "synthetic-profile-beta"
    assert profile.account_alias == "synthetic-profile-alpha"
    assert with_external.external_account_identifier == "synthetic-external-reference-beta"
    assert with_credential.credential_reference == "synthetic-credential-reference-beta"
    assert with_credential.profile_id == profile.profile_id


def test_profile_allows_only_approved_lifecycle_transitions() -> None:
    pending = Profile.create(profile_id=PROFILE_ID, account_alias="synthetic-profile")

    enabled = pending.transition_to(ProfileLifecycleStatus.ENABLED)
    disabled_from_pending = pending.transition_to(ProfileLifecycleStatus.DISABLED)
    disabled_from_enabled = enabled.transition_to(ProfileLifecycleStatus.DISABLED)
    reenabled = disabled_from_enabled.transition_to(ProfileLifecycleStatus.ENABLED)

    assert enabled.lifecycle_status is ProfileLifecycleStatus.ENABLED
    assert disabled_from_pending.lifecycle_status is ProfileLifecycleStatus.DISABLED
    assert disabled_from_enabled.lifecycle_status is ProfileLifecycleStatus.DISABLED
    assert reenabled.lifecycle_status is ProfileLifecycleStatus.ENABLED
    assert pending.lifecycle_status is ProfileLifecycleStatus.PENDING


def test_profile_rejects_disallowed_and_unknown_lifecycle_transitions() -> None:
    pending = Profile.create(profile_id=PROFILE_ID, account_alias="synthetic-profile")
    enabled = pending.transition_to(ProfileLifecycleStatus.ENABLED)
    disabled = enabled.transition_to(ProfileLifecycleStatus.DISABLED)

    disallowed = [
        (pending, ProfileLifecycleStatus.PENDING),
        (enabled, ProfileLifecycleStatus.ENABLED),
        (disabled, ProfileLifecycleStatus.DISABLED),
        (enabled, ProfileLifecycleStatus.PENDING),
        (disabled, ProfileLifecycleStatus.PENDING),
        (pending, "UNKNOWN"),
    ]

    for profile, target in disallowed:
        with pytest.raises((InvalidLifecycleTransition, InvalidAccountInput)):
            profile.transition_to(target)


def test_domain_errors_do_not_expose_sensitive_synthetic_values() -> None:
    credential = "synthetic-credential-reference-alpha"
    external = "synthetic-external-reference-alpha"
    alias = "synthetic-profile-alpha"

    with pytest.raises(InvalidAccountInput) as error:
        Profile(
            profile_id=OTHER_PROFILE_ID,
            account_reference=AccountReference(
                profile_id=PROFILE_ID,
                account_alias=alias,
                external_account_identifier=external,
                credential_reference=credential,
            ),
            lifecycle_status=ProfileLifecycleStatus.PENDING,
            row_version=1,
        )

    text = str(error.value)
    assert alias not in text
    assert external not in text
    assert credential not in text
    assert "Cookie" not in text
    assert "Token" not in text
    assert "Secret" not in text
