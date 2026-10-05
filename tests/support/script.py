"""Scripted model outputs for a full low-balance-alerts initiative.

Three outputs are deliberately wrong on the first try: a compound question,
a made-up source ID, and a ticket plan that misses FR-03. Tests pass only if
the rules reject each one and the retry fixes it.
"""


def q(text, area="Problem"):
    """Test helper: q."""
    return {"text": text, "recommended_answer": "Recommended", "reason": "Because", "area": area}


def e(t, area, title, **kw):
    """Test helper: e."""
    return {"type": t, "area": area, "title": title, "detail": title, "source": "Jordan (PM)", **kw}


AC = [
    "Given an eligible account, when the customer saves a threshold of 200, then it is stored and shown.",
    "Given a threshold above 5000, when the customer saves it, then it is rejected with the allowed range.",
    "Given any change, when it is saved, then an audit event records who, when, and old and new values.",
]


def dod_item(level, statement):
    """Test helper: dod item."""
    return {
        "level": level,
        "statement": statement,
        "category": "Quality",
        "how_verified": "Pipeline check",
        "evidence": "Pipeline run link",
        "verified_by": "Reviewer",
        "source": "DoD session, Jordan",
    }


def script(kind: str, n: int) -> dict:
    """Test helper: script."""
    if kind == "GrillTurn":
        if n == 1:
            return {"next_question": q("What problem are we solving? Who has it?"), "done": False}
        if n == 2:
            return {"next_question": q("What problem are we solving for customers?"), "done": False}
        return {
            "recorded": [
                e("D", "Problem", "Customers overdraw without warning"),
                e("D", "Users", "Retail checking customers and contact-centre agents"),
                e(
                    "D",
                    "Outcome",
                    "Fewer overdrafts",
                    metric={
                        "measure": "Overdrafts per 1,000 accounts",
                        "baseline": "42",
                        "target": "34",
                        "by_when": "2027-06-30",
                    },
                ),
                e("D", "Scope", "Checking accounts are in scope", scope_side="in"),
                e("D", "Scope", "Joint holders are out of scope", scope_side="out"),
                e("D", "Journeys", "Customer sets a threshold", journey_path="happy"),
                e(
                    "D",
                    "Journeys",
                    "If saving fails, an error shows and nothing is stored",
                    journey_path="failure",
                ),
                e("D", "Data", "Threshold per account, classified Internal Confidential"),
                e("D", "Non-functional", "Alert within 2 minutes in 99% of cases"),
                e(
                    "Q",
                    "Regulation",
                    "Is a balance alert a customer disclosure?",
                    priority="Important",
                    owner="Compliance",
                    status="Open",
                ),
                e(
                    "D",
                    "Rollout",
                    "Pilot with staff; turn off the flag to roll back",
                    covers_rollback=True,
                ),
            ],
            "glossary_updates": [
                {
                    "term": "Threshold",
                    "definition": "The balance below which a customer wants an alert.",
                }
            ],
            "done": True,
        }
    if kind == "DodTurn":
        if n == 1:
            return {
                "next_question": q("Is there a bank-mandated SDLC standard?", "Delivery"),
                "done": False,
            }
        if n == 2:
            return {
                "agreed": [
                    dod_item("ticket", "A reviewer other than the author approved the merge"),
                    dod_item("ticket", "Every acceptance criterion has an automated test"),
                    dod_item("feature", "Business owner signed off user acceptance testing"),
                    dod_item("story", "Business owner confirmed the story's success measure"),
                ],
                "done": True,
            }
        return {"agreed": [], "done": True}
    if kind == "PRDCore":
        src = ["D-999"] if n == 1 else ["D-001"]
        return {
            "stories": [
                {
                    "id": "S-01",
                    "text": "As a retail customer, I want low-balance alerts, so that I avoid overdrafts.",
                    "features": [
                        {
                            "id": "F-01",
                            "name": "Alert set-up",
                            "summary": "Customers choose a threshold.",
                        },
                        {
                            "id": "F-02",
                            "name": "Alert delivery",
                            "summary": "Alerts reach the customer fast.",
                        },
                    ],
                }
            ],
            "functional": [
                {
                    "text": "The customer must be able to set one threshold per account.",
                    "priority": "Must have",
                    "feature_id": "F-01",
                    "sources": src,
                },
                {
                    "text": "The agent must be able to view, but not change, settings.",
                    "priority": "Should have",
                    "feature_id": "F-01",
                    "sources": ["D-002"],
                },
                {
                    "text": "The system must send an alert when the balance falls below the threshold.",
                    "priority": "Must have",
                    "feature_id": "F-02",
                    "sources": ["D-003"],
                },
            ],
            "non_functional": [
                {
                    "area": "Performance",
                    "text": "Alerts must arrive within 2 minutes in 99% of cases.",
                    "priority": "Must have",
                    "sources": ["D-009"],
                }
            ],
        }
    if kind == "PRDNarrative":
        return {
            "executive_summary": "Customers overdraw because they do not know their balance is low.",
            "problem": "Overdraft complaints are rising.",
            "evidence": "Contact-centre complaint data.",
            "cost_of_doing_nothing": "Fee reversals and complaints continue.",
            "objectives": [
                {
                    "objective": "Fewer overdrafts",
                    "measure": "Per 1,000 accounts",
                    "baseline": "42",
                    "target": "34",
                    "by_when": "2027-06-30",
                    "source": "D-003",
                }
            ],
            "in_scope": ["Checking accounts"],
            "out_of_scope": ["Joint account holders"],
            "stakeholders": [
                {"group": "Retail banking", "interest": "Fewer complaints", "role": "Accountable"}
            ],
            "risk_controls": [
                {
                    "area": "Disclosures",
                    "consideration": "Alert wording may be a disclosure",
                    "owner": "Compliance",
                }
            ],
            "release_approach": "Pilot with staff first.",
            "rollback": "Turn off the feature flag.",
            "training_and_procedures": "Brief contact-centre agents.",
            "customer_communication": "In-app notice.",
        }
    if kind == "Seams":
        return {"seams": ["Alert Preferences service API"], "rationale": "Highest stable boundary."}
    if kind == "Spec":
        return {
            "summary": "Add an Alert Preferences service and an alert sender.",
            "modules": [
                {
                    "name": "Alert Preferences",
                    "change": "New",
                    "responsibility": "Stores thresholds",
                    "serves": ["FR-01", "FR-02"],
                },
                {
                    "name": "Alert Sender",
                    "change": "New",
                    "responsibility": "Sends alerts",
                    "serves": ["FR-03", "NFR-01"],
                },
            ],
            "interfaces": "Save Threshold rejects values outside the allowed range.",
            "data": "Threshold per account.",
            "key_flows": "Save, then confirm.",
            "integrations": "Notification vendor.",
            "security": "Agents need the servicing role. Changes are audited.",
            "nfr_design": "Queue-backed sends.",
            "observability": "Send latency metric.",
            "rollout": "Feature flag.",
            "testing": "Test via the API.",
            "coverage": [
                {"requirement": "FR-01", "sections": ["modules", "interfaces"]},
                {"requirement": "FR-02", "sections": ["security"]},
                {"requirement": "FR-03", "sections": ["modules", "key_flows"]},
                {"requirement": "NFR-01", "sections": ["nfr_design"]},
            ],
        }
    if kind == "TicketPlan":
        t1 = {
            "feature_id": "F-01",
            "title": "Customer saves a threshold on one account",
            "user_story": "As a retail customer, I want to save a threshold, so that I am warned.",
            "acceptance_criteria": AC,
            "requirements": ["FR-01", "NFR-01"],
            "spec_refs": ["modules", "interfaces"],
            "sources": ["D-001"],
            "size": "M",
            "priority": "Must have",
        }
        t2 = {
            "feature_id": "F-01",
            "title": "Agent views a customer's alert settings",
            "user_story": "As an agent, I want to view alert settings, so that I can help customers.",
            "acceptance_criteria": AC,
            "requirements": ["FR-02"],
            "spec_refs": ["security"],
            "size": "S",
            "priority": "Should have",
            "depends_on": [1],
        }
        spike = {
            "feature_id": "F-02",
            "type": "Spike",
            "title": "Confirm the vendor's send rate",
            "question": "Can the vendor send 50,000 alerts per hour?",
            "timebox": "2 days",
            "acceptance_criteria": ["A written answer and an ADR if queuing is needed."],
            "size": "S",
            "priority": "Must have",
        }
        t4 = {
            "feature_id": "F-02",
            "title": "Send an alert when the balance drops",
            "user_story": "As a retail customer, I want an alert when my balance drops, so that I can act.",
            "acceptance_criteria": AC,
            "requirements": ["FR-03"],
            "spec_refs": ["key_flows"],
            "size": "M",
            "priority": "Must have",
            "depends_on": [3],
        }
        return {"tickets": [t1, t2, spike] if n == 1 else [t1, t2, spike, t4]}
    if kind == "BriefCritique":
        return {"ready": True}
    if kind == "Questionnaire":
        item = lambda t: {
            "text": t,
            "owner_role": "Developer",
            "priority": "Important",
            "why_it_matters": "x",
            "proposed_answer": "y",
            "reason": "z",
            "area": "Data",
        }
        return {
            "summary": "Data questions.",
            "questions": [item("Where is the threshold stored?"), item("How long is it kept?")],
        }
    if kind == "Reconciliation":
        return {
            "recorded": [
                {
                    "type": "D",
                    "area": "Data",
                    "title": "Thresholds kept seven years",
                    "detail": "Corrected by a developer",
                    "source": "Q-02, priya (Lead Developer)",
                }
            ]
        }
    if kind == "CurrentStateMap":
        return {
            "components": ["Alert Preferences"],
            "data_flow": "API to store",
            "data_stores": ["prefs"],
            "tests": "None",
        }
    raise AssertionError(f"unscripted {kind}")
