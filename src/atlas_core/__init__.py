"""Domain-independent core package for Atlas."""

from atlas_core.actor import Actor
from atlas_core.ai_model import AIModel
from atlas_core.artifact import Artifact
from atlas_core.configuration_specification import ConfigurationSpecification
from atlas_core.evidence import Evidence
from atlas_core.execution_specification import ExecutionSpecification
from atlas_core.external_resource import ExternalResource
from atlas_core.external_run import ExternalRun
from atlas_core.observation import Observation
from atlas_core.prompt_specification import PromptSpecification
from atlas_core.provenance import Provenance
from atlas_core.source import Source

__version__ = "0.1.0"

__all__ = [
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
]
