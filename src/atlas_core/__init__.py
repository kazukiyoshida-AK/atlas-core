"""Domain-independent core package for Atlas."""

from atlas_core.evidence import Evidence
from atlas_core.observation import Observation
from atlas_core.provenance import Provenance
from atlas_core.source import Source

__version__ = "0.1.0"

__all__ = ["Evidence", "Observation", "Provenance", "Source", "__version__"]
