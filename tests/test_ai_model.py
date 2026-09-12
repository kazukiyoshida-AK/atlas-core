from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from atlas_core import AIModel, Provenance


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 3,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "model_id": "model:llama-3.1-70b-instruct",
        "model_kind": "language_model",
        "canonical_name": "Llama 3.1 70B Instruct",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_ai_model_can_be_created() -> None:
    arguments = _valid_arguments()

    ai_model = AIModel(**arguments)

    assert ai_model.model_id == "model:llama-3.1-70b-instruct"
    assert ai_model.model_kind == "language_model"
    assert ai_model.canonical_name == "Llama 3.1 70B Instruct"
    assert ai_model.recorded_at == arguments["recorded_at"]


def test_ai_model_is_exported_from_package_root() -> None:
    from atlas_core.ai_model import AIModel as ModuleAIModel

    assert AIModel is ModuleAIModel


def test_ai_model_is_immutable() -> None:
    ai_model = AIModel(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        ai_model.canonical_name = "changed"  # type: ignore[misc]


def test_ai_model_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        AIModel(*arguments.values())  # type: ignore[misc]


def test_ai_model_has_slots() -> None:
    ai_model = AIModel(**_valid_arguments())

    assert not hasattr(ai_model, "__dict__")


def test_ai_model_has_exact_approved_field_set_and_order() -> None:
    field_names = tuple(field.name for field in fields(AIModel))

    assert field_names == (
        "model_id",
        "model_kind",
        "canonical_name",
        "recorded_at",
    )


def test_ai_model_field_count_is_four() -> None:
    assert len(fields(AIModel)) == 4


def test_all_fields_are_required() -> None:
    for field in fields(AIModel):
        assert field.default is MISSING
        assert field.default_factory is MISSING  # type: ignore[misc]


# --- Required strings ---


@pytest.mark.parametrize(
    "field_name",
    ("model_id", "model_kind", "canonical_name"),
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
        AIModel(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("model_id", "model_kind", "canonical_name"),
)
@pytest.mark.parametrize("invalid_value", (123, None, [], {}))
def test_required_strings_reject_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        AIModel(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("model_id", "model_kind", "canonical_name"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        AIModel(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("model_id", "model_kind", "canonical_name"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    ai_model = AIModel(**arguments)

    assert getattr(ai_model, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


# --- model_kind extensibility and recommended vocabulary ---


def test_unknown_but_valid_model_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["model_kind"] = "some-brand-new-model-kind"

    ai_model = AIModel(**arguments)

    assert ai_model.model_kind == "some-brand-new-model-kind"


@pytest.mark.parametrize(
    "recommended_kind",
    (
        "language_model",
        "multimodal_model",
        "vision_model",
        "embedding_model",
        "reranking_model",
        "speech_model",
        "transcription_model",
        "image_generation_model",
        "classification_model",
        "forecasting_model",
        "recommendation_model",
        "anomaly_detection_model",
        "unknown",
    ),
)
def test_recommended_model_kind_values_are_accepted(recommended_kind: str) -> None:
    arguments = _valid_arguments()
    arguments["model_kind"] = recommended_kind

    ai_model = AIModel(**arguments)

    assert ai_model.model_kind == recommended_kind


def test_model_kind_is_not_a_closed_enum() -> None:
    # Demonstrates the recommended vocabulary is documentation, not a
    # runtime-enforced set: an arbitrary domain-local value is still valid.
    arguments = _valid_arguments()
    arguments["model_kind"] = "domain_local_experimental_kind"

    ai_model = AIModel(**arguments)

    assert ai_model.model_kind == "domain_local_experimental_kind"


def test_rule_based_label_is_not_asserted_as_a_valid_ai_model_kind() -> None:
    # rule_based_v1 and similar deterministic-analyzer labels stay on the
    # Tool/Execution Specification side; this suite deliberately contains
    # no worked example admitting such a label as an AI Model kind.
    recommended_kinds = {
        "language_model",
        "multimodal_model",
        "vision_model",
        "embedding_model",
        "reranking_model",
        "speech_model",
        "transcription_model",
        "image_generation_model",
        "classification_model",
        "forecasting_model",
        "recommendation_model",
        "anomaly_detection_model",
        "unknown",
    }

    assert "rule_based_model" not in recommended_kinds
    assert "rule_based_v1" not in recommended_kinds


# --- canonical_name semantics ---


def test_duplicate_canonical_name_is_permitted_across_distinct_ai_models() -> None:
    arguments_a = _valid_arguments()
    arguments_a["model_id"] = "model:a"
    arguments_a["canonical_name"] = "Shared Release Label"

    arguments_b = _valid_arguments()
    arguments_b["model_id"] = "model:b"
    arguments_b["canonical_name"] = "Shared Release Label"

    ai_model_a = AIModel(**arguments_a)
    ai_model_b = AIModel(**arguments_b)

    assert ai_model_a.canonical_name == ai_model_b.canonical_name
    assert ai_model_a.model_id != ai_model_b.model_id


def test_canonical_name_is_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["canonical_name"] = "Whisper large-v3"

    ai_model = AIModel(**arguments)

    assert ai_model.canonical_name == "Whisper large-v3"


def test_arbitrary_opaque_model_id_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["model_id"] = "01HZY3K9G8N7Q2R5T6V8W0X1Y2"

    ai_model = AIModel(**arguments)

    assert ai_model.model_id == "01HZY3K9G8N7Q2R5T6V8W0X1Y2"


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    ai_model = AIModel(**arguments)

    assert ai_model.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    non_utc = datetime(2026, 8, 3, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    ai_model = AIModel(**arguments)

    assert ai_model.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 3, 10)

    with pytest.raises(ValueError):
        AIModel(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-03T10:00:00Z"

    with pytest.raises(TypeError):
        AIModel(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        AIModel(**arguments)


# --- Known, Unknown, and confidential AI Model examples ---


def test_known_model_release_example() -> None:
    ai_model = AIModel(
        model_id="model:whisper-large-v3",
        model_kind="transcription_model",
        canonical_name="Whisper large-v3",
        recorded_at=_aware_datetime(),
    )

    assert ai_model.model_kind == "transcription_model"
    assert ai_model.canonical_name == "Whisper large-v3"


def test_unknown_model_is_accepted_as_complete_record() -> None:
    # Opaque, non-sequential identifiers only — sequential suffixes would
    # leak creation order and inventory size for Unknown/confidential
    # records (ACR-007 Revision 1, R3).
    ai_model = AIModel(
        model_id="model:unknown:7f3c9a2e1b6d",
        model_kind="unknown",
        canonical_name="unknown-legacy-analysis-model-7f3c9a2e1b6d",
        recorded_at=_aware_datetime(),
    )

    assert ai_model.model_kind == "unknown"
    assert ai_model.canonical_name == "unknown-legacy-analysis-model-7f3c9a2e1b6d"


def test_confidential_model_uses_opaque_non_sequential_identifiers() -> None:
    ai_model = AIModel(
        model_id="model:confidential:9d4e2f8a1c73",
        model_kind="multimodal_model",
        canonical_name="confidential-multimodal-model-9d4e2f8a1c73",
        recorded_at=_aware_datetime(),
    )

    assert ai_model.model_kind == "multimodal_model"
    assert ai_model.canonical_name == "confidential-multimodal-model-9d4e2f8a1c73"


def test_empty_identifiers_remain_rejected_for_unknown_models() -> None:
    arguments = _valid_arguments()
    arguments["model_kind"] = "unknown"
    arguments["canonical_name"] = ""

    with pytest.raises(ValueError):
        AIModel(**arguments)


# --- Persistent fine-tuned derivative example (identity only, no lineage) ---


def test_persistent_fine_tuned_derivative_is_an_independent_ai_model() -> None:
    base_model = AIModel(
        model_id="model:base-release",
        model_kind="language_model",
        canonical_name="Base Release",
        recorded_at=_aware_datetime(),
    )
    fine_tuned_derivative = AIModel(
        model_id="model:persistent-customer-fine-tune-001",
        model_kind="language_model",
        canonical_name="Persistent Customer Fine-Tune 001",
        recorded_at=_aware_datetime(),
    )

    # The derivative is its own complete, independent record. Nothing in
    # the schema links it back to base_model — no lineage field exists
    # (ACR-007 Revision 1, R6): derivative identity support without
    # lineage support is the intended and disclosed v0.1 limitation.
    assert fine_tuned_derivative.model_id != base_model.model_id
    assert fine_tuned_derivative.canonical_name != base_model.canonical_name


# --- Prohibited fields ---


def test_ai_model_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(AIModel)}

    prohibited_fields = {
        # Provider and Deployment
        "provider_ref",
        "provider_name",
        "endpoint_ref",
        "deployment_ref",
        "api_model_name",
        "api_version",
        "region",
        "gateway_ref",
        # Family and Lineage
        "family_ref",
        "family_name",
        "base_model_ref",
        "parent_model_ref",
        "derivation_kind",
        "fine_tune_ref",
        "adapter_ref",
        # Artifact
        "weights_ref",
        "weights_digest",
        "weights_path",
        "local_path",
        "checkpoint_ref",
        "checkpoint_path",
        "repository_commit",
        "model_file",
        # Architecture and size
        "architecture",
        "parameter_count",
        "hidden_size",
        "layer_count",
        "attention_type",
        # Capability and modality
        "modality",
        "modalities",
        "capabilities",
        "context_window",
        "maximum_output",
        "supports_tools",
        "supports_vision",
        "supports_audio",
        "supports_embeddings",
        "supports_generation",
        "structured_output",
        "reasoning",
        # Training and release
        "training_cutoff",
        "training_dataset",
        "release_date",
        "released_at",
        "published_at",
        "trained_at",
        "fine_tuned_at",
        "license",
        "tokenizer_ref",
        # Prompt and Configuration
        "prompt_ref",
        "prompt_text",
        "system_prompt",
        "user_prompt",
        "configuration_ref",
        "configuration",
        "temperature",
        "top_p",
        "top_k",
        "max_tokens",
        "seed",
        "reasoning_effort",
        "safety_settings",
        # Evaluation and cost
        "accuracy",
        "quality_score",
        "benchmark_score",
        "hallucination_rate",
        "safety_rating",
        "latency",
        "cost",
        "token_price",
        "reliability",
        # Lifecycle and policy
        "status",
        "active",
        "inactive",
        "available",
        "deprecated",
        "retired",
        "preview",
        "beta",
        "production",
        "preferred",
        "approved",
        "blocked",
        "deprecated_at",
        "retired_at",
        "updated_at",
        # External and Domain data
        "external_identifier",
        "customer_id",
        "tenant_id",
        "project_id",
        "openai_model_name",
        "anthropic_model_name",
        "gemini_model_name",
        "azure_deployment_name",
        "huggingface_repository",
        "ollama_tag",
        # Unbounded content and secrets
        "metadata",
        "raw_payload",
        "arbitrary_json",
        "api_key",
        "access_token",
        "credential",
        "endpoint_secret",
        "signed_url",
        "private_repository_token",
        "private_weights",
        "environment_variables",
        "connection_string",
        "secret",
        # Reverse references
        "provenance_refs",
        "deployment_refs",
        "provider_refs",
        "artifact_refs",
        "evaluation_refs",
        # Correction / resolution machinery (not implemented in v0.1)
        "supersedes_ref",
        "resolved_ref",
        "duplicate_of_ref",
        "revision_of_ref",
        "merged_into_ref",
    }

    assert field_names.isdisjoint(prohibited_fields)


def test_ai_model_has_no_alias_or_relationship_field() -> None:
    field_names = {field.name for field in fields(AIModel)}

    assert "aliases" not in field_names
    assert "alias_refs" not in field_names
    assert "relationship_refs" not in field_names
    assert "family_relationship_ref" not in field_names


# --- Provenance compatibility ---


def _valid_provenance_arguments(model_id: str | None) -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-ai-model-001",
        "activity_kind": "generate",
        "actor_ref": "actor:atlas:ai-extraction-service",
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
        "model_ref": model_id,
    }


def test_ai_model_id_can_be_passed_to_provenance_model_ref() -> None:
    ai_model = AIModel(**_valid_arguments())

    provenance = Provenance(**_valid_provenance_arguments(ai_model.model_id))

    assert provenance.model_ref == ai_model.model_id


def test_provenance_holds_id_string_not_ai_model_object() -> None:
    ai_model = AIModel(**_valid_arguments())

    provenance = Provenance(**_valid_provenance_arguments(ai_model.model_id))

    assert isinstance(provenance.model_ref, str)
    assert not isinstance(provenance.model_ref, AIModel)


def test_provenance_model_ref_remains_optional() -> None:
    provenance = Provenance(**_valid_provenance_arguments(None))

    assert provenance.model_ref is None


def test_ai_model_has_no_reverse_provenance_reference() -> None:
    field_names = {field.name for field in fields(AIModel)}

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

    assert atlas_core.AIModel is AIModel


def test_ai_model_has_no_evidence_observation_source_or_actor_reference() -> None:
    field_names = {field.name for field in fields(AIModel)}

    assert "evidence_id" not in field_names
    assert "evidence_ref" not in field_names
    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "source_id" not in field_names
    assert "source_ref" not in field_names
    assert "actor_id" not in field_names
    assert "actor_ref" not in field_names


def test_ai_model_module_imports_only_standard_library() -> None:
    """Circular-import check inspects actual import nodes, not text
    such as docstrings or comments that happen to mention Core Model
    names."""
    import ast
    import inspect

    import atlas_core.ai_model as ai_model_module

    source = inspect.getsource(ai_model_module)
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
        "atlas_core.evidence",
        "atlas_core.observation",
        "atlas_core.provenance",
        "atlas_core.source",
    }

    assert imported_modules.isdisjoint(prohibited_modules)

    for module_name in imported_modules:
        assert module_name in {"__future__", "dataclasses", "datetime"}


def test_no_existing_core_model_imports_ai_model() -> None:
    import ast
    import inspect

    import atlas_core.actor as actor_module
    import atlas_core.evidence as evidence_module
    import atlas_core.observation as observation_module
    import atlas_core.provenance as provenance_module
    import atlas_core.source as source_module

    for module in (
        actor_module,
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

        assert "atlas_core.ai_model" not in imported_modules


# --- Raise-only validation ---


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_canonical_name = " Llama 3.1 70B Instruct"

    arguments = _valid_arguments()
    arguments["canonical_name"] = original_canonical_name

    with pytest.raises(ValueError):
        AIModel(**arguments)

    assert arguments["canonical_name"] == original_canonical_name


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.ai_model as ai_model_module

    source = inspect.getsource(ai_model_module)

    assert "object.__setattr__" not in source
