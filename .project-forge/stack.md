# Stack

| Choice | Requirement served | Rejected | Why |
|---|---|---|---|
| Python 3.11+ | C3, existing team skills | — | LangGraph's primary language |
| LangGraph | I5, I6, I7: gated flow with checkpointed pauses | Pydantic AI graph, hand-rolled state machine | Mature interrupts and Postgres checkpoints |
| langchain-core + langchain-openai | A1: OpenAI-compatible gateway | Pydantic AI (removed by ruling) | Already a LangGraph dependency |
| Pydantic | I1: typed outputs | dataclasses, JSON Schema | Validation plus model tool schemas |
| FastAPI + one HTML page | C2 | Streamlit, React app | Small, testable, no build step |
| Postgres / SQLite | I6, C4 | Redis | Official LangGraph checkpointers |
| Jinja2 | C1: one definition per output format | f-strings | Templates editable without Python |
| ReportLab | C5: signable PDF | WeasyPrint, Word template | Pure Python, no system packages |
