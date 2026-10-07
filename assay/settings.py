"""All configuration, read once from the environment. See .env.example."""
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ROLES = ("grill", "explore", "questionnaire", "reconcile", "dod", "prd", "spec", "tickets")


@dataclass(frozen=True)
class Settings:
    artifacts_dir: Path                 # generated files are written and served here
    database_url: str                   # Postgres; empty = local SQLite, development only
    sqlite_path: Path
    gateway_url: str                    # OpenAI-compatible model gateway
    gateway_key: str
    gateway_headers: dict[str, str]
    models: dict[str, str]              # model per role
    timeout_s: float
    cache_mode: Literal["explicit", "auto", "off"]
    retry_attempts: int
    retry_base_s: float
    retry_cap_s: float
    max_steps: int
    max_output_retries: int
    code_roots: tuple[Path, ...]        # the only directories code tools may read
    user_header: str                    # header the SSO proxy sets with the user's ID
    dev_user: str                       # development only: user when no SSO header is present
    approvers: frozenset[str]           # who may approve a PRD (empty = anyone)
    team_name: str
    service_token: str


def env(name: str, default: str = "") -> str:
    """Read one environment variable with a default."""
    return os.environ.get(name, default)


def load_settings() -> Settings:
    """Build Settings from environment variables."""
    dm = env("ASSAY_MODEL")
    models = {r: env(f"ASSAY_MODEL_{r.upper()}", dm) for r in ROLES}
    roots = tuple(Path(p).resolve() for p in env("ASSAY_CODE_ROOTS").split(os.pathsep) if p)
    approvers = frozenset(u.strip() for u in env("ASSAY_APPROVERS").split(",") if u.strip())
    headers = json.loads(env("ASSAY_GATEWAY_HEADERS", "{}"))
    return Settings(
        artifacts_dir=Path(env("ASSAY_ARTIFACTS_DIR", "./data")).resolve(),
        sqlite_path=Path(env("ASSAY_SQLITE_PATH", "./data/assay.sqlite")).resolve(),
        timeout_s=float(env("ASSAY_TIMEOUT_S", "120")),
        cache_mode=env("ASSAY_CACHE_MODE", "explicit"),
        retry_attempts=int(env("ASSAY_RETRY_ATTEMPTS", "5")),
        retry_base_s=float(env("ASSAY_RETRY_BASE_S", "1.0")),
        retry_cap_s=float(env("ASSAY_RETRY_CAP_S", "30")),
        max_steps=int(env("ASSAY_MAX_STEPS", "40")),
        max_output_retries=int(env("ASSAY_MAX_OUTPUT_RETRIES", "3")),
        user_header=env("ASSAY_USER_HEADER", "X-Forwarded-User"),
        dev_user=env("ASSAY_DEV_USER"),
        team_name=env("ASSAY_TEAM_NAME", "Delivery team"),
        service_token=env("ASSAY_SERVICE_TOKEN"),
        database_url=env("ASSAY_DATABASE_URL"),
        gateway_url=env("ASSAY_GATEWAY_URL"),
        gateway_key=env("ASSAY_GATEWAY_KEY"),
        models=models,
        code_roots=roots,
        approvers=approvers,
      gateway_headers=headers
    )

def missing_config(s: Settings) -> list[str]:
    """Name every setting that must be set before models can be called."""
    out = [f"ASSAY_MODEL or ASSAY_MODEL_{role.upper()}" for role, model in s.models.items() if not model]
    if not s.gateway_url:
        out.append("ASSAY_GATEWAY_URL")
    if not s.gateway_key:
        out.append("ASSAY_GATEWAY_KEY")
    return out
