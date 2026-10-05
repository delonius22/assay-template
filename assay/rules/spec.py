"""Spec rules."""
from ..domain.models import Spec
from .common import compliance_claims


def problems(spec: Spec, prd_ids: set[str]) -> list[str]:
    """Problems with spec coverage and module traces.

    Spec: S3.5 | Ticket: 06 | Traces to: I1, I4

    Build steps:
    1. Task: `covered = {c.requirement for c in spec.coverage}`.
       Expected outcome: the IDs the spec claims to address.
    2. Task: If `missing := sorted(prd_ids - covered)`, add
       f"Coverage is missing {missing}. Every FR-/NFR- ID must appear.".
       Expected outcome: no requirement left without design.
    3. Task: If `extra := sorted(covered - prd_ids)`, add f"Coverage lists IDs that are not in the PRD: {extra}".
       Expected outcome: no invented requirements.
    4. Task: For each module `m` with `bad := [s for s in m.serves if s not in prd_ids]`, add
       f"Module '{m.name}' serves unknown IDs {bad}".
       Expected outcome: modules trace to real requirements.
    5. Task: Return the problems plus `compliance_claims(spec)`.
       Expected outcome: empty means the spec passes.
    """
    raise NotImplementedError("S3.5")
