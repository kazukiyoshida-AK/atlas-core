from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from atlas_core import ConfigurationSpecification, Provenance


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 4,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "configuration_specification_id": (
            "config-spec:summarizer-generation-params-v1"
        ),
        "configuration_kind": "parameter_profile",
        "canonical_name": "Summarizer Generation Parameters gen-params-v1",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_configuration_specification_can_be_created() -> None:
    arguments = _valid_arguments()

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.configuration_specification_id == (
        "config-spec:summarizer-generation-params-v1"
    )
    assert configuration_specification.configuration_kind == "parameter_profile"
    assert configuration_specification.canonical_name == (
        "Summarizer Generation Parameters gen-params-v1"
    )
    assert configuration_specification.recorded_at == arguments["recorded_at"]


def test_configuration_specification_is_exported_from_package_root() -> None:
    from atlas_core.configuration_specification import (
        ConfigurationSpecification as ModuleConfigurationSpecification,
    )

    assert ConfigurationSpecification is ModuleConfigurationSpecification


def test_configuration_specification_is_immutable() -> None:
    configuration_specification = ConfigurationSpecification(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        configuration_specification.canonical_name = "changed"  # type: ignore[misc]


def test_configuration_specification_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        ConfigurationSpecification(*arguments.values())  # type: ignore[misc]


def test_configuration_specification_has_slots() -> None:
    configuration_specification = ConfigurationSpecification(**_valid_arguments())

    assert not hasattr(configuration_specification, "__dict__")


def test_configuration_specification_has_exact_approved_field_set_and_order() -> (
    None
):
    field_names = tuple(field.name for field in fields(ConfigurationSpecification))

    assert field_names == (
        "configuration_specification_id",
        "configuration_kind",
        "canonical_name",
        "recorded_at",
    )


def test_configuration_specification_field_count_is_four() -> None:
    assert len(fields(ConfigurationSpecification)) == 4


def test_all_fields_are_required() -> None:
    for field in fields(ConfigurationSpecification):
        assert field.default is MISSING
        assert field.default_factory is MISSING  # type: ignore[misc]


def test_configuration_specification_module_imports_only_standard_library() -> (
    None
):
    import ast
    import inspect

    import atlas_core.configuration_specification as configuration_specification_module

    source = inspect.getsource(configuration_specification_module)
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
        "atlas_core.evidence",
        "atlas_core.execution_specification",
        "atlas_core.observation",
        "atlas_core.prompt_specification",
        "atlas_core.provenance",
        "atlas_core.source",
    }

    assert imported_modules.isdisjoint(prohibited_modules)

    for module_name in imported_modules:
        assert module_name in {"__future__", "dataclasses", "datetime"}


# --- Required strings ---


@pytest.mark.parametrize(
    "field_name",
    ("configuration_specification_id", "configuration_kind", "canonical_name"),
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
        ConfigurationSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("configuration_specification_id", "configuration_kind", "canonical_name"),
)
@pytest.mark.parametrize("invalid_value", (123, None, [], {}))
def test_required_strings_reject_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        ConfigurationSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("configuration_specification_id", "configuration_kind", "canonical_name"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        ConfigurationSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("configuration_specification_id", "configuration_kind", "canonical_name"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    configuration_specification = ConfigurationSpecification(**arguments)

    assert getattr(configuration_specification, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_canonical_name = " Summarizer Generation Parameters gen-params-v1"

    arguments = _valid_arguments()
    arguments["canonical_name"] = original_canonical_name

    with pytest.raises(ValueError):
        ConfigurationSpecification(**arguments)

    assert arguments["canonical_name"] == original_canonical_name


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.configuration_specification as configuration_specification_module

    source = inspect.getsource(configuration_specification_module)

    assert "object.__setattr__" not in source


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    non_utc = datetime(2026, 8, 4, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 4, 10)

    with pytest.raises(ValueError):
        ConfigurationSpecification(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-04T10:00:00Z"

    with pytest.raises(TypeError):
        ConfigurationSpecification(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        ConfigurationSpecification(**arguments)


# --- configuration_kind: structural axis only, extensible, no closed enum ---


@pytest.mark.parametrize(
    "recommended_kind",
    (
        "parameter_profile",
        "settings_bundle",
        "policy_profile",
        "feature_flag_set",
        "unknown",
    ),
)
def test_recommended_configuration_kind_values_are_accepted(
    recommended_kind: str,
) -> None:
    arguments = _valid_arguments()
    arguments["configuration_kind"] = recommended_kind

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.configuration_kind == recommended_kind


def test_custom_structural_configuration_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["configuration_kind"] = "custom_structural_kind"

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.configuration_kind == (
        "custom_structural_kind"
    )


def test_configuration_kind_is_not_a_closed_enum() -> None:
    arguments = _valid_arguments()
    arguments["configuration_kind"] = "domain_local_experimental_kind"

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.configuration_kind == (
        "domain_local_experimental_kind"
    )


@pytest.mark.parametrize(
    "functional_purpose_value",
    (
        "model_generation",
        "routing",
        "collection",
        "analysis",
        "publication",
        "retry",
        "timeout",
        "scheduling",
    ),
)
def test_functional_purpose_strings_remain_technically_constructible(
    functional_purpose_value: str,
) -> None:
    # ACR-010: functional purpose is excluded from the RECOMMENDED
    # configuration_kind vocabulary because the field's single axis is
    # structural architecture. Core does not runtime-enforce vocabulary
    # membership, so these strings are not rejected — the exclusion is
    # governance, not validation.
    arguments = _valid_arguments()
    arguments["configuration_kind"] = functional_purpose_value

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.configuration_kind == (
        functional_purpose_value
    )


@pytest.mark.parametrize(
    "source_format_value",
    (
        "environment",
        "json",
        "yaml",
        "toml",
        "command_line",
        "env_file",
        "settings_class",
    ),
)
def test_source_format_strings_remain_technically_constructible(
    source_format_value: str,
) -> None:
    arguments = _valid_arguments()
    arguments["configuration_kind"] = source_format_value

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.configuration_kind == source_format_value


# --- canonical_name / revision-distinguishable identity ---


def test_duplicate_canonical_name_is_permitted_across_distinct_records() -> None:
    arguments_a = _valid_arguments()
    arguments_a["configuration_specification_id"] = "config-spec:a"
    arguments_a["canonical_name"] = "Shared Label"

    arguments_b = _valid_arguments()
    arguments_b["configuration_specification_id"] = "config-spec:b"
    arguments_b["canonical_name"] = "Shared Label"

    configuration_specification_a = ConfigurationSpecification(**arguments_a)
    configuration_specification_b = ConfigurationSpecification(**arguments_b)

    assert (
        configuration_specification_a.canonical_name
        == configuration_specification_b.canonical_name
    )
    assert (
        configuration_specification_a.configuration_specification_id
        != configuration_specification_b.configuration_specification_id
    )


def test_canonical_name_is_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["canonical_name"] = "FRED/TwelveData/NewsAPI Adapter Retry Profile retry-v1"

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.canonical_name == (
        "FRED/TwelveData/NewsAPI Adapter Retry Profile retry-v1"
    )


def test_revision_qualified_canonical_name_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["canonical_name"] = "Summarizer Generation Parameters gen-params-v1"

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.canonical_name == (
        "Summarizer Generation Parameters gen-params-v1"
    )


@pytest.mark.parametrize(
    "mutable_alias",
    ("production", "staging", "default", "current", "latest"),
)
def test_mutable_alias_strings_remain_technically_constructible(
    mutable_alias: str,
) -> None:
    # ACR-010: a mutable alias alone is insufficient for the semantic
    # Known-identity Admission Rule, but that is a governance rule
    # evaluated at minting time, not a Core runtime constraint.
    arguments = _valid_arguments()
    arguments["canonical_name"] = mutable_alias

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.canonical_name == mutable_alias


def test_arbitrary_opaque_configuration_specification_id_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["configuration_specification_id"] = "01HZY3K9G8N7Q2R5T6V8W0X1Y2"

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.configuration_specification_id == (
        "01HZY3K9G8N7Q2R5T6V8W0X1Y2"
    )


def test_no_required_id_prefix_is_enforced() -> None:
    arguments = _valid_arguments()
    arguments["configuration_specification_id"] = "just-any-non-empty-string"

    configuration_specification = ConfigurationSpecification(**arguments)

    assert configuration_specification.configuration_specification_id == (
        "just-any-non-empty-string"
    )


def test_a_materially_revised_profile_is_a_new_independent_record() -> None:
    revision_one = ConfigurationSpecification(
        configuration_specification_id="config-spec:gen-params-v1",
        configuration_kind="parameter_profile",
        canonical_name="Summarizer Generation Parameters gen-params-v1",
        recorded_at=_aware_datetime(),
    )
    revision_two = ConfigurationSpecification(
        configuration_specification_id="config-spec:gen-params-v2",
        configuration_kind="parameter_profile",
        canonical_name="Summarizer Generation Parameters gen-params-v2",
        recorded_at=_aware_datetime(),
    )

    # No field links the two records — a materially revised registered
    # profile definition is an entirely new, independent identity.
    assert revision_one.configuration_specification_id != (
        revision_two.configuration_specification_id
    )
    assert revision_one.canonical_name != revision_two.canonical_name


def test_frozen_dataclass_equality_is_ordinary_value_equality() -> None:
    arguments = _valid_arguments()

    first = ConfigurationSpecification(**arguments)
    second = ConfigurationSpecification(**arguments)

    # Ordinary dataclass value equality only — Core performs no
    # identity-merging, deduplication, or semantic comparison beyond
    # what @dataclass(frozen=True) provides by default.
    assert first == second
    assert first is not second


# --- Known, Confidential Known, Unknown examples ---


def test_known_parameter_profile_example() -> None:
    configuration_specification = ConfigurationSpecification(
        configuration_specification_id="config-spec:retry-profile-v1",
        configuration_kind="parameter_profile",
        canonical_name=(
            "FRED/TwelveData/NewsAPI Adapter Retry Profile retry-v1"
        ),
        recorded_at=_aware_datetime(),
    )

    assert configuration_specification.configuration_kind == "parameter_profile"


def test_known_settings_bundle_example() -> None:
    configuration_specification = ConfigurationSpecification(
        configuration_specification_id="config-spec:schedule-definition-v1",
        configuration_kind="settings_bundle",
        canonical_name="Analysis Schedule Settings schedule-v1",
        recorded_at=_aware_datetime(),
    )

    assert configuration_specification.configuration_kind == "settings_bundle"


def test_known_policy_profile_example() -> None:
    configuration_specification = ConfigurationSpecification(
        configuration_specification_id="config-spec:confidence-policy-v1",
        configuration_kind="policy_profile",
        canonical_name="Evidence Confidence Policy confidence-v1",
        recorded_at=_aware_datetime(),
    )

    assert configuration_specification.configuration_kind == "policy_profile"


def test_known_feature_flag_set_example() -> None:
    configuration_specification = ConfigurationSpecification(
        configuration_specification_id="config-spec:auto-analyze-flags-v1",
        configuration_kind="feature_flag_set",
        canonical_name="Collection Automation Flags flags-v1",
        recorded_at=_aware_datetime(),
    )

    assert configuration_specification.configuration_kind == "feature_flag_set"


def test_confidential_known_configuration_uses_sanitized_canonical_name() -> None:
    # ACR-010 §16/§19.3: withheld/confidential parameter values alone do
    # not force Unknown classification when revision-distinguishable
    # identity is known. No content field exists on this model regardless.
    configuration_specification = ConfigurationSpecification(
        configuration_specification_id="config-spec:confidential:9d4e2f8a1c73",
        configuration_kind="policy_profile",
        canonical_name="confidential-routing-policy-9d4e2f8a1c73",
        recorded_at=_aware_datetime(),
    )

    assert configuration_specification.canonical_name == (
        "confidential-routing-policy-9d4e2f8a1c73"
    )


def test_unknown_configuration_specification_is_accepted_as_complete_record() -> (
    None
):
    configuration_specification = ConfigurationSpecification(
        configuration_specification_id="config-spec:unknown:3e9b7f1a5c82",
        configuration_kind="unknown",
        canonical_name="Unknown Configuration Specification 3e9b7f1a5c82",
        recorded_at=_aware_datetime(),
    )

    assert configuration_specification.configuration_kind == "unknown"
    assert configuration_specification.canonical_name == (
        "Unknown Configuration Specification 3e9b7f1a5c82"
    )


def test_empty_identifiers_remain_rejected_for_unknown_records() -> None:
    arguments = _valid_arguments()
    arguments["configuration_kind"] = "unknown"
    arguments["canonical_name"] = ""

    with pytest.raises(ValueError):
        ConfigurationSpecification(**arguments)


# --- Content-free model ---


def test_configuration_specification_has_no_content_fields() -> None:
    field_names = {field.name for field in fields(ConfigurationSpecification)}

    content_fields = {
        "parameter_schema",
        "parameter_values",
        "resolved_values",
        "defaults",
        "overrides",
        "inheritance",
        "content",
        "content_hash",
        "source_file",
        "environment",
        "environment_variables",
        "format",
        "loader",
        "raw_payload",
    }

    assert field_names.isdisjoint(content_fields)


# --- Secret-free model ---


def test_configuration_specification_has_no_secret_fields() -> None:
    field_names = {field.name for field in fields(ConfigurationSpecification)}

    secret_fields = {
        "secret_ref",
        "secret_refs",
        "secret_name",
        "credential",
        "api_key",
        "access_token",
        "token",
        "password",
        "private_key",
        "database_url",
        "api_endpoint",
        "hostname",
        "region",
    }

    assert field_names.isdisjoint(secret_fields)


# --- Other prohibited fields ---


def test_configuration_specification_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(ConfigurationSpecification)}

    prohibited_fields = {
        # Version / revision (folded into canonical_name)
        "version",
        "revision",
        "revision_id",
        "semantic_version",
        # Other Concepts (already separate / already on Provenance)
        "model_ref",
        "prompt_ref",
        "execution_ref",
        "actor_ref",
        "provider_ref",
        "source_ref",
        # Deployment / Runtime
        "deployment_ref",
        "runtime_ref",
        # Occurrence-level (Job/Attempt/Run)
        "job_id",
        "attempt_id",
        "run_id",
        "request_id",
        "generation_id",
        "invocation_id",
        # Lifecycle / policy
        "status",
        "active",
        "inactive",
        "deprecated",
        "retired",
        "approved",
        "blocked",
        "deprecated_at",
        "retired_at",
        "updated_at",
        # Unbounded
        "metadata",
        "arbitrary_json",
        "personal_information",
        # Reverse references / correction machinery (not implemented)
        "provenance_refs",
        "configuration_refs",
        "supersedes_ref",
        "resolved_ref",
        "duplicate_of_ref",
        "revision_of_ref",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Provenance compatibility ---


def _valid_provenance_arguments(
    configuration_specification_id: str | None,
) -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-config-spec-001",
        "activity_kind": "summarize",
        "actor_ref": "actor:atlas:summarization-service",
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
        "configuration_ref": configuration_specification_id,
    }


def test_configuration_specification_id_can_be_passed_to_provenance_configuration_ref() -> (
    None
):
    configuration_specification = ConfigurationSpecification(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments(
            configuration_specification.configuration_specification_id
        )
    )

    assert provenance.configuration_ref == (
        configuration_specification.configuration_specification_id
    )


def test_provenance_holds_id_string_not_configuration_specification_object() -> (
    None
):
    configuration_specification = ConfigurationSpecification(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments(
            configuration_specification.configuration_specification_id
        )
    )

    assert isinstance(provenance.configuration_ref, str)
    assert not isinstance(provenance.configuration_ref, ConfigurationSpecification)


def test_provenance_configuration_ref_remains_optional_and_none_is_accepted() -> (
    None
):
    provenance = Provenance(**_valid_provenance_arguments(None))

    assert provenance.configuration_ref is None


def test_configuration_specification_has_no_reverse_provenance_reference() -> None:
    field_names = {field.name for field in fields(ConfigurationSpecification)}

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


# --- Package export and cross-Concept isolation ---


def test_package_exports_all_ten_core_models() -> None:
    import atlas_core

    assert set(atlas_core.__all__) == {
        "AIModel",
        "Actor",
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

    assert atlas_core.ConfigurationSpecification is ConfigurationSpecification


def test_configuration_specification_has_no_other_core_model_reference() -> None:
    field_names = {field.name for field in fields(ConfigurationSpecification)}

    assert "evidence_id" not in field_names
    assert "evidence_ref" not in field_names
    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "source_id" not in field_names
    assert "source_ref" not in field_names
    assert "actor_id" not in field_names
    assert "actor_ref" not in field_names
    assert "model_id" not in field_names
    assert "model_ref" not in field_names
    assert "execution_specification_id" not in field_names
    assert "execution_ref" not in field_names
    assert "prompt_specification_id" not in field_names
    assert "prompt_ref" not in field_names


def test_no_existing_core_model_imports_configuration_specification() -> None:
    import ast
    import inspect

    import atlas_core.actor as actor_module
    import atlas_core.ai_model as ai_model_module
    import atlas_core.evidence as evidence_module
    import atlas_core.execution_specification as execution_specification_module
    import atlas_core.observation as observation_module
    import atlas_core.prompt_specification as prompt_specification_module
    import atlas_core.provenance as provenance_module
    import atlas_core.source as source_module

    for module in (
        actor_module,
        ai_model_module,
        evidence_module,
        execution_specification_module,
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

        assert "atlas_core.configuration_specification" not in imported_modules
