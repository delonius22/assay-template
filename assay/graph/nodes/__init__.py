"""Graph nodes, grouped by stage. Signature: node(state, runtime) -> dict.

Model calls live in *_think-style nodes; interrupt() lives alone in *_ask
nodes, because LangGraph reruns a paused node from its first line on
resume (I7). Routers (after_*) only read state.
"""
