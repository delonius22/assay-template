"""PRD rules."""
from ..domain.models import PRDCore, PRDNarrative
from .common import compliance_claims


def core_problems(core: PRDCore, known_ids: set[str]) -> list[str]:
    """Problems with stories, features, and requirements.

       Expected outcome: no invented sources (I3) and no compliance assertions (I4).
    """
    sids = [s.id for s in core.stories] 
    problems = []
    if sids != [f"S-{i:02d}" for i in range(1, len(sids) + 1)]:
        problems.append(f"Story IDs must run S-01, S-02… in order; got {sids}")
    fids = [f.id for s in core.stories for f in s.features]
    if fids != [f"F-{i:02d}" for i in range(1, len(fids) + 1)]:
        problems.append(f"Feature IDs must run F-01, F-02… in order across all stories; got {fids}")
    for i, r in enumerate(core.functional, start=1):
        if r.feature_id not in fids:
            problems.append(f"Requirement {i}: unknown feature {r.feature_id}; valid: {fids}")
    for f in fids:
        if f not in {r.feature_id for r in core.functional}:
            problems.append(f"Feature {f} has no functional requirement.")
    for r in [*core.functional, *core.non_functional]:
        unknown = [s for s in r.sources if s not in known_ids]
        if unknown:
            problems.append(f"'{r.text[:60]}' cites unknown sources {unknown}. Cite only session-log or questionnaire IDs.")
    problems.extend(compliance_claims(core))
    return problems


def narrative_problems(nar: PRDNarrative, known_ids: set[str]) -> list[str]:
    """Problems with the PRD narrative.

       Expected outcome: no compliance assertions in prose.
    """
    problems = []
    for o in nar.objectives:
        if o.source not in known_ids:
            problems.append(f"Objective '{o.objective}' cites unknown source {o.source}.")
    problems.extend(compliance_claims(nar))
    return problems
