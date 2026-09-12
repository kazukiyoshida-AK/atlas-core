from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from atlas_core import ExecutionSpecification, Provenance


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 4,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "execution_specification_id": "execution-spec:rule-based-analyzer-v1",
        "execution_kind": "analyzer",
        "canonical_name": "RuleBasedAnalyzer rule_based_v1",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_execution_specification_can_be_created() -> None:
    arguments = _valid_arguments()

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.execution_specification_id == (
        "execution-spec:rule-based-analyzer-v1"
    )
    assert execution_specification.execution_kind == "analyzer"
    assert execution_specification.canonical_name == (
        "RuleBasedAnalyzer rule_based_v1"
    )
    assert execution_specification.recorded_at == arguments["recorded_at"]


def test_execution_specification_is_exported_from_package_root() -> None:
    from atlas_core.execution_specification import (
        ExecutionSpecification as ModuleExecutionSpecification,
    )

    assert ExecutionSpecification is ModuleExecutionSpecification


def test_execution_specification_is_immutable() -> None:
    execution_specification = ExecutionSpecification(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        execution_specification.canonical_name = "changed"  # type: ignore[misc]


def test_execution_specification_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        ExecutionSpecification(*arguments.values())  # type: ignore[misc]


def test_execution_specification_has_slots() -> None:
    execution_specification = ExecutionSpecification(**_valid_arguments())

    assert not hasattr(execution_specification, "__dict__")


def test_execution_specification_has_exact_approved_field_set_and_order() -> None:
    field_names = tuple(field.name for field in fields(ExecutionSpecification))

    assert field_names == (
        "execution_specification_id",
        "execution_kind",
        "canonical_name",
        "recorded_at",
    )


def test_execution_specification_field_count_is_four() -> None:
    assert len(fields(ExecutionSpecification)) == 4


def test_all_fields_are_required() -> None:
    for field in fields(ExecutionSpecification):
        assert field.default is MISSING
        assert field.default_factory is MISSING  # type: ignore[misc]


# --- Required strings ---


@pytest.mark.parametrize(
    "field_name",
    ("execution_specification_id", "execution_kind", "canonical_name"),
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
        ExecutionSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("execution_specification_id", "execution_kind", "canonical_name"),
)
@pytest.mark.parametrize("invalid_value", (123, None, [], {}))
def test_required_strings_reject_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        ExecutionSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("execution_specification_id", "execution_kind", "canonical_name"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        ExecutionSpecification(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("execution_specification_id", "execution_kind", "canonical_name"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    execution_specification = ExecutionSpecification(**arguments)

    assert getattr(execution_specification, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


# --- execution_kind extensibility and recommended vocabulary ---


def test_unknown_but_valid_execution_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["execution_kind"] = "some-brand-new-execution-kind"

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.execution_kind == "some-brand-new-execution-kind"


@pytest.mark.parametrize(
    "recommended_kind",
    (
        "tool",
        "adapter",
        "parser",
        "pipeline",
        "workflow",
        "analyzer",
        "engine",
        "collector",
        "classifier",
        "client",
        "service",
        "function",
        "unknown",
    ),
)
def test_recommended_execution_kind_values_are_accepted(
    recommended_kind: str,
) -> None:
    arguments = _valid_arguments()
    arguments["execution_kind"] = recommended_kind

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.execution_kind == recommended_kind


def test_execution_kind_is_not_a_closed_enum() -> None:
    arguments = _valid_arguments()
    arguments["execution_kind"] = "domain_local_experimental_kind"

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.execution_kind == "domain_local_experimental_kind"


# --- canonical_name semantics ---


def test_duplicate_canonical_name_is_permitted_across_distinct_records() -> None:
    arguments_a = _valid_arguments()
    arguments_a["execution_specification_id"] = "execution-spec:a"
    arguments_a["canonical_name"] = "Shared Label"

    arguments_b = _valid_arguments()
    arguments_b["execution_specification_id"] = "execution-spec:b"
    arguments_b["canonical_name"] = "Shared Label"

    execution_specification_a = ExecutionSpecification(**arguments_a)
    execution_specification_b = ExecutionSpecification(**arguments_b)

    assert (
        execution_specification_a.canonical_name
        == execution_specification_b.canonical_name
    )
    assert (
        execution_specification_a.execution_specification_id
        != execution_specification_b.execution_specification_id
    )


def test_canonical_name_is_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["canonical_name"] = "FredAdapter"

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.canonical_name == "FredAdapter"


def test_arbitrary_opaque_execution_specification_id_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["execution_specification_id"] = "01HZY3K9G8N7Q2R5T6V8W0X1Y2"

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.execution_specification_id == (
        "01HZY3K9G8N7Q2R5T6V8W0X1Y2"
    )


def test_no_required_id_prefix_is_enforced() -> None:
    arguments = _valid_arguments()
    arguments["execution_specification_id"] = "just-any-non-empty-string"

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.execution_specification_id == (
        "just-any-non-empty-string"
    )


def test_revision_qualified_canonical_name_is_accepted() -> None:
    # ACR-008: canonical_name, not a separate version field, carries the
    # adopted implementation revision label.
    arguments = _valid_arguments()
    arguments["canonical_name"] = "RuleBasedAnalyzer rule_based_v1"

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.canonical_name == "RuleBasedAnalyzer rule_based_v1"


def test_a_distinct_code_revision_is_a_new_independent_record() -> None:
    revision_one = ExecutionSpecification(
        execution_specification_id="execution-spec:rule-based-analyzer-v1",
        execution_kind="analyzer",
        canonical_name="RuleBasedAnalyzer rule_based_v1",
        recorded_at=_aware_datetime(),
    )
    revision_two = ExecutionSpecification(
        execution_specification_id="execution-spec:rule-based-analyzer-v2",
        execution_kind="analyzer",
        canonical_name="RuleBasedAnalyzer rule_based_v2",
        recorded_at=_aware_datetime(),
    )

    # No field links the two records — a materially distinct revision is
    # an entirely new, independent identity (ACR-008 §14), never a
    # mutation of the prior record.
    assert revision_one.execution_specification_id != (
        revision_two.execution_specification_id
    )
    assert revision_one.canonical_name != revision_two.canonical_name


def test_bare_shared_label_remains_technically_accepted() -> None:
    # Semantic admission (whether a bare label is sufficient to
    # distinguish an implementation revision) is outside Core runtime
    # validation — Core only enforces string shape, per ACR-008 §11/§13.1.
    # "rule_based_v1" alone is not a *recommended* canonical_name when
    # several distinct implementations share the label, but it is not
    # rejected at construction time either.
    arguments = _valid_arguments()
    arguments["canonical_name"] = "rule_based_v1"

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.canonical_name == "rule_based_v1"


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    non_utc = datetime(2026, 8, 4, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    execution_specification = ExecutionSpecification(**arguments)

    assert execution_specification.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 4, 10)

    with pytest.raises(ValueError):
        ExecutionSpecification(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-04T10:00:00Z"

    with pytest.raises(TypeError):
        ExecutionSpecification(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        ExecutionSpecification(**arguments)


# --- Known, Unknown, and first-class invocation examples ---


def test_known_tool_example() -> None:
    execution_specification = ExecutionSpecification(
        execution_specification_id="execution-spec:fred-adapter",
        execution_kind="adapter",
        canonical_name="FredAdapter",
        recorded_at=_aware_datetime(),
    )

    assert execution_specification.execution_kind == "adapter"
    assert execution_specification.canonical_name == "FredAdapter"


def test_known_pipeline_example() -> None:
    execution_specification = ExecutionSpecification(
        execution_specification_id="execution-spec:llm-orchestration-pipeline",
        execution_kind="pipeline",
        canonical_name="LLM Orchestration Pipeline",
        recorded_at=_aware_datetime(),
    )

    assert execution_specification.execution_kind == "pipeline"


def test_standalone_first_class_function_example() -> None:
    # A standalone function directly selected/invoked as the activity's
    # executable unit, independently named and reusable, may be Known —
    # unlike an internal helper method (ACR-008 first-class invocation
    # boundary), which is never independently admitted.
    execution_specification = ExecutionSpecification(
        execution_specification_id="execution-spec:standalone-report-script",
        execution_kind="function",
        canonical_name="generate_weekly_report",
        recorded_at=_aware_datetime(),
    )

    assert execution_specification.execution_kind == "function"


def test_unknown_execution_specification_is_accepted_as_complete_record() -> None:
    # Opaque, non-sequential identifiers only.
    execution_specification = ExecutionSpecification(
        execution_specification_id="execution-spec:unknown:3e9b7f1a5c82",
        execution_kind="unknown",
        canonical_name="Unknown Execution Specification 3e9b7f1a5c82",
        recorded_at=_aware_datetime(),
    )

    assert execution_specification.execution_kind == "unknown"
    assert execution_specification.canonical_name == (
        "Unknown Execution Specification 3e9b7f1a5c82"
    )


def test_confidential_execution_specification_uses_opaque_identifiers() -> None:
    execution_specification = ExecutionSpecification(
        execution_specification_id="execution-spec:confidential:8a1d4e7c9f02",
        execution_kind="tool",
        canonical_name="confidential-tool-8a1d4e7c9f02",
        recorded_at=_aware_datetime(),
    )

    assert execution_specification.canonical_name == (
        "confidential-tool-8a1d4e7c9f02"
    )


def test_empty_identifiers_remain_rejected_for_unknown_records() -> None:
    arguments = _valid_arguments()
    arguments["execution_kind"] = "unknown"
    arguments["canonical_name"] = ""

    with pytest.raises(ValueError):
        ExecutionSpecification(**arguments)


# --- Prohibited fields ---


def test_execution_specification_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(ExecutionSpecification)}

    prohibited_fields = {
        # Version / revision (folded into canonical_name instead)
        "version",
        "code_revision",
        "semantic_version",
        "revision_id",
        # Package / artifact
        "package_name",
        "package_version",
        "sdk_version",
        "requirements_hash",
        "wheel_ref",
        "build_id",
        "git_commit_sha",
        # Entrypoint / method granularity
        "entrypoint",
        "method_name",
        "adapter_name",
        "pipeline_name",
        # Job / Attempt / Run / occurrence
        "job_id",
        "attempt_id",
        "run_id",
        "request_id",
        "invocation_id",
        "retry_count",
        "generation_id",
        # Deployment / Runtime / Container
        "container_image_ref",
        "container_digest",
        "runtime_ref",
        "deployment_ref",
        "region",
        "hostname",
        "cluster_ref",
        # Provider
        "provider_ref",
        "provider_name",
        "api_endpoint",
        # Other Concepts
        "model_ref",
        "actor_ref",
        "configuration_ref",
        "external_run_ref",
        "prompt_ref",
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
        # Capability / evaluation
        "capabilities",
        "supported_inputs",
        "benchmark_score",
        "reliability",
        "latency",
        "cost",
        # Unbounded / secret
        "metadata",
        "raw_payload",
        "arbitrary_json",
        "api_key",
        "access_token",
        "credential",
        "secret",
        # Reverse references
        "provenance_refs",
        "execution_refs",
        # Correction / resolution machinery (not implemented in v0.1)
        "supersedes_ref",
        "resolved_ref",
        "duplicate_of_ref",
        "revision_of_ref",
    }

    assert field_names.isdisjoint(prohibited_fields)


def test_execution_specification_has_no_relationship_field() -> None:
    field_names = {field.name for field in fields(ExecutionSpecification)}

    assert "base_execution_specification_ref" not in field_names
    assert "parent_execution_specification_ref" not in field_names
    assert "relationship_refs" not in field_names


# --- Provenance compatibility ---


def _valid_provenance_arguments(
    execution_specification_id: str | None,
) -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-execution-spec-001",
        "activity_kind": "analyze",
        "actor_ref": "actor:atlas:analysis-service",
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
        "execution_ref": execution_specification_id,
    }


def test_execution_specification_id_can_be_passed_to_provenance_execution_ref() -> (
    None
):
    execution_specification = ExecutionSpecification(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments(
            execution_specification.execution_specification_id
        )
    )

    assert provenance.execution_ref == (
        execution_specification.execution_specification_id
    )


def test_provenance_holds_id_string_not_execution_specification_object() -> None:
    execution_specification = ExecutionSpecification(**_valid_arguments())

    provenance = Provenance(
        **_valid_provenance_arguments(
            execution_specification.execution_specification_id
        )
    )

    assert isinstance(provenance.execution_ref, str)
    assert not isinstance(provenance.execution_ref, ExecutionSpecification)


def test_provenance_execution_ref_remains_optional() -> None:
    provenance = Provenance(**_valid_provenance_arguments(None))

    assert provenance.execution_ref is None


def test_execution_specification_has_no_reverse_provenance_reference() -> None:
    field_names = {field.name for field in fields(ExecutionSpecification)}

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


def test_package_exports_all_twelve_core_models() -> None:
    import atlas_core

    assert set(atlas_core.__all__) == {
        "AIModel",
        "Actor",
        "Artifact",
        "ConfigurationSpecification",
        "CorrectionRecord",
        "Evidence",
        "ExecutionSpecification",
        "ExternalResource",
        "ExternalRun",
        "Observation",
        "Outcome",
        "PromptSpecification",
        "Provenance",
        "Source",
        "__version__",
    }


def test_package_root_import_succeeds() -> None:
    import atlas_core

    assert atlas_core.ExecutionSpecification is ExecutionSpecification


def test_execution_specification_has_no_evidence_observation_source_actor_or_model_reference() -> (
    None
):
    field_names = {field.name for field in fields(ExecutionSpecification)}

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


def test_execution_specification_module_imports_only_standard_library() -> None:
    """Circular-import check inspects actual import nodes, not text
    such as docstrings or comments that happen to mention Core Model
    names."""
    import ast
    import inspect

    import atlas_core.execution_specification as execution_specification_module

    source = inspect.getsource(execution_specification_module)
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
        "atlas_core.observation",
        "atlas_core.provenance",
        "atlas_core.source",
    }

    assert imported_modules.isdisjoint(prohibited_modules)

    for module_name in imported_modules:
        assert module_name in {"__future__", "dataclasses", "datetime"}


def test_no_existing_core_model_imports_execution_specification() -> None:
    import ast
    import inspect

    import atlas_core.actor as actor_module
    import atlas_core.ai_model as ai_model_module
    import atlas_core.evidence as evidence_module
    import atlas_core.observation as observation_module
    import atlas_core.provenance as provenance_module
    import atlas_core.source as source_module

    for module in (
        actor_module,
        ai_model_module,
        evidence_module,
        observation_module,
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

        assert "atlas_core.execution_specification" not in imported_modules


# --- Raise-only validation ---


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_canonical_name = " RuleBasedAnalyzer rule_based_v1"

    arguments = _valid_arguments()
    arguments["canonical_name"] = original_canonical_name

    with pytest.raises(ValueError):
        ExecutionSpecification(**arguments)

    assert arguments["canonical_name"] == original_canonical_name


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.execution_specification as execution_specification_module

    source = inspect.getsource(execution_specification_module)

    assert "object.__setattr__" not in source
