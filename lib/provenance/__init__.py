"""Provenance documents for filed testimony: every figure, table and number, linked to its code.

See ``.cursor/skills/testimony-provenance/SKILL.md`` for how to build one.
"""

from lib.provenance.config import Hardcoded, KnownDifference, Link, ProvenanceConfig
from lib.provenance.resolve import filed_constant_resolver

__all__ = ["Hardcoded", "KnownDifference", "Link", "ProvenanceConfig", "filed_constant_resolver"]
