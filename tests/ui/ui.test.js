const { JSDOM } = require("jsdom");
const fs = require("fs");
const html = fs.readFileSync(require("path").join(__dirname, "../../assay/api/static/index.html"), "utf8");

const pendings = {
  question: {kind: "question", challenge: "That is a solution, not a problem.", area: "Problem",
             question: "What problem are we solving?", recommended: "Overdrafts", reason: "Evidence"},
  dod_question: {kind: "dod_question", challenge: null, question: "Mandated standard?", recommended: "None", reason: "r"},
  map_review: {kind: "map_review", map: {components: ["A"], data_flow: "x", data_stores: ["s"], tests: "t", unknowns: []}},
  brief_fix: {kind: "brief_fix", issues: ["Outcome has no number"], brief: {ask: "a", why: "w", outcome: "o", known_steps: "", constraints: ""}},
  await_answers: {kind: "await_answers", round: 1, form: "/q/demo", note: "No new responses yet."},
  approval: {kind: "approval", version: "0.1", files: ["prd.pdf"], error: null},
  seams: {kind: "seams", seams: {seams: ["Service API"], rationale: "Stable", prior_art: []}},
  ticket_review: {kind: "ticket_review", uncovered: [{id: "NFR-02", reason: "Covered by platform"}],
                  tickets: [{id: "T-001", title: "Save a threshold", feature_id: "F-01", type: "Ticket", size: "M", depends_on_ids: []},
                            {id: "T-002", title: "View settings", feature_id: "F-01", type: "Ticket", size: "S", depends_on_ids: ["T-001"]}]},
};
const expect = {question: "#send", dod_question: "#send", map_review: "#ok", brief_fix: "#b-outcome",
                await_answers: "#who-answered", approval: "#approve", seams: "#approve", ticket_review: "#approve"};

async function render(kind, status, approver = true) {
  const errors = [];
  const dom = new JSDOM(html, {url: "http://localhost/s/demo", runScripts: "dangerously", pretendToBeVisual: true,
    beforeParse(w) {
      w.addEventListener("error", e => errors.push(e.message));
      w.alert = m => errors.push("alert: " + m);
      w.fetch = async (url) => {
        const body = url.endsWith("/api/me") ? {user: "jordan", approver, missing_config: []}
          : url.endsWith("/api/sessions") ? [{slug: "demo", title: "Demo", stage: "Intake", status}]
          : url.includes("/usage") ? {total: {calls: 3, cache_hit_rate: 0.8, transient_retries: 1, rejections: 2}}
          : url.includes("/responses") ? [{respondent: "priya", role: "Dev"}]
          : {slug: "demo", status, pending: kind ? pendings[kind] : null, error: status === "error" ? "Boom" : null,
             stage: "PRD review", title: "Demo", mode: 3, pm: "jordan", files: ["prd.pdf", "tickets.csv", "agent-prompt.md"]};
        return {ok: true, json: async () => body};
      };
    }});
  await new Promise(r => setTimeout(r, 150));
  return {doc: dom.window.document, errors};
}

(async () => {
  let failed = 0;
  for (const kind of Object.keys(pendings)) {
    const {doc, errors} = await render(kind, "waiting");
    const ok = doc.querySelector(expect[kind]) && !errors.length;
    console.log(`${ok ? "ok  " : "FAIL"} ${kind.padEnd(14)} ${errors.join("; ")}`);
    if (!ok) failed++;
  }
  for (const status of ["working", "error", "done"]) {
    const {doc, errors} = await render(null, status);
    const text = doc.querySelector("#pane")?.textContent || "";
    const ok = !errors.length && text.length > 10;
    console.log(`${ok ? "ok  " : "FAIL"} status:${status.padEnd(8)} ${text.trim().slice(0, 60)}`);
    if (!ok) failed++;
  }
  const {doc} = await render("approval", "waiting", false);
  const disabled = doc.querySelector("#approve").disabled;
  console.log(`${disabled ? "ok  " : "FAIL"} non-approver sees a disabled Approve button`);
  const {doc: d2} = await render("question", "waiting");
  const challenge = d2.querySelector(".challenge")?.textContent;
  const usage = d2.querySelector(".usage")?.textContent.trim();
  console.log(`${challenge ? "ok  " : "FAIL"} challenge shown: ${challenge}`);
  console.log(`${usage ? "ok  " : "FAIL"} usage line: ${usage}`);
  process.exit(failed || !disabled ? 1 : 0);
})();
