"""Spec rules."""
from ..domain.models import Spec
from .common import compliance_claims


def problems(spec: Spec, prd_ids: set[str]) -> list[str]:
    """Problems with spec coverage and module traces.
       Expected outcome: empty means the spec passes.
    """
    covered = {c.requirement for c in spec.coverage}
    problems = []
    if missing := sorted(prd_ids - covered):
        problems.append(f"Coverage is missing {missing}. Every FR-/NFR- ID must appear.")
    if extra := sorted(covered - prd_ids):
        problems.append(f"Coverage lists IDs that are not in the PRD: {extra}")
    for m in spec.modules:
        if bad := [s for s in m.serves if s not in prd_ids]:
            problems.append(f"Module '{m.name}' serves unknown IDs {bad}")
    problems.extend(compliance_claims(spec))
    return problems
