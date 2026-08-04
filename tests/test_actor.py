from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone

import pytest

from atlas_core import Actor, Evidence, Observation, Provenance, Source


def _aware_datetime(
    year: int = 2026,
    month: int = 8,
    day: int = 3,
    hour: int = 10,
) -> datetime:
    return datetime(year, month, day, hour, tzinfo=timezone.utc)


def _valid_arguments() -> dict[str, object]:
    return {
        "actor_id": "actor:atlas:pdf-retrieval-service",
        "actor_kind": "service",
        "canonical_name": "Atlas PDF Retrieval Service",
        "recorded_at": _aware_datetime(),
    }


# --- Construction and representation ---


def test_actor_can_be_created() -> None:
    arguments = _valid_arguments()

    actor = Actor(**arguments)

    assert actor.actor_id == "actor:atlas:pdf-retrieval-service"
    assert actor.actor_kind == "service"
    assert actor.canonical_name == "Atlas PDF Retrieval Service"
    assert actor.recorded_at == arguments["recorded_at"]


def test_actor_is_exported_from_package_root() -> None:
    from atlas_core.actor import Actor as ModuleActor

    assert Actor is ModuleActor


def test_actor_is_immutable() -> None:
    actor = Actor(**_valid_arguments())

    with pytest.raises(FrozenInstanceError):
        actor.canonical_name = "changed"  # type: ignore[misc]


def test_actor_requires_keyword_arguments() -> None:
    arguments = _valid_arguments()

    with pytest.raises(TypeError):
        Actor(*arguments.values())  # type: ignore[misc]


def test_actor_has_slots() -> None:
    actor = Actor(**_valid_arguments())

    assert not hasattr(actor, "__dict__")


def test_actor_has_exact_approved_field_set_and_order() -> None:
    field_names = tuple(field.name for field in fields(Actor))

    assert field_names == (
        "actor_id",
        "actor_kind",
        "canonical_name",
        "recorded_at",
    )


def test_actor_field_count_is_four() -> None:
    assert len(fields(Actor)) == 4


def test_all_fields_are_required() -> None:
    for field in fields(Actor):
        assert field.default is MISSING
        assert field.default_factory is MISSING  # type: ignore[misc]


# --- Required strings ---


@pytest.mark.parametrize(
    "field_name",
    ("actor_id", "actor_kind", "canonical_name"),
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
        Actor(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("actor_id", "actor_kind", "canonical_name"),
)
@pytest.mark.parametrize("invalid_value", (123, None, [], {}))
def test_required_strings_reject_non_string(
    field_name: str,
    invalid_value: object,
) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = invalid_value

    with pytest.raises(TypeError):
        Actor(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("actor_id", "actor_kind", "canonical_name"),
)
def test_required_strings_are_required_at_construction(
    field_name: str,
) -> None:
    arguments = _valid_arguments()
    del arguments[field_name]

    with pytest.raises(TypeError):
        Actor(**arguments)


@pytest.mark.parametrize(
    "field_name",
    ("actor_id", "actor_kind", "canonical_name"),
)
def test_required_strings_preserve_internal_content(field_name: str) -> None:
    arguments = _valid_arguments()
    arguments[field_name] = "Value With Internal   Spacing, Punctuation! Ünïcödé"

    actor = Actor(**arguments)

    assert getattr(actor, field_name) == (
        "Value With Internal   Spacing, Punctuation! Ünïcödé"
    )


# --- actor_kind extensibility ---


def test_unknown_but_valid_actor_kind_is_accepted() -> None:
    arguments = _valid_arguments()
    arguments["actor_kind"] = "some-brand-new-actor-kind"

    actor = Actor(**arguments)

    assert actor.actor_kind == "some-brand-new-actor-kind"


# --- canonical_name semantics ---


def test_duplicate_canonical_name_is_permitted_across_distinct_actors() -> None:
    arguments_a = _valid_arguments()
    arguments_a["actor_id"] = "actor:a"
    arguments_a["canonical_name"] = "Atlas Ingestion Worker"

    arguments_b = _valid_arguments()
    arguments_b["actor_id"] = "actor:b"
    arguments_b["canonical_name"] = "Atlas Ingestion Worker"

    actor_a = Actor(**arguments_a)
    actor_b = Actor(**arguments_b)

    assert actor_a.canonical_name == actor_b.canonical_name
    assert actor_a.actor_id != actor_b.actor_id


def test_canonical_name_is_not_normalized() -> None:
    arguments = _valid_arguments()
    arguments["canonical_name"] = "Atlas Ingestion Worker"

    actor = Actor(**arguments)

    assert actor.canonical_name == "Atlas Ingestion Worker"


# --- recorded_at ---


def test_recorded_at_accepts_timezone_aware_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = _aware_datetime(hour=9)

    actor = Actor(**arguments)

    assert actor.recorded_at == _aware_datetime(hour=9)


def test_recorded_at_accepts_non_utc_aware_datetime() -> None:
    non_utc = datetime(2026, 8, 3, 10, tzinfo=timezone(timedelta(hours=9)))
    arguments = _valid_arguments()
    arguments["recorded_at"] = non_utc

    actor = Actor(**arguments)

    assert actor.recorded_at == non_utc


def test_recorded_at_rejects_naive_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = datetime(2026, 8, 3, 10)

    with pytest.raises(ValueError):
        Actor(**arguments)


def test_recorded_at_rejects_non_datetime() -> None:
    arguments = _valid_arguments()
    arguments["recorded_at"] = "2026-08-03T10:00:00Z"

    with pytest.raises(TypeError):
        Actor(**arguments)


def test_recorded_at_is_required_at_construction() -> None:
    arguments = _valid_arguments()
    del arguments["recorded_at"]

    with pytest.raises(TypeError):
        Actor(**arguments)


# --- Human, Service, Organization, AI Agent, Unknown, Anonymous examples ---


def test_human_actor_example() -> None:
    actor = Actor(
        actor_id="actor:human:field-operator-42",
        actor_kind="person",
        canonical_name="Field Operator 42",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "person"


def test_service_actor_example() -> None:
    actor = Actor(
        actor_id="actor:atlas:ingestion-service",
        actor_kind="service",
        canonical_name="Atlas Ingestion Service",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "service"


def test_crawler_actor_example() -> None:
    actor = Actor(
        actor_id="actor:atlas:government-document-crawler",
        actor_kind="crawler",
        canonical_name="Atlas Government Document Crawler",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "crawler"


def test_worker_actor_example() -> None:
    actor = Actor(
        actor_id="actor:atlas:ingestion-worker",
        actor_kind="worker",
        canonical_name="Atlas Ingestion Worker",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "worker"


def test_scheduler_actor_example() -> None:
    actor = Actor(
        actor_id="actor:atlas:scheduler",
        actor_kind="scheduler",
        canonical_name="Atlas Scheduler Service",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "scheduler"


def test_organization_actor_example() -> None:
    actor = Actor(
        actor_id="actor:org:bank-of-japan",
        actor_kind="organization",
        canonical_name="Bank of Japan",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "organization"


def test_autonomous_ai_agent_actor_example() -> None:
    actor = Actor(
        actor_id="actor:atlas:autonomous-research-agent",
        actor_kind="agent",
        canonical_name="Atlas Autonomous Research Agent",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "agent"


def test_ai_system_actor_example() -> None:
    actor = Actor(
        actor_id="actor:ai-system:public-statement-generator",
        actor_kind="ai_system",
        canonical_name="Public Statement Generator",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "ai_system"


def test_unknown_actor_is_accepted_as_complete_record() -> None:
    actor = Actor(
        actor_id="actor:unknown:legacy-import-001",
        actor_kind="unknown",
        canonical_name="unknown-legacy-operator-001",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "unknown"
    assert actor.canonical_name == "unknown-legacy-operator-001"


def test_anonymous_actor_is_accepted_as_complete_record() -> None:
    actor = Actor(
        actor_id="actor:confidential:operator-014",
        actor_kind="anonymous",
        canonical_name="confidential-operator-014",
        recorded_at=_aware_datetime(),
    )

    assert actor.actor_kind == "anonymous"
    assert actor.canonical_name == "confidential-operator-014"


def test_empty_identifiers_remain_rejected_for_anonymous_actors() -> None:
    arguments = _valid_arguments()
    arguments["actor_kind"] = "anonymous"
    arguments["canonical_name"] = ""

    with pytest.raises(ValueError):
        Actor(**arguments)


# --- Prohibited fields ---


def test_actor_has_no_prohibited_fields() -> None:
    field_names = {field.name for field in fields(Actor)}

    prohibited_fields = {
        # Role and authority
        "role",
        "actor_role",
        "reviewer",
        "approver",
        "validator",
        "operator",
        "permissions",
        "capabilities",
        # Relationships
        "organization_ref",
        "person_ref",
        "owner_ref",
        "operator_ref",
        "parent_actor_ref",
        "supervisor_ref",
        "delegator_ref",
        "provider_ref",
        # Accounts and credentials
        "account_ref",
        "credential_ref",
        "authorization_principal_ref",
        "service_account",
        "user_account",
        # Tool, Model, and execution
        "tool_ref",
        "model_ref",
        "software_version",
        "code_version",
        "parser_version",
        "job_id",
        "run_id",
        "process_id",
        "container_id",
        "deployment_id",
        "queue_name",
        "host_id",
        "session_id",
        # Status and lifecycle
        "status",
        "active",
        "is_active",
        "disabled",
        "suspended",
        "retired",
        "compromised",
        "revoked",
        "unavailable",
        "terminated",
        "last_active_at",
        "last_login_at",
        "updated_at",
        "established_at",
        "created_at",
        "activated_at",
        "deactivated_at",
        "account_created_at",
        "employment_started_at",
        "deployment_started_at",
        "born_at",
        "founded_at",
        # Domain identifiers
        "youtube_user_id",
        "github_user_id",
        "slack_user_id",
        "google_account_id",
        "openai_agent_id",
        "anthropic_agent_id",
        "aws_role_arn",
        "kubernetes_service_account",
        "employee_id",
        "department_id",
        "tenant_id",
        "customer_id",
        # Sensitive or unbounded data
        "email",
        "phone",
        "phone_number",
        "address",
        "government_id",
        "birth_date",
        "legal_identity",
        "api_key",
        "access_token",
        "refresh_token",
        "password",
        "cookie",
        "authorization_header",
        "private_key",
        "certificate_secret",
        "database_url",
        "connection_string",
        "secret",
        "metadata",
        "configuration",
        "attributes",
        "extra",
        "raw_payload",
        "authentication_payload",
        # Mutable name/alias
        "display_name",
        "current_name",
        "previous_name",
        "aliases",
        "former_names",
        # Reverse references
        "provenance_refs",
        "job_refs",
        "run_refs",
        "evidence_refs",
        "source_refs",
        "observation_refs",
    }

    assert field_names.isdisjoint(prohibited_fields)


# --- Provenance compatibility ---


def _valid_provenance_arguments(actor_id: str) -> dict[str, object]:
    activity_time = _aware_datetime()

    return {
        "provenance_id": "provenance-001",
        "activity_kind": "retrieve",
        "actor_ref": actor_id,
        "started_at": activity_time,
        "completed_at": activity_time,
        "recorded_at": activity_time,
    }


def test_actor_id_can_be_passed_to_provenance_actor_ref() -> None:
    actor = Actor(**_valid_arguments())

    provenance = Provenance(**_valid_provenance_arguments(actor.actor_id))

    assert provenance.actor_ref == actor.actor_id


def test_provenance_holds_id_string_not_actor_object() -> None:
    actor = Actor(**_valid_arguments())

    provenance = Provenance(**_valid_provenance_arguments(actor.actor_id))

    assert isinstance(provenance.actor_ref, str)
    assert not isinstance(provenance.actor_ref, Actor)


def test_actor_has_no_reverse_provenance_reference() -> None:
    field_names = {field.name for field in fields(Actor)}

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


# --- Multiple Actors used by separate Provenance records ---


def test_scheduler_and_worker_use_separate_provenance_records() -> None:
    scheduler = Actor(
        actor_id="actor:atlas:scheduler",
        actor_kind="scheduler",
        canonical_name="Atlas Scheduler Service",
        recorded_at=_aware_datetime(),
    )
    worker = Actor(
        actor_id="actor:atlas:ingestion-worker",
        actor_kind="worker",
        canonical_name="Atlas Ingestion Worker",
        recorded_at=_aware_datetime(),
    )

    dispatch_arguments = _valid_provenance_arguments(scheduler.actor_id)
    dispatch_arguments["provenance_id"] = "provenance:dispatch"
    dispatch_arguments["activity_kind"] = "dispatch"

    process_arguments = _valid_provenance_arguments(worker.actor_id)
    process_arguments["provenance_id"] = "provenance:process"
    process_arguments["activity_kind"] = "extract"

    dispatch_provenance = Provenance(**dispatch_arguments)
    process_provenance = Provenance(**process_arguments)

    assert dispatch_provenance.actor_ref == scheduler.actor_id
    assert process_provenance.actor_ref == worker.actor_id
    assert dispatch_provenance.actor_ref != process_provenance.actor_ref


def test_ai_generation_and_human_approval_use_separate_provenance_records() -> None:
    ai_service = Actor(
        actor_id="actor:atlas:ai-extraction-service",
        actor_kind="service",
        canonical_name="Atlas AI Extraction Service",
        recorded_at=_aware_datetime(),
    )
    human_approver = Actor(
        actor_id="actor:human:approver-07",
        actor_kind="person",
        canonical_name="Approver 07",
        recorded_at=_aware_datetime(),
    )

    generation_arguments = _valid_provenance_arguments(ai_service.actor_id)
    generation_arguments["provenance_id"] = "provenance:generation"
    generation_arguments["activity_kind"] = "generate"

    approval_arguments = _valid_provenance_arguments(human_approver.actor_id)
    approval_arguments["provenance_id"] = "provenance:approval"
    approval_arguments["activity_kind"] = "validate"
    approval_arguments["parent_provenance_refs"] = ("provenance:generation",)

    generation_provenance = Provenance(**generation_arguments)
    approval_provenance = Provenance(**approval_arguments)

    assert generation_provenance.actor_ref == ai_service.actor_id
    assert approval_provenance.actor_ref == human_approver.actor_id
    assert generation_provenance.actor_ref != approval_provenance.actor_ref


# --- Observation, Evidence, Source, and Provenance protection ---


def test_observation_evidence_source_provenance_remain_importable() -> None:
    import atlas_core

    assert atlas_core.Observation is Observation
    assert atlas_core.Evidence is Evidence
    assert atlas_core.Source is Source
    assert atlas_core.Provenance is Provenance


def test_package_exports_all_nine_core_models() -> None:
    import atlas_core

    assert set(atlas_core.__all__) == {
        "AIModel",
        "Actor",
        "ConfigurationSpecification",
        "Evidence",
        "ExecutionSpecification",
        "Observation",
        "PromptSpecification",
        "Provenance",
        "Source",
        "__version__",
    }


def test_actor_has_no_evidence_observation_or_source_reference() -> None:
    field_names = {field.name for field in fields(Actor)}

    assert "evidence_id" not in field_names
    assert "evidence_ref" not in field_names
    assert "evidence_refs" not in field_names
    assert "observation_id" not in field_names
    assert "observation_ref" not in field_names
    assert "source_id" not in field_names
    assert "source_ref" not in field_names


def test_actor_module_imports_only_standard_library() -> None:
    """Circular-import check inspects actual import nodes, not text
    such as docstrings or comments that happen to mention Core Model
    names."""
    import ast
    import inspect

    import atlas_core.actor as actor_module

    source = inspect.getsource(actor_module)
    tree = ast.parse(source)

    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.add(node.module)

    prohibited_modules = {
        "atlas_core.evidence",
        "atlas_core.observation",
        "atlas_core.provenance",
        "atlas_core.source",
    }

    assert imported_modules.isdisjoint(prohibited_modules)

    for module_name in imported_modules:
        assert module_name in {"__future__", "dataclasses", "datetime"}


def test_no_existing_core_model_imports_actor() -> None:
    import ast
    import inspect

    import atlas_core.evidence as evidence_module
    import atlas_core.observation as observation_module
    import atlas_core.provenance as provenance_module
    import atlas_core.source as source_module

    for module in (
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

        assert "atlas_core.actor" not in imported_modules


def test_package_root_import_succeeds() -> None:
    import atlas_core

    assert atlas_core.Actor is Actor


# --- Raise-only validation ---


def test_invalid_construction_raises_and_does_not_mutate_inputs() -> None:
    original_canonical_name = " Atlas Ingestion Worker"

    arguments = _valid_arguments()
    arguments["canonical_name"] = original_canonical_name

    with pytest.raises(ValueError):
        Actor(**arguments)

    assert arguments["canonical_name"] == original_canonical_name


def test_invalid_construction_does_not_use_object_setattr() -> None:
    import inspect

    import atlas_core.actor as actor_module

    source = inspect.getsource(actor_module)

    assert "object.__setattr__" not in source
