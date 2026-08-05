from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from atlas_core import Artifact, ExternalResource, Provenance


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 5,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "external_resource_id": "external-resource:01HZY3K9G8N7Q2R5T6V8W0X1Y2",
        "external_resource_kind": "object",
        "external_identifier": "abc123",
        "resource_locator": "https://example.invalid/resource/abc123",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_external_resource_can_be_created() -> None:
    arguments = _valid_arguments()

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_id == (
        "external-resource:01HZY3K9G8N7Q2R5T6V8W0X1Y2"
    )
    assert external_resource.external_resource_kind == "object"
    assert external_resource.external_identifier == "abc123"
    assert external_resource.resource_locator == (
        "https://example.invalid/resource/abc123"
    )
    assert external_resource.recorded_at == arguments["recorded_at"]


def test_external_resource_is_exported_from_package_root() -> None:
    from atlas_core.external_resource import ExternalResource as ModuleExternalResource

    assert ExternalResource is ModuleExternalResource


def test_external_resource_is_immutable() -> None:
    external_resource = ExternalResource(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        external_resource.external_resource_kind = "changed"  # type: ignore[misc]


def test_external_resource_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        ExternalResource(*arguments.values())  # type: ignore[misc]


def test_external_resource_has_slots() -> None:
    external_resource = ExternalResource(**_valid_arguments())

    assert not hasattr(external_resource, "__dict__")


def test_external_resource_has_exact_approved_field_set_and_order() -> None:
    field_names = tuple(field.name for field in fields(ExternalResource))

    assert field_names == (
        "external_resource_id",
        "external_resource_kind",
        "external_identifier",
        "resource_locator",
        "recorded_at",
    )


def test_external_resource_field_count_is_five() -> None:
    assert len(fields(ExternalResource)) == 5


def test_three_fields_are_required() -> None:
    required = [
        field
        for field in fields(ExternalResource)
        if field.default is MISSING and field.default_factory is MISSING  # type: ignore[misc]
    ]
    required_names = {field.name for field in required}

    assert required_names == {
        "external_resource_id",
        "external_resource_kind",
        "recorded_at",
    }
    assert len(required) == 3


def test_two_fields_are_optional_with_default_none() -> None:
    optional = [
        field
        for field in fields(ExternalResource)
        if field.default is not MISSING or field.default_factory is not MISSING  # type: ignore[misc]
    ]
    optional_names = {field.name for field in optional}

    assert optional_names == {"external_identifier", "resource_locator"}
    assert len(optional) == 2
    for field in optional:
        assert field.default is None


def test_external_resource_has_no_canonical_name_field() -> None:
    field_names = {field.name for field in fields(ExternalResource)}

    assert "canonical_name" not in field_names


def test_external_resource_module_imports_only_standard_library() -> None:
    import ast
    import inspect

    import atlas_core.external_resource as external_resource_module

    source = inspect.getsource(external_resource_module)
    tree = ast.parse(source)

    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.add(node.module)

    prohibited_modules = {
        "atlas_core.actor",
        "atlas_core.ai_model",
        "atlas_core.artifact",
        "atlas_core.configuration_specification",
        "atlas_core.evidence",
        "atlas_core.execution_specification",
        "atlas_core.external_run",
        "atlas_core.observation",
        "atlas_core.prompt_specification",
        "atlas_core.provenance",
        "atlas_core.source",
    }

    assert imported_modules.isdisjoint(prohibited_modules)

    for module_name in imported_modules:
        assert module_name in {"__future__", "dataclasses", "datetime"}


# --- Required strings: external_resource_id, external_resource_kind ---


@pytest.mark.parametrize(
    "field_name",
    ("external_resource_id", "external_resource_kind"),
)
@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        " ",
        " leading",
        "trailing ",
    ),
)
def test_required_strings_reject_invalid_values(
    field_name: str,
    invalid_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(ValueError):
        ExternalResource(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("external_resource_id", "external_resource_kind"),
)
@pytest.mark.parametrize("invalid_value", (123, None, [], {}))
def test_required_strings_reject_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        ExternalResource(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("external_resource_id", "external_resource_kind"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        ExternalResource(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("external_resource_id", "external_resource_kind"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    external_resource = ExternalResource(**arguments)

    assert getattr(external_resource, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_kind = " object"

    arguments = _valid_arguments()
    arguments["external_resource_kind"] = original_kind

    with pytest.raises(ValueError):
        ExternalResource(**arguments)

    assert arguments["external_resource_kind"] == original_kind


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.external_resource as external_resource_module

    source = inspect.getsource(external_resource_module)

    assert "object.__setattr__" not in source


# --- Optional external_identifier and resource_locator ---


@pytest.mark.parametrize(
    "field_name",
    ("external_identifier", "resource_locator"),
)
def test_optional_string_omitted_defaults_to_none(field_name: str) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    external_resource = ExternalResource(**arguments)

    assert getattr(external_resource, field_name) is None


@pytest.mark.parametrize(
    "field_name",
    ("external_identifier", "resource_locator"),
)
def test_optional_string_explicit_none_is_accepted(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = None

    external_resource = ExternalResource(**arguments)

    assert getattr(external_resource, field_name) is None


@pytest.mark.parametrize(
    "field_name",
    ("external_identifier", "resource_locator"),
)
@pytest.mark.parametrize("invalid_value", (123, [], {}))
def test_optional_string_rejects_non_none_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        ExternalResource(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("external_identifier", "resource_locator"),
)
@pytest.mark.parametrize(
    "invalid_value",
    ("", " ", " leading", "trailing "),
)
def test_optional_string_rejects_invalid_string_values(
    field_name: str,
    invalid_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(ValueError):
        ExternalResource(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("external_identifier", "resource_locator"),
)
def test_optional_string_preserves_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    external_resource = ExternalResource(**arguments)

    assert getattr(external_resource, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


@pytest.mark.parametrize(
    "field_name",
    ("external_identifier", "resource_locator"),
)
def test_optional_string_is_not_normalized(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "MixedCase-Value_123"

    external_resource = ExternalResource(**arguments)

    assert getattr(external_resource, field_name) == "MixedCase-Value_123"


# --- Optional field combinations ---


def test_both_optional_fields_omitted() -> None:
    arguments = _valid_arguments()
    del arguments["external_identifier"]
    del arguments["resource_locator"]

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier is None
    assert external_resource.resource_locator is None


def test_both_optional_fields_explicit_none() -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = None
    arguments["resource_locator"] = None

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier is None
    assert external_resource.resource_locator is None


def test_identifier_present_locator_none() -> None:
    arguments = _valid_arguments()
    arguments["resource_locator"] = None

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier == "abc123"
    assert external_resource.resource_locator is None


def test_locator_present_identifier_none() -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = None

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier is None
    assert external_resource.resource_locator == (
        "https://example.invalid/resource/abc123"
    )


def test_both_optional_fields_present() -> None:
    external_resource = ExternalResource(**_valid_arguments())

    assert external_resource.external_identifier == "abc123"
    assert external_resource.resource_locator == (
        "https://example.invalid/resource/abc123"
    )


def test_same_string_in_both_optional_fields_is_technically_constructible() -> None:
    # This confirms only that the dataclass has no cross-field parser
    # or policy enforcement between external_identifier and
    # resource_locator — it is NOT a recommendation to store the same
    # value in both fields for any real resource (e.g. a YouTube video
    # ID vs. its URL remain semantically distinct, ACR-013 §9).
    arguments = _valid_arguments()
    shared_value = "shared-opaque-value"
    arguments["external_identifier"] = shared_value
    arguments["resource_locator"] = shared_value

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier == shared_value
    assert external_resource.resource_locator == shared_value


def test_no_mandatory_identifier() -> None:
    arguments = _valid_arguments()
    del arguments["external_identifier"]

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier is None


def test_no_mandatory_locator() -> None:
    arguments = _valid_arguments()
    del arguments["resource_locator"]

    external_resource = ExternalResource(**arguments)

    assert external_resource.resource_locator is None


def test_no_distinctness_invariant_between_identifier_and_locator() -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = "same-value"
    arguments["resource_locator"] = "same-value"

    # Must not raise: no cross-field distinctness is enforced.
    ExternalResource(**arguments)


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    external_resource = ExternalResource(**arguments)

    assert external_resource.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    non_utc = datetime(2026, 8, 5, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    external_resource = ExternalResource(**arguments)

    assert external_resource.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 5, 10)

    with pytest.raises(ValueError):
        ExternalResource(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-05T10:00:00Z"

    with pytest.raises(TypeError):
        ExternalResource(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        ExternalResource(**arguments)


# --- external_resource_kind: external resource architecture axis only ---


@pytest.mark.parametrize(
    "recommended_kind",
    (
        "object",
        "account",
        "document",
        "file",
        "record",
        "collection",
        "dataset",
        "message",
        "model",
        "deployment",
        "unknown",
    ),
)
def test_recommended_external_resource_kind_values_are_accepted(
    recommended_kind: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_resource_kind"] = recommended_kind

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_kind == recommended_kind


def test_custom_external_resource_architecture_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["external_resource_kind"] = "custom_external_resource_architecture"

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_kind == (
        "custom_external_resource_architecture"
    )


def test_external_resource_kind_is_not_a_closed_enum() -> None:
    arguments = _valid_arguments()
    arguments["external_resource_kind"] = "domain_local_experimental_kind"

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_kind == "domain_local_experimental_kind"


@pytest.mark.parametrize(
    "excluded_media_content_value",
    ("article", "image", "video", "audio", "post"),
)
def test_excluded_media_content_strings_remain_technically_constructible(
    excluded_media_content_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_resource_kind"] = excluded_media_content_value

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_kind == excluded_media_content_value


@pytest.mark.parametrize(
    "excluded_domain_semantic_value",
    ("listing", "shop", "channel", "series", "price_bar", "instrument"),
)
def test_excluded_domain_semantic_strings_remain_technically_constructible(
    excluded_domain_semantic_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_resource_kind"] = excluded_domain_semantic_value

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_kind == excluded_domain_semantic_value


@pytest.mark.parametrize(
    "excluded_provider_specific_value",
    ("tweet", "youtube_video", "etsy_listing", "fred_series"),
)
def test_excluded_provider_specific_strings_remain_technically_constructible(
    excluded_provider_specific_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["external_resource_kind"] = excluded_provider_specific_value

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_kind == (
        excluded_provider_specific_value
    )


# --- external_identifier opaque preservation ---


@pytest.mark.parametrize(
    "identifier_value",
    (
        "123456789",
        "01HZY3K9G8N7Q2R5T6V8W0X1Y2",
        "id-with-punctuation!_.~",
        "MixedCaseID",
        "Ünïcödé-ïd",
        "https://example.invalid/object/123",
        "provider-prefix:composite-value-001",
    ),
)
def test_external_identifier_preserves_opaque_values(identifier_value: str) -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = identifier_value

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier == identifier_value


def test_external_identifier_has_no_prefix_addition() -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = "raw-id-001"

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier == "raw-id-001"


def test_duplicate_external_identifier_permitted_across_distinct_records() -> None:
    # ACR-013 §36 Risk 2/§9: identifier reuse and cross-provider
    # collision are named, unresolved v0.1 risks — Core performs no
    # uniqueness enforcement and no automatic deduplication.
    arguments_a = _valid_arguments()
    arguments_a["external_resource_id"] = "external-resource:a"
    arguments_a["external_identifier"] = "shared-id-123"

    arguments_b = _valid_arguments()
    arguments_b["external_resource_id"] = "external-resource:b"
    arguments_b["external_identifier"] = "shared-id-123"

    external_resource_a = ExternalResource(**arguments_a)
    external_resource_b = ExternalResource(**arguments_b)

    assert (
        external_resource_a.external_identifier
        == external_resource_b.external_identifier
    )
    assert (
        external_resource_a.external_resource_id
        != external_resource_b.external_resource_id
    )


def test_frozen_dataclass_equality_is_ordinary_value_equality() -> None:
    arguments = _valid_arguments()

    first = ExternalResource(**arguments)
    second = ExternalResource(**arguments)

    assert first == second
    assert first is not second


# --- resource_locator opaque preservation ---


@pytest.mark.parametrize(
    "locator_value",
    (
        "https://example.invalid/resource/123",
        "/api/v1/objects/123",
        "opaque-locator-value",
    ),
)
def test_resource_locator_preserves_opaque_values(locator_value: str) -> None:
    arguments = _valid_arguments()
    arguments["resource_locator"] = locator_value

    external_resource = ExternalResource(**arguments)

    assert external_resource.resource_locator == locator_value


def test_resource_locator_is_not_parsed_or_normalized() -> None:
    arguments = _valid_arguments()
    arguments["resource_locator"] = "HTTPS://EXAMPLE.INVALID/Resource/ABC"

    external_resource = ExternalResource(**arguments)

    assert external_resource.resource_locator == "HTTPS://EXAMPLE.INVALID/Resource/ABC"


def test_same_locator_permitted_across_distinct_records() -> None:
    arguments_a = _valid_arguments()
    arguments_a["external_resource_id"] = "external-resource:a"
    arguments_a["resource_locator"] = "https://example.invalid/shared"

    arguments_b = _valid_arguments()
    arguments_b["external_resource_id"] = "external-resource:b"
    arguments_b["resource_locator"] = "https://example.invalid/shared"

    external_resource_a = ExternalResource(**arguments_a)
    external_resource_b = ExternalResource(**arguments_b)

    assert (
        external_resource_a.resource_locator == external_resource_b.resource_locator
    )
    assert (
        external_resource_a.external_resource_id
        != external_resource_b.external_resource_id
    )


def test_historical_locator_value_preserved_exactly() -> None:
    arguments = _valid_arguments()
    arguments["resource_locator"] = "https://example.invalid/moved-since/original"

    external_resource = ExternalResource(**arguments)

    assert external_resource.resource_locator == (
        "https://example.invalid/moved-since/original"
    )


# --- URL classification boundary (structural behavior only) ---


def test_url_shaped_value_technically_accepted_as_identifier() -> None:
    # Structural behavior only. Whether a URL is the correct value for
    # external_identifier versus resource_locator is a semantic
    # admission decision (ACR-013 §9), not something the dataclass
    # decides or enforces.
    arguments = _valid_arguments()
    arguments["external_identifier"] = "https://example.invalid/object/123"

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier == (
        "https://example.invalid/object/123"
    )


def test_url_shaped_value_technically_accepted_as_locator() -> None:
    arguments = _valid_arguments()
    arguments["resource_locator"] = "https://example.invalid/object/123"

    external_resource = ExternalResource(**arguments)

    assert external_resource.resource_locator == "https://example.invalid/object/123"


def test_non_url_value_technically_accepted_as_identifier() -> None:
    arguments = _valid_arguments()
    arguments["external_identifier"] = "plain-opaque-id"

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_identifier == "plain-opaque-id"


# --- Known, Known-without-optionals, Unknown examples ---


def test_known_external_resource_with_both_optionals_example() -> None:
    external_resource = ExternalResource(
        external_resource_id="external-resource:youtube-video-001",
        external_resource_kind="object",
        external_identifier="dQw4w9WgXcQ",
        resource_locator="https://youtube.example.invalid/watch?v=dQw4w9WgXcQ",
        recorded_at=_aware_datetime(),
    )

    assert external_resource.external_identifier == "dQw4w9WgXcQ"
    assert external_resource.resource_locator == (
        "https://youtube.example.invalid/watch?v=dQw4w9WgXcQ"
    )


def test_known_external_resource_with_identifier_only_example() -> None:
    external_resource = ExternalResource(
        external_resource_id="external-resource:etsy-listing-001",
        external_resource_kind="object",
        external_identifier="1234567890",
        recorded_at=_aware_datetime(),
    )

    assert external_resource.external_identifier == "1234567890"
    assert external_resource.resource_locator is None


def test_known_external_resource_with_locator_only_example() -> None:
    external_resource = ExternalResource(
        external_resource_id="external-resource:article-001",
        external_resource_kind="document",
        resource_locator="https://news.example.invalid/article/001",
        recorded_at=_aware_datetime(),
    )

    assert external_resource.external_identifier is None
    assert external_resource.resource_locator == (
        "https://news.example.invalid/article/001"
    )


def test_confidential_style_identity_only_known_example() -> None:
    # ACR-013 §14/§33: a confidential account may still be a valid
    # Known External Resource with both optional fields None.
    external_resource = ExternalResource(
        external_resource_id="external-resource:confidential-account-001",
        external_resource_kind="account",
        recorded_at=_aware_datetime(),
    )

    assert external_resource.external_identifier is None
    assert external_resource.resource_locator is None


def test_unknown_external_resource_is_accepted_as_complete_record() -> None:
    external_resource = ExternalResource(
        external_resource_id="external-resource:unknown:3e9b7f1a5c82",
        external_resource_kind="unknown",
        recorded_at=_aware_datetime(),
    )

    assert external_resource.external_resource_kind == "unknown"
    assert external_resource.external_identifier is None
    assert external_resource.resource_locator is None


def test_unknown_external_resource_may_carry_confirmed_identifier_or_locator() -> (
    None
):
    # An Unknown record MAY carry an identifier and/or locator if
    # confirmed applicable — this is a semantic admission judgment,
    # not a runtime constraint; Core accepts either shape.
    external_resource = ExternalResource(
        external_resource_id="external-resource:unknown:8a1d4e7c9f02",
        external_resource_kind="unknown",
        external_identifier="op-8a1d4e7c9f02",
        recorded_at=_aware_datetime(),
    )

    assert external_resource.external_identifier == "op-8a1d4e7c9f02"


def test_arbitrary_opaque_external_resource_id_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["external_resource_id"] = "01HZY3K9G8N7Q2R5T6V8W0X1Y2"

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_id == "01HZY3K9G8N7Q2R5T6V8W0X1Y2"


def test_no_required_id_prefix_is_enforced() -> None:
    arguments = _valid_arguments()
    arguments["external_resource_id"] = "just-any-non-empty-string"

    external_resource = ExternalResource(**arguments)

    assert external_resource.external_resource_id == "just-any-non-empty-string"


def test_separate_ids_remain_separate_records() -> None:
    arguments_a = _valid_arguments()
    arguments_a["external_resource_id"] = "external-resource:a"

    arguments_b = _valid_arguments()
    arguments_b["external_resource_id"] = "external-resource:b"

    external_resource_a = ExternalResource(**arguments_a)
    external_resource_b = ExternalResource(**arguments_b)

    assert external_resource_a != external_resource_b


# --- Prohibited fields ---


def test_external_resource_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(ExternalResource)}

    prohibited_fields = {
        # Naming and mutable description
        "canonical_name",
        "name",
        "title",
        "display_name",
        "username",
        "handle",
        "slug",
        "description",
        # Source / Provider / ownership relationships
        "source_ref",
        "provider_ref",
        "external_system_ref",
        "owner_ref",
        "actor_ref",
        # Mutable state and lifecycle
        "status",
        "availability",
        "price",
        "metrics",
        "view_count",
        "like_count",
        "follower_count",
        "created_at",
        "published_at",
        "updated_at",
        "deleted_at",
        "expired_at",
        "last_seen_at",
        "restored_at",
        # Artifact / execution relationships
        "artifact_ref",
        "artifact_refs",
        "external_run_ref",
        "external_run_refs",
        "provenance_ref",
        "provenance_refs",
        # Hierarchy / revision / resolution
        "parent_resource_ref",
        "collection_members",
        "version",
        "revision",
        "revision_id",
        "supersedes_ref",
        "redirects_to_ref",
        "equivalent_to_ref",
        "duplicate_of_ref",
        "resolved_ref",
        # Unbounded or sensitive content
        "metadata",
        "raw_payload",
        "request_payload",
        "response_payload",
        "content",
        "api_key",
        "access_token",
        "credential",
        "secret",
        "authorization_header",
        "session_id",
        "email",
        "phone",
        "personal_information",
        # Locator variants
        "canonical_locator",
        "current_locator",
        "url",
        "uri",
        "file_path",
        "storage_key",
        "signed_url",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Provenance compatibility ---


def _valid_provenance_arguments(input_refs: tuple[str, ...]) -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-external-resource-001",
        "activity_kind": "fetch",
        "actor_ref": "actor:atlas:retrieval-service",
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
        "input_refs": input_refs,
    }


def test_external_resource_id_can_be_passed_to_provenance_input_refs() -> None:
    external_resource = ExternalResource(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments((external_resource.external_resource_id,))
    )

    assert provenance.input_refs == (external_resource.external_resource_id,)


def test_provenance_input_refs_accepts_empty_tuple() -> None:
    provenance = Provenance(**_valid_provenance_arguments(()))

    assert provenance.input_refs == ()


def test_provenance_input_refs_accepts_multiple_external_resource_ids() -> None:
    provenance = Provenance(
        **_valid_provenance_arguments(
            ("external-resource:a", "external-resource:b")
        )
    )

    assert provenance.input_refs == ("external-resource:a", "external-resource:b")


def test_provenance_input_refs_accepts_external_resource_and_artifact_ids_together() -> (
    None
):
    external_resource = ExternalResource(**_valid_arguments())
    artifact = Artifact(
        artifact_id="artifact-001",
        artifact_kind="document",
        recorded_at=_aware_datetime(),
    )

    provenance = Provenance(
        **_valid_provenance_arguments(
            (external_resource.external_resource_id, artifact.artifact_id)
        )
    )

    assert provenance.input_refs == (
        external_resource.external_resource_id,
        artifact.artifact_id,
    )


def test_provenance_input_refs_duplicate_rejection_is_preserved() -> None:
    with pytest.raises(ValueError):
        Provenance(
            **_valid_provenance_arguments(
                ("external-resource:dup", "external-resource:dup")
            )
        )


def test_provenance_holds_id_string_not_external_resource_object() -> None:
    external_resource = ExternalResource(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments((external_resource.external_resource_id,))
    )

    for reference in provenance.input_refs:
        assert isinstance(reference, str)
        assert not isinstance(reference, ExternalResource)


def test_external_resource_has_no_reverse_provenance_reference() -> None:
    field_names = {field.name for field in fields(ExternalResource)}

    assert "provenance_id" not in field_names
    assert "provenance_ref" not in field_names
    assert "provenance_refs" not in field_names


def test_provenance_retains_exact_approved_thirteen_field_set() -> None:
    field_names = tuple(field.name for field in fields(Provenance))

    assert field_names == (
        "provenance_id",
        "activity_kind",
        "actor_ref",
        "started_at",
        "completed_at",
        "recorded_at",
        "input_refs",
        "parent_provenance_refs",
        "execution_ref",
        "model_ref",
        "prompt_ref",
        "configuration_ref",
        "external_run_ref",
    )
    assert len(field_names) == 13


def test_no_existing_core_model_imports_external_resource() -> None:
    import ast
    import inspect

    import atlas_core.actor as actor_module
    import atlas_core.ai_model as ai_model_module
    import atlas_core.artifact as artifact_module
    import atlas_core.configuration_specification as configuration_specification_module
    import atlas_core.evidence as evidence_module
    import atlas_core.execution_specification as execution_specification_module
    import atlas_core.external_run as external_run_module
    import atlas_core.observation as observation_module
    import atlas_core.prompt_specification as prompt_specification_module
    import atlas_core.provenance as provenance_module
    import atlas_core.source as source_module

    for module in (
        actor_module,
        ai_model_module,
        artifact_module,
        configuration_specification_module,
        evidence_module,
        execution_specification_module,
        external_run_module,
        observation_module,
        prompt_specification_module,
        provenance_module,
        source_module,
    ):
        tree = ast.parse(inspect.getsource(module))
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.add(node.module)

        assert "atlas_core.external_resource" not in imported_modules


# --- Existing-model compatibility ---


def test_artifact_retains_exact_approved_seven_field_set() -> None:
    field_names = tuple(field.name for field in fields(Artifact))

    assert field_names == (
        "artifact_id",
        "artifact_kind",
        "content_digest",
        "digest_algorithm",
        "media_type",
        "artifact_locator",
        "recorded_at",
    )
    assert len(field_names) == 7


def test_source_has_no_external_resource_field() -> None:
    from atlas_core import Source

    field_names = {field.name for field in fields(Source)}

    assert "external_resource_ref" not in field_names
    assert "external_resource_id" not in field_names


def test_actor_has_no_external_resource_field() -> None:
    from atlas_core import Actor

    field_names = {field.name for field in fields(Actor)}

    assert "external_resource_ref" not in field_names
    assert "external_resource_id" not in field_names


def test_resource_locator_is_distinct_field_from_artifact_locator() -> None:
    # ACR-013 §18/§32: resource_locator (live external object) is a
    # deliberately distinct field from Artifact.artifact_locator
    # (Atlas's own captured copy) — both may independently be set.
    field_names = {field.name for field in fields(ExternalResource)}
    artifact_field_names = {field.name for field in fields(Artifact)}

    assert "resource_locator" in field_names
    assert "artifact_locator" not in field_names
    assert "artifact_locator" in artifact_field_names
    assert "resource_locator" not in artifact_field_names


# --- Package export and cross-Concept isolation ---


def test_package_exports_all_twelve_core_models() -> None:
    import atlas_core

    assert set(atlas_core.__all__) == {
        "AIModel",
        "Actor",
        "Artifact",
        "ConfigurationSpecification",
        "Evidence",
        "ExecutionSpecification",
        "ExternalResource",
        "ExternalRun",
        "Observation",
        "PromptSpecification",
        "Provenance",
        "Source",
        "__version__",
    }


def test_package_root_import_succeeds() -> None:
    import atlas_core

    assert atlas_core.ExternalResource is ExternalResource


def test_external_resource_has_no_other_core_model_reference() -> None:
    field_names = {field.name for field in fields(ExternalResource)}

    assert "evidence_id" not in field_names
    assert "evidence_ref" not in field_names
    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "source_id" not in field_names
    assert "source_ref" not in field_names
    assert "actor_id" not in field_names
    assert "model_id" not in field_names
    assert "model_ref" not in field_names
    assert "artifact_id" not in field_names
    assert "external_run_id" not in field_names
    assert "execution_specification_id" not in field_names
    assert "execution_ref" not in field_names
    assert "prompt_specification_id" not in field_names
    assert "prompt_ref" not in field_names
    assert "configuration_specification_id" not in field_names
    assert "configuration_ref" not in field_names
