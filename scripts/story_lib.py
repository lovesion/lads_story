from __future__ import annotations
from datetime import date
from pathlib import Path
import re

REQUIRED = {"id", "title", "fandom", "character", "world", "relationship_stage", "characters", "tags", "length", "created_at", "generation_seed"}

def parse_story(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"): raise ValueError("missing opening front-matter delimiter")
    try: raw, body = text[4:].split("\n---\n", 1)
    except ValueError as exc: raise ValueError("missing closing front-matter delimiter") from exc
    meta, active_list, active_object = {}, None, None
    for line in raw.splitlines():
        if not line.strip(): continue
        if (item := re.match(r"^\s+-\s+(.+)$", line)) and active_list:
            meta[active_list].append(item.group(1).strip().strip('"')); continue
        if (nested := re.match(r"^\s{2}([a-z_]+):\s*(.+)$", line)) and active_object:
            meta[active_object][nested.group(1)] = nested.group(2).strip().strip('"'); continue
        match = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not match: raise ValueError(f"invalid front-matter line: {line}")
        key, value = match.groups(); active_list = key if not value and key in {"characters", "tags"} else None; active_object = key if not value and key == "generation_seed" else None
        meta[key] = [] if active_list else ({} if active_object else value.strip().strip('"'))
    return meta, body.strip()

def validate(meta: dict, body: str, path: Path) -> list[str]:
    errors = []
    if unknown := set(meta) - (REQUIRED | {"summary"}): errors.append(f"unknown fields: {', '.join(sorted(unknown))}")
    if missing := REQUIRED - set(meta): errors.append(f"missing fields: {', '.join(sorted(missing))}")
    if not re.fullmatch(r"\d{11}", str(meta.get("id", ""))): errors.append("id must be 11 digits")
    if meta.get("fandom") != "恋与深空": errors.append("fandom must equal 恋与深空")
    if meta.get("character") not in {"qinche", "xiyi"}: errors.append("invalid character")
    if meta.get("world") not in {"canon", "if", "modern"}: errors.append("invalid world")
    if meta.get("relationship_stage") not in {"first_meet", "close", "dating", "married"}: errors.append("invalid relationship_stage")
    if meta.get("length") != "short": errors.append("length must equal short")
    for key in ("characters", "tags"):
        if not isinstance(meta.get(key), list) or not meta[key]: errors.append(f"{key} must be a non-empty list")
    seed = meta.get("generation_seed")
    if not isinstance(seed, dict) or any(not seed.get(key) for key in ("scene", "emotion", "conflict")): errors.append("generation_seed must contain scene, emotion and conflict")
    try:
        created = date.fromisoformat(str(meta.get("created_at")))
        if created.isoformat() != path.parent.name: errors.append("created_at must match its directory")
        if str(meta.get("id"))[:8] != created.strftime("%Y%m%d"): errors.append("id date must match created_at")
    except ValueError: errors.append("created_at must be ISO date")
    if not body: errors.append("body must not be empty")
    return errors
