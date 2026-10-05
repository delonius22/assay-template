"""The model gateway client (assumes OpenAI-compatible, A1). Replace only
this function if your gateway differs."""
from langchain_core.language_models import BaseChatModel

from ..settings import Settings


def make_model(model: str, s: Settings) -> BaseChatModel:
    """A chat client for one model on the gateway.

    Spec: S4.3 | Ticket: 10 | Traces to: I9, I11, A1

    Build steps:
    1. Task: Import inside the function: `from langchain_openai import ChatOpenAI`
       (heavy optional dependency; tests never call this).
       Expected outcome: test runs need no gateway client.
    2. Task: Return `ChatOpenAI(model=model, base_url=s.gateway_url, api_key=s.gateway_key,
       default_headers=s.gateway_headers or None, timeout=s.timeout_s, max_retries=0, temperature=0.2)`.
       Expected outcome: a timeout on every call; the client's own retries off so S4.1 owns retries.
    """
    raise NotImplementedError("S4.3")
