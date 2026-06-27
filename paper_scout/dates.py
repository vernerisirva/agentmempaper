from __future__ import annotations

import re
from dataclasses import dataclass


PRECISION_RANK = {
    "unknown": 0,
    "year": 1,
    "month": 2,
    "day": 3,
}


@dataclass(frozen=True)
class PublicationDate:
    value: str | None
    year: str | None
    precision: str
    source: str | None


def publication_date(value: str | None, source: str | None, year: str | int | None = None) -> PublicationDate:
    cleaned = str(value).strip() if value not in {None, ""} else None
    explicit_year = str(year).strip() if year not in {None, ""} else None
    precision = publication_date_precision(cleaned)
    derived_year = _year_from_value(cleaned) or explicit_year
    if precision == "unknown" and explicit_year:
        cleaned = explicit_year
        precision = "year"
    return PublicationDate(cleaned, derived_year, precision, source if precision != "unknown" else None)


def publication_date_precision(value: str | None) -> str:
    if not value:
        return "unknown"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return "day"
    if re.fullmatch(r"\d{4}-\d{2}", value):
        return "month"
    if re.fullmatch(r"\d{4}", value):
        return "year"
    return "unknown"


def precision_rank(precision: str | None) -> int:
    return PRECISION_RANK.get(precision or "unknown", 0)


def best_publication_date(left: PublicationDate, right: PublicationDate) -> PublicationDate:
    if precision_rank(right.precision) > precision_rank(left.precision):
        return right
    if precision_rank(left.precision) > 0:
        return left
    return right


def effective_sort_date(publication_value: str | None, precision: str | None, first_seen_date: str | None, future_date: bool = False) -> str | None:
    if future_date:
        return first_seen_date
    if precision_rank(precision) >= precision_rank("month"):
        return publication_value
    return first_seen_date


def sort_date_value(value: str | None, precision: str | None) -> str | None:
    if not value:
        return None
    if precision == "month" and re.fullmatch(r"\d{4}-\d{2}", value):
        return f"{value}-01"
    if precision == "year":
        return None
    return value


def _year_from_value(value: str | None) -> str | None:
    if not value:
        return None
    match = re.match(r"(\d{4})", value)
    return match.group(1) if match else None
