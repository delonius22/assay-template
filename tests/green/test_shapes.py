"""Data shapes (shipped complete) and the test fixtures that rely on them."""
import pytest
from pydantic import ValidationError

from assay.domain import models as M
from tests.support.script import script

OUTPUTS = {"GrillTurn": M.GrillTurn, "DodTurn": M.DodTurn, "PRDCore": M.PRDCore, "PRDNarrative": M.PRDNarrative,
           "Seams": M.Seams, "Spec": M.Spec, "TicketPlan": M.TicketPlan, "BriefCritique": M.BriefCritique,
           "Questionnaire": M.Questionnaire, "Reconciliation": M.Reconciliation, "CurrentStateMap": M.CurrentStateMap}


@pytest.mark.parametrize("kind", sorted(OUTPUTS))
def test_scripted_outputs_fit_their_shapes(kind):
    for n in (1, 2, 3):
        OUTPUTS[kind].model_validate(script(kind, n))


def test_story_text_must_be_a_user_story():
    with pytest.raises(ValidationError):
        M.StoryDraft(id="S-01", text="Low-balance alerts", features=[M.FeatureDraft(id="F-01", name="n", summary="s")])


def test_ticket_size_and_spec_refs_are_closed_sets():
    base = script("TicketPlan", 2)["tickets"][0]
    with pytest.raises(ValidationError):
        M.TicketDraft(**{**base, "size": "XL"})
    with pytest.raises(ValidationError):
        M.TicketDraft(**{**base, "spec_refs": ["database"]})
