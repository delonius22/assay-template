"""PRD rules."""
from ..domain.models import PRDCore, PRDNarrative
from .common import compliance_claims


def core_problems(core: PRDCore, known_ids: set[str]) -> list[str]:
    """Problems with stories, features, and requirements.

    Spec: S3.4 | Ticket: 05 | Traces to: I3, I4

    Build steps:
    1. Task: `sids = [s.id for s in core.stories]`; if `sids != [f"S-{i:02d}" for i in range(1, len(sids) + 1)]`,
       add f"Story IDs must run S-01, S-02… in order; got {sids}".
       Expected outcome: story numbering is sequential.
    2. Task: `fids = [f.id for s in core.stories for f in s.features]`; if it differs from
       `[f"F-{i:02d}" for i in range(1, len(fids) + 1)]`, add
       f"Feature IDs must run F-01, F-02… in order across all stories; got {fids}".
       Expected outcome: features number across stories, not per story.
    3. Task: For each requirement `r` (1-based index `i`) in `core.functional` whose `r.feature_id not in fids`,
       add f"Requirement {i}: unknown feature {r.feature_id}; valid: {fids}".
       Expected outcome: every requirement belongs to a real feature.
    4. Task: For each `f` in `fids` not in `{r.feature_id for r in core.functional}`, add
       f"Feature {f} has no functional requirement.".
       Expected outcome: every feature is specified.
    5. Task: For each `r` in `[*core.functional, *core.non_functional]`, collect
       `unknown = [s for s in r.sources if s not in known_ids]`; if any, add
       f"'{r.text[:60]}' cites unknown sources {unknown}. Cite only session-log or questionnaire IDs.".
       Then return the problems plus `compliance_claims(core)`.
       Expected outcome: no invented sources (I3) and no compliance assertions (I4).
    """
    raise NotImplementedError("S3.4")


def narrative_problems(nar: PRDNarrative, known_ids: set[str]) -> list[str]:
    """Problems with the PRD narrative.

    Spec: S3.4 | Ticket: 05 | Traces to: I3, I4

    Build steps:
    1. Task: For each `o` in `nar.objectives` with `o.source not in known_ids`, add
       f"Objective '{o.objective}' cites unknown source {o.source}.".
       Expected outcome: objectives are sourced.
    2. Task: Return those problems plus `compliance_claims(nar)`.
       Expected outcome: no compliance assertions in prose.
    """
    raise NotImplementedError("S3.4")
