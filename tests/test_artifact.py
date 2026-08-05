from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from atlas_core import Artifact, Provenance


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 4,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "artifact_id": "artifact:01HZY3K9G8N7Q2R5T6V8W0X1Y2",
        "artifact_kind": "text",
        "content_digest": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        "digest_algorithm": "sha256",
        "media_type": "text/html",
        "artifact_locator": "artifact-store://bucket/2026/08/04/reuters-article.html",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_artifact_can_be_created() -> None:
    arguments = _valid_arguments()

    artifact = Artifact(**arguments)

    assert artifact.artifact_id == "artifact:01HZY3K9G8N7Q2R5T6V8W0X1Y2"
    assert artifact.artifact_kind == "text"
    assert artifact.content_digest == arguments["content_digest"]
    assert artifact.digest_algorithm == "sha256"
    assert artifact.media_type == "text/html"
    assert artifact.artifact_locator == arguments["artifact_locator"]
    assert artifact.recorded_at == arguments["recorded_at"]


def test_artifact_is_exported_from_package_root() -> None:
    from atlas_core.artifact import Artifact as ModuleArtifact

    assert Artifact is ModuleArtifact


def test_artifact_is_immutable() -> None:
    artifact = Artifact(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        artifact.artifact_kind = "changed"  # type: ignore[misc]


def test_artifact_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        Artifact(*arguments.values())  # type: ignore[misc]


def test_artifact_has_slots() -> None:
    artifact = Artifact(**_valid_arguments())

    assert not hasattr(artifact, "__dict__")


def test_artifact_has_exact_approved_field_set_and_order() -> None:
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


def test_artifact_field_count_is_seven() -> None:
    assert len(fields(Artifact)) == 7


def test_three_fields_are_required() -> None:
    required = [
        field
        for field in fields(Artifact)
        if field.default is MISSING and field.default_factory is MISSING  # type: ignore[misc]
    ]
    required_names = {field.name for field in required}

    assert required_names == {"artifact_id", "artifact_kind", "recorded_at"}
    assert len(required) == 3


def test_four_fields_are_optional_with_default_none() -> None:
    optional = [
        field
        for field in fields(Artifact)
        if field.default is not MISSING or field.default_factory is not MISSING  # type: ignore[misc]
    ]
    optional_names = {field.name for field in optional}

    assert optional_names == {
        "content_digest",
        "digest_algorithm",
        "media_type",
        "artifact_locator",
    }
    assert len(optional) == 4
    for field in optional:
        assert field.default is None


def test_artifact_has_no_canonical_name_field() -> None:
    field_names = {field.name for field in fields(Artifact)}

    assert "canonical_name" not in field_names


def test_artifact_has_no_byte_length_field() -> None:
    field_names = {field.name for field in fields(Artifact)}

    assert "byte_length" not in field_names
    assert "size_bytes" not in field_names


def test_artifact_module_imports_only_standard_library() -> None:
    import ast
    import inspect

    import atlas_core.artifact as artifact_module

    source = inspect.getsource(artifact_module)
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


# --- Required strings: artifact_id, artifact_kind ---


@pytest.mark.parametrize(
    "field_name",
    ("artifact_id", "artifact_kind"),
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
        Artifact(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("artifact_id", "artifact_kind"),
)
@pytest.mark.parametrize("invalid_value", (123, None, [], {}))
def test_required_strings_reject_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        Artifact(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("artifact_id", "artifact_kind"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        Artifact(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("artifact_id", "artifact_kind"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    artifact = Artifact(**arguments)

    assert getattr(artifact, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_kind = " text"

    arguments = _valid_arguments()
    arguments["artifact_kind"] = original_kind

    with pytest.raises(ValueError):
        Artifact(**arguments)

    assert arguments["artifact_kind"] == original_kind


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.artifact as artifact_module

    source = inspect.getsource(artifact_module)

    assert "object.__setattr__" not in source


# --- Optional strings: content_digest, digest_algorithm, media_type,
# artifact_locator ---


@pytest.mark.parametrize(
    "field_name",
    ("content_digest", "digest_algorithm", "media_type", "artifact_locator"),
)
def test_optional_string_omitted_defaults_to_none(field_name: str) -> None:
    minimal_arguments = {
        "artifact_id": "artifact:a",
        "artifact_kind": "text",
        "recorded_at": _aware_datetime(),
    }

    artifact = Artifact(**minimal_arguments)

    assert getattr(artifact, field_name) is None


@pytest.mark.parametrize(
    "field_name",
    ("media_type", "artifact_locator"),
)
def test_optional_non_digest_string_explicit_none_is_accepted(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = None

    artifact = Artifact(**arguments)

    assert getattr(artifact, field_name) is None


@pytest.mark.parametrize(
    "field_name",
    ("media_type", "artifact_locator"),
)
@pytest.mark.parametrize("invalid_value", (123, [], {}))
def test_optional_string_rejects_non_none_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        Artifact(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("media_type", "artifact_locator"),
)
@pytest.mark.parametrize(
    "invalid_value",
    ("", " ", " leading", "trailing "),
)
def test_optional_string_rejects_invalid_values(
    field_name: str,
    invalid_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(ValueError):
        Artifact(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("content_digest", "digest_algorithm", "media_type", "artifact_locator"),
)
def test_optional_string_preserves_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    artifact = Artifact(**arguments)

    assert getattr(artifact, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


# --- Digest pair invariant ---


def test_digest_pair_both_omitted_is_accepted() -> None:
    arguments = _valid_arguments()
    del arguments["content_digest"]
    del arguments["digest_algorithm"]

    artifact = Artifact(**arguments)

    assert artifact.content_digest is None
    assert artifact.digest_algorithm is None


def test_digest_pair_both_explicit_none_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = None
    arguments["digest_algorithm"] = None

    artifact = Artifact(**arguments)

    assert artifact.content_digest is None
    assert artifact.digest_algorithm is None


def test_digest_pair_both_present_is_accepted() -> None:
    arguments = _valid_arguments()

    artifact = Artifact(**arguments)

    assert artifact.content_digest is not None
    assert artifact.digest_algorithm is not None


def test_digest_only_without_algorithm_is_rejected() -> None:
    arguments = _valid_arguments()
    arguments["digest_algorithm"] = None

    with pytest.raises(ValueError):
        Artifact(**arguments)


def test_algorithm_only_without_digest_is_rejected() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = None

    with pytest.raises(ValueError):
        Artifact(**arguments)


def test_digest_and_algorithm_exact_values_preserved() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = "abc123"
    arguments["digest_algorithm"] = "custom-algorithm-v1"

    artifact = Artifact(**arguments)

    assert artifact.content_digest == "abc123"
    assert artifact.digest_algorithm == "custom-algorithm-v1"


def test_custom_algorithm_string_is_accepted_no_enum() -> None:
    arguments = _valid_arguments()
    arguments["digest_algorithm"] = "not-a-real-algorithm-name"

    artifact = Artifact(**arguments)

    assert artifact.digest_algorithm == "not-a-real-algorithm-name"


def test_no_digest_format_or_length_enforcement() -> None:
    arguments = _valid_arguments()
    arguments["content_digest"] = "x"
    arguments["digest_algorithm"] = "y"

    artifact = Artifact(**arguments)

    assert artifact.content_digest == "x"
    assert artifact.digest_algorithm == "y"


def test_duplicate_digest_values_allowed_across_distinct_artifact_ids() -> None:
    arguments_a = _valid_arguments()
    arguments_a["artifact_id"] = "artifact:a"

    arguments_b = _valid_arguments()
    arguments_b["artifact_id"] = "artifact:b"
    # Same digest and algorithm as arguments_a.

    artifact_a = Artifact(**arguments_a)
    artifact_b = Artifact(**arguments_b)

    assert artifact_a.content_digest == artifact_b.content_digest
    assert artifact_a.digest_algorithm == artifact_b.digest_algorithm
    assert artifact_a.artifact_id != artifact_b.artifact_id


def test_duplicate_locator_values_allowed_across_distinct_artifact_ids() -> None:
    arguments_a = _valid_arguments()
    arguments_a["artifact_id"] = "artifact:a"

    arguments_b = _valid_arguments()
    arguments_b["artifact_id"] = "artifact:b"
    # Same locator as arguments_a.

    artifact_a = Artifact(**arguments_a)
    artifact_b = Artifact(**arguments_b)

    assert artifact_a.artifact_locator == artifact_b.artifact_locator
    assert artifact_a.artifact_id != artifact_b.artifact_id


def test_frozen_dataclass_equality_is_ordinary_value_equality() -> None:
    arguments = _valid_arguments()

    first = Artifact(**arguments)
    second = Artifact(**arguments)

    assert first == second
    assert first is not second


def test_distinct_byte_revisions_are_separate_records() -> None:
    revision_one = Artifact(
        artifact_id="artifact:article-html-v1",
        artifact_kind="text",
        content_digest="digest-of-original-html",
        digest_algorithm="sha256",
        recorded_at=_aware_datetime(),
    )
    revision_two = Artifact(
        artifact_id="artifact:article-html-v1-corrected",
        artifact_kind="text",
        content_digest="digest-of-corrected-html",
        digest_algorithm="sha256",
        recorded_at=_aware_datetime(),
    )

    # No field links the two records — a materially distinct byte
    # representation is a wholly new, independent identity.
    assert revision_one.artifact_id != revision_two.artifact_id
    assert revision_one.content_digest != revision_two.content_digest


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    artifact = Artifact(**arguments)

    assert artifact.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    non_utc = datetime(2026, 8, 4, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    artifact = Artifact(**arguments)

    assert artifact.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 4, 10)

    with pytest.raises(ValueError):
        Artifact(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-04T10:00:00Z"

    with pytest.raises(TypeError):
        Artifact(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        Artifact(**arguments)


# --- artifact_kind: representation architecture axis only ---


@pytest.mark.parametrize(
    "recommended_kind",
    ("text", "binary", "structured", "collection", "unknown"),
)
def test_recommended_artifact_kind_values_are_accepted(
    recommended_kind: str,
) -> None:
    arguments = _valid_arguments()
    arguments["artifact_kind"] = recommended_kind

    artifact = Artifact(**arguments)

    assert artifact.artifact_kind == recommended_kind


def test_custom_representation_architecture_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["artifact_kind"] = "custom_representation_architecture"

    artifact = Artifact(**arguments)

    assert artifact.artifact_kind == "custom_representation_architecture"


def test_artifact_kind_is_not_a_closed_enum() -> None:
    arguments = _valid_arguments()
    arguments["artifact_kind"] = "domain_local_experimental_kind"

    artifact = Artifact(**arguments)

    assert artifact.artifact_kind == "domain_local_experimental_kind"


@pytest.mark.parametrize(
    "excluded_media_family_value",
    ("document", "image", "video", "audio", "archive", "dataset"),
)
def test_excluded_media_family_strings_remain_technically_constructible(
    excluded_media_family_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["artifact_kind"] = excluded_media_family_value

    artifact = Artifact(**arguments)

    assert artifact.artifact_kind == excluded_media_family_value


@pytest.mark.parametrize(
    "excluded_purpose_value",
    (
        "prompt",
        "configuration",
        "request",
        "response",
        "report",
        "transcript",
        "log",
    ),
)
def test_excluded_semantic_purpose_strings_remain_technically_constructible(
    excluded_purpose_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["artifact_kind"] = excluded_purpose_value

    artifact = Artifact(**arguments)

    assert artifact.artifact_kind == excluded_purpose_value


@pytest.mark.parametrize(
    "excluded_format_value",
    ("json", "csv", "markdown", "html", "pdf", "png", "jpeg", "mp4"),
)
def test_excluded_storage_format_strings_remain_technically_constructible(
    excluded_format_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["artifact_kind"] = excluded_format_value

    artifact = Artifact(**arguments)

    assert artifact.artifact_kind == excluded_format_value


# --- Known, minimal, confidential, Unknown patterns ---


def test_minimal_known_artifact_with_all_optional_fields_none() -> None:
    artifact = Artifact(
        artifact_id="artifact:minimal-001",
        artifact_kind="text",
        recorded_at=_aware_datetime(),
    )

    assert artifact.content_digest is None
    assert artifact.digest_algorithm is None
    assert artifact.media_type is None
    assert artifact.artifact_locator is None


def test_known_artifact_with_digest_pair_only() -> None:
    artifact = Artifact(
        artifact_id="artifact:digest-only-001",
        artifact_kind="structured",
        content_digest="digest-value",
        digest_algorithm="sha256",
        recorded_at=_aware_datetime(),
    )

    assert artifact.content_digest == "digest-value"
    assert artifact.artifact_locator is None
    assert artifact.media_type is None


def test_known_artifact_with_locator_only() -> None:
    artifact = Artifact(
        artifact_id="artifact:locator-only-001",
        artifact_kind="binary",
        artifact_locator="artifact-store://bucket/key",
        recorded_at=_aware_datetime(),
    )

    assert artifact.artifact_locator == "artifact-store://bucket/key"
    assert artifact.content_digest is None
    assert artifact.digest_algorithm is None


def test_known_artifact_with_media_type_only() -> None:
    artifact = Artifact(
        artifact_id="artifact:media-type-only-001",
        artifact_kind="text",
        media_type="application/json",
        recorded_at=_aware_datetime(),
    )

    assert artifact.media_type == "application/json"
    assert artifact.content_digest is None
    assert artifact.artifact_locator is None


def test_known_artifact_with_all_optional_fields_present() -> None:
    artifact = Artifact(**_valid_arguments())

    assert artifact.content_digest is not None
    assert artifact.digest_algorithm is not None
    assert artifact.media_type is not None
    assert artifact.artifact_locator is not None


def test_confidential_style_minimal_known_artifact() -> None:
    # ACR-012 §22.1/§23: a confidential Artifact may be Known with
    # every optional field absent — no canonical_name exists to
    # sanitize, since this Concept has none.
    artifact = Artifact(
        artifact_id="artifact:confidential:9d4e2f8a1c73",
        artifact_kind="binary",
        recorded_at=_aware_datetime(),
    )

    assert artifact.content_digest is None
    assert artifact.digest_algorithm is None
    assert artifact.media_type is None
    assert artifact.artifact_locator is None


def test_unknown_style_artifact_with_kind_unknown() -> None:
    artifact = Artifact(
        artifact_id="artifact:unknown:3e9b7f1a5c82",
        artifact_kind="unknown",
        recorded_at=_aware_datetime(),
    )

    assert artifact.artifact_kind == "unknown"


def test_unknown_style_artifact_with_all_optional_fields_none() -> None:
    artifact = Artifact(
        artifact_id="artifact:unknown:8a1d4e7c9f02",
        artifact_kind="unknown",
        recorded_at=_aware_datetime(),
    )

    assert artifact.content_digest is None
    assert artifact.digest_algorithm is None
    assert artifact.media_type is None
    assert artifact.artifact_locator is None


def test_empty_identifiers_remain_rejected_for_unknown_style_records() -> None:
    arguments = _valid_arguments()
    arguments["artifact_kind"] = "unknown"
    arguments["artifact_id"] = ""

    with pytest.raises(ValueError):
        Artifact(**arguments)


def test_no_cross_field_requirement_that_digest_locator_or_media_type_exist() -> (
    None
):
    # A bare identity-only record (artifact_id/artifact_kind/
    # recorded_at) is fully valid — no combination of digest, locator,
    # or media_type is ever required.
    artifact = Artifact(
        artifact_id="artifact:bare-001",
        artifact_kind="text",
        recorded_at=_aware_datetime(),
    )

    assert artifact.artifact_id == "artifact:bare-001"


# --- Representation identity / no automatic merge ---


def test_no_required_id_prefix_is_enforced() -> None:
    arguments = _valid_arguments()
    arguments["artifact_id"] = "just-any-non-empty-string"

    artifact = Artifact(**arguments)

    assert artifact.artifact_id == "just-any-non-empty-string"


def test_arbitrary_opaque_artifact_id_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["artifact_id"] = "01HZY3K9G8N7Q2R5T6V8W0X1Y2"

    artifact = Artifact(**arguments)

    assert artifact.artifact_id == "01HZY3K9G8N7Q2R5T6V8W0X1Y2"


# --- Prohibited fields ---


def test_artifact_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(Artifact)}

    prohibited_fields = {
        # Naming / revision
        "canonical_name",
        "version",
        "revision",
        # Size / encoding (Deferred)
        "byte_length",
        "size_bytes",
        "encoding",
        # Raw content
        "content",
        "text_content",
        "binary_content",
        "structured_content",
        "bytes",
        "payload",
        "raw_payload",
        "request_payload",
        "response_payload",
        "base64",
        "arbitrary_json",
        # Time / lifecycle
        "created_at",
        "captured_at",
        "produced_at",
        "modified_at",
        "retrieved_at",
        "updated_at",
        "deleted_at",
        "expired_at",
        "retention_until",
        "status",
        "availability",
        # Relationships
        "source_ref",
        "external_resource_ref",
        "produced_by_provenance_ref",
        "input_provenance_refs",
        "output_provenance_refs",
        "parent_artifact_ref",
        "collection_members",
        "schema_ref",
        "evidence_refs",
        "observation_refs",
        # Storage variants (folded into artifact_locator)
        "uri",
        "file_path",
        "storage_key",
        "signed_url",
        # Security / metadata
        "confidentiality",
        "retention",
        "metadata",
        "secret",
        "credential",
        "api_key",
        "access_token",
        "authorization_header",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Provenance compatibility ---


def _valid_provenance_arguments(input_refs: tuple[str, ...]) -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-artifact-001",
        "activity_kind": "extract",
        "actor_ref": "actor:atlas:extraction-service",
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
        "input_refs": input_refs,
    }


def test_artifact_id_can_be_included_in_provenance_input_refs() -> None:
    artifact = Artifact(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments((artifact.artifact_id,))
    )

    assert artifact.artifact_id in provenance.input_refs


def test_multiple_artifact_ids_accepted_in_input_refs() -> None:
    artifact_a = Artifact(
        artifact_id="artifact:a",
        artifact_kind="text",
        recorded_at=_aware_datetime(),
    )
    artifact_b = Artifact(
        artifact_id="artifact:b",
        artifact_kind="text",
        recorded_at=_aware_datetime(),
    )

    provenance = Provenance(
        **_valid_provenance_arguments(
            (artifact_a.artifact_id, artifact_b.artifact_id)
        )
    )

    assert provenance.input_refs == (artifact_a.artifact_id, artifact_b.artifact_id)


def test_empty_input_refs_tuple_remains_accepted() -> None:
    provenance = Provenance(**_valid_provenance_arguments(()))

    assert provenance.input_refs == ()


def test_duplicate_input_refs_remain_rejected_by_existing_provenance_validation() -> (
    None
):
    artifact = Artifact(**_valid_arguments())

    with pytest.raises(ValueError):
        Provenance(
            **_valid_provenance_arguments(
                (artifact.artifact_id, artifact.artifact_id)
            )
        )


def test_provenance_holds_id_strings_not_artifact_objects() -> None:
    artifact = Artifact(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments((artifact.artifact_id,))
    )

    for ref in provenance.input_refs:
        assert isinstance(ref, str)
        assert not isinstance(ref, Artifact)


def test_artifact_has_no_reverse_provenance_reference() -> None:
    field_names = {field.name for field in fields(Artifact)}

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


def test_provenance_input_refs_field_type_and_default_unchanged() -> None:
    input_refs_field = next(
        f for f in fields(Provenance) if f.name == "input_refs"
    )

    assert input_refs_field.type == "tuple[str, ...]"
    assert input_refs_field.default == ()


# --- Evidence compatibility ---


def test_evidence_exact_structure_unchanged() -> None:
    from atlas_core import Evidence

    field_names = tuple(field.name for field in fields(Evidence))

    assert field_names == (
        "evidence_id",
        "evidence_kind",
        "source_ref",
        "artifact_locator",
        "provenance_ref",
        "captured_at",
        "recorded_at",
        "content_selector",
        "media_type",
        "content_digest",
        "digest_algorithm",
        "byte_length",
        "source_published_at",
    )


def test_evidence_retains_artifact_locator_field() -> None:
    from atlas_core import Evidence

    field_names = {field.name for field in fields(Evidence)}

    assert "artifact_locator" in field_names


def test_evidence_has_no_artifact_ref_field() -> None:
    from atlas_core import Evidence

    field_names = {field.name for field in fields(Evidence)}

    assert "artifact_ref" not in field_names


def test_no_evidence_artifact_circular_import() -> None:
    import ast
    import inspect

    import atlas_core.evidence as evidence_module

    tree = ast.parse(inspect.getsource(evidence_module))
    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.add(node.module)

    assert "atlas_core.artifact" not in imported_modules


# --- Package export and cross-Concept isolation ---


def test_package_exports_all_eleven_core_models() -> None:
    import atlas_core

    assert set(atlas_core.__all__) == {
        "AIModel",
        "Actor",
        "Artifact",
        "ConfigurationSpecification",
        "Evidence",
        "ExecutionSpecification",
        "ExternalRun",
        "Observation",
        "PromptSpecification",
        "Provenance",
        "Source",
        "__version__",
    }


def test_package_root_import_succeeds() -> None:
    import atlas_core

    assert atlas_core.Artifact is Artifact


def test_artifact_has_no_other_core_model_reference() -> None:
    field_names = {field.name for field in fields(Artifact)}

    assert "evidence_id" not in field_names
    assert "evidence_ref" not in field_names
    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "source_id" not in field_names
    assert "actor_id" not in field_names
    assert "actor_ref" not in field_names
    assert "model_id" not in field_names
    assert "model_ref" not in field_names
    assert "execution_specification_id" not in field_names
    assert "execution_ref" not in field_names
    assert "prompt_specification_id" not in field_names
    assert "prompt_ref" not in field_names
    assert "configuration_specification_id" not in field_names
    assert "configuration_ref" not in field_names
    assert "external_run_id" not in field_names
    assert "external_run_ref" not in field_names


def test_no_existing_core_model_imports_artifact() -> None:
    import ast
    import inspect

    import atlas_core.actor as actor_module
    import atlas_core.ai_model as ai_model_module
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

        assert "atlas_core.artifact" not in imported_modules
