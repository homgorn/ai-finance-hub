#!/usr/bin/env python3
"""Sync external skill-like assets into local catalog lock.

- Reads `config/skill_sources/sources.yaml` (very small parser fallback if PyYAML absent).
- Uses GitHub REST API (tree endpoint) when available.
- Generates `data/skills/catalog.lock.json` with normalized entries.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_FILE = ROOT / "config/skill_sources/sources.yaml"
LOCK_FILE = ROOT / "data/skills/catalog.lock.json"


@dataclass
class RepoSource:
    provider: str
    owner: str
    repo: str
    branch: str
    skill_path_hints: list[str]


@dataclass
class CatalogEntry:
    provider: str
    repo: str
    path: str
    kind: str


def parse_sources_yaml(raw: str) -> list[RepoSource]:
    """Minimal parser for the known YAML shape to avoid non-stdlib dependency."""
    providers: list[RepoSource] = []
    current_provider = ""
    current_repo: dict[str, str] | None = None
    current_hints: list[str] = []

    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("- name:"):
            current_provider = s.split(":", 1)[1].strip()
            continue
        if s.startswith("- owner:"):
            if current_repo:
                providers.append(
                    RepoSource(
                        provider=current_provider,
                        owner=current_repo["owner"],
                        repo=current_repo["repo"],
                        branch=current_repo.get("branch", "main"),
                        skill_path_hints=current_hints[:] or ["skills"],
                    )
                )
            current_repo = {"owner": s.split(":", 1)[1].strip()}
            current_hints = []
            continue
        if current_repo and s.startswith("repo:"):
            current_repo["repo"] = s.split(":", 1)[1].strip()
            continue
        if current_repo and s.startswith("branch:"):
            current_repo["branch"] = s.split(":", 1)[1].strip()
            continue
        if current_repo and s.startswith("-") and "skill_path_hints" not in s:
            val = s[1:].strip()
            if val and not val.startswith("owner:"):
                current_hints.append(val)

    if current_repo:
        providers.append(
            RepoSource(
                provider=current_provider,
                owner=current_repo["owner"],
                repo=current_repo["repo"],
                branch=current_repo.get("branch", "main"),
                skill_path_hints=current_hints[:] or ["skills"],
            )
        )
    return providers


def github_tree(owner: str, repo: str, branch: str) -> list[str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{urllib.parse.quote(branch)}?recursive=1"
    req = urllib.request.Request(url, headers={"User-Agent": "ai-finance-hub-sync"})
    with urllib.request.urlopen(req, timeout=20) as resp:  # nosec B310
        payload = json.loads(resp.read().decode("utf-8"))
    items = payload.get("tree", [])
    return [x.get("path", "") for x in items if x.get("type") == "blob"]


def classify(path: str) -> str | None:
    p = path.lower()
    if p.endswith("skill.md"):
        return "skill"
    if re.search(r"(agent|orchestr|tool|prompt)", p):
        return "agent_asset"
    return None


def discover_entries(src: RepoSource, paths: list[str]) -> list[CatalogEntry]:
    out: list[CatalogEntry] = []
    for p in paths:
        if not any(p.startswith(hint + "/") or p == hint for hint in src.skill_path_hints):
            continue
        kind = classify(p)
        if kind:
            out.append(
                CatalogEntry(
                    provider=src.provider,
                    repo=f"{src.owner}/{src.repo}@{src.branch}",
                    path=p,
                    kind=kind,
                )
            )
    return out


def main() -> int:
    raw = SOURCES_FILE.read_text(encoding="utf-8")
    sources = parse_sources_yaml(raw)

    entries: list[CatalogEntry] = []
    failures: list[str] = []

    for src in sources:
        try:
            paths = github_tree(src.owner, src.repo, src.branch)
            entries.extend(discover_entries(src, paths))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            failures.append(f"{src.owner}/{src.repo}: {exc}")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources_total": len(sources),
        "entries_total": len(entries),
        "failures": failures,
        "entries": [asdict(e) for e in sorted(entries, key=lambda x: (x.provider, x.repo, x.path))],
    }
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"sources={len(sources)} entries={len(entries)} failures={len(failures)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
