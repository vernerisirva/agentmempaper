from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class QualityCuration:
    pinned: bool = False
    include_despite_quality: bool = False
    suppress_for_quality: bool = False
    quality_score_override: int | None = None
    quality_recommendation_override: str | None = None
    quality_note: str | None = None

    @property
    def has_manual_assessment(self) -> bool:
        return self.quality_score_override is not None or bool(self.quality_recommendation_override or self.quality_note)

    @property
    def has_quality_directive(self) -> bool:
        return self.pinned or self.include_despite_quality or self.suppress_for_quality or self.has_manual_assessment


def parse_curation_sections(text: str) -> dict[str, list[dict[str, object]]]:
    sections: dict[str, list[dict[str, object]]] = {
        "pinned": [],
        "overrides": [],
        "excluded": [],
        "date_overrides": [],
    }
    current_section: str | None = None
    current_item: dict[str, object] | None = None
    current_list_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current_section = line[:-1].strip()
            sections.setdefault(current_section, [])
            current_item = None
            current_list_key = None
            continue
        if current_section not in sections:
            continue
        stripped = line.strip()
        if stripped.startswith("- ") and current_list_key and current_item is not None and ":" not in stripped[2:]:
            current_item.setdefault(current_list_key, [])
            value = _clean_value(stripped[2:])
            if isinstance(current_item[current_list_key], list):
                current_item[current_list_key].append(value)  # type: ignore[index]
            continue
        if stripped.startswith("- "):
            current_item = {}
            sections[current_section].append(current_item)
            current_list_key = None
            rest = stripped[2:].strip()
            if ":" in rest:
                key, value = rest.split(":", 1)
                current_item[key.strip()] = _clean_value(value)
            continue
        if current_item is None:
            continue
        if stripped.endswith(":"):
            current_list_key = stripped[:-1].strip()
            current_item[current_list_key] = []
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            current_list_key = None
            current_item[key.strip()] = _clean_value(value)
    return sections


def quality_curation_for_paper(path: Path | None, canonical_id: str, title: str) -> QualityCuration:
    if path is None or not path.exists():
        return QualityCuration()
    sections = parse_curation_sections(path.read_text(encoding="utf-8"))
    matches: list[tuple[str, dict[str, object]]] = []
    for section in ("pinned", "overrides", "excluded"):
        for item in sections.get(section, []):
            if _matches(item, canonical_id, title):
                matches.append((section, item))
    if not matches:
        return QualityCuration()
    pinned = any(section == "pinned" for section, _ in matches)
    merged: dict[str, object] = {}
    for _, item in matches:
        merged.update(item)
    score = _optional_int(merged.get("quality_score_override"))
    recommendation = _optional_text(merged.get("quality_recommendation_override"))
    if recommendation not in {None, "strong", "promising", "uncertain", "weak", "unknown"}:
        recommendation = None
    return QualityCuration(
        pinned=pinned,
        include_despite_quality=_as_bool(merged.get("include_despite_quality")),
        suppress_for_quality=_as_bool(merged.get("suppress_for_quality")),
        quality_score_override=score,
        quality_recommendation_override=recommendation,
        quality_note=_optional_text(merged.get("quality_note")),
    )


def _matches(item: dict[str, object], canonical_id: str, title: str) -> bool:
    item_id = _optional_text(item.get("canonical_id"))
    item_title = _optional_text(item.get("title"))
    return bool((item_id and item_id == canonical_id) or (item_title and _normalize(item_title) == _normalize(title)))


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _clean_value(value: object) -> str:
    return str(value).strip().strip('"').strip("'")


def _optional_text(value: object) -> str | None:
    text = _clean_value(value) if value is not None else ""
    return text or None


def _optional_int(value: object) -> int | None:
    try:
        result = int(str(value)) if value not in {None, ""} else None
    except ValueError:
        return None
    return max(0, min(100, result)) if result is not None else None


def _as_bool(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}
