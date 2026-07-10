from typing import Any, Dict, List, Optional, Text
from datetime import datetime, timedelta
import re

from dateutil import parser as date_parser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

# Canonical storage format for incident_date. Matches what utter_ask_incident_date
# asks for and what action_claim_summary displays, so everything downstream sees
# one consistent format regardless of how the user typed the date.
DATE_FORMAT = "%m/%d/%Y"

# Two reference dates with every field different. dateutil fills any field the
# user did NOT supply from `default`, so a field is only genuinely present in the
# input when both parses agree on it. This lets us reject partial input like a
# bare "June" or a time-only "3pm" that would otherwise silently borrow today's
# date and pass as a valid incident date.
_DEFAULTS = (datetime(1900, 1, 1), datetime(2001, 2, 3))

_WEEKDAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
}
_WEEKDAY_RE = re.compile(
    r"(?:last |this |this past |past )?(" + "|".join(_WEEKDAYS) + r")"
)
_AGO_RE = re.compile(r"(?:(\d+)|a|an|one) (day|days|week|weeks) ago")


def _most_recent_weekday(today: datetime, target: int) -> datetime:
    """Most recent past date whose weekday is `target` (never today)."""
    delta = (today.weekday() - target) % 7
    if delta == 0:
        delta = 7  # "last Tuesday" / a bare weekday means a past day, not today
    return today - timedelta(days=delta)


def _resolve_relative(text: Text, today: datetime) -> Optional[datetime]:
    """Resolve common relative date phrases against `today`. None if not relative.

    The LLM extracts phrases like "last Tuesday" verbatim; the command generator
    has no notion of the current date, so we resolve them here where we do.
    """
    t = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        return None
    if t == "today":
        return today
    if t == "yesterday":
        return today - timedelta(days=1)
    if t in ("day before yesterday", "the day before yesterday"):
        return today - timedelta(days=2)
    if t == "last week":
        return today - timedelta(days=7)
    m = _AGO_RE.fullmatch(t)
    if m:
        n = int(m.group(1)) if m.group(1) else 1
        return today - timedelta(days=n * (7 if m.group(2).startswith("week") else 1))
    m = _WEEKDAY_RE.fullmatch(t)
    if m:
        return _most_recent_weekday(today, _WEEKDAYS[m.group(1)])
    return None


def _parse_full_date(text: Text, today: datetime) -> Optional[datetime]:
    """Resolve a relative phrase, else parse a concrete date (day+month+year)."""
    relative = _resolve_relative(text, today)
    if relative is not None:
        return relative

    parsed = []
    for default in _DEFAULTS:
        try:
            parsed.append(date_parser.parse(text, default=default, fuzzy=False))
        except (ValueError, OverflowError, TypeError):
            return None
    first, second = parsed
    # A field that came from the default (not the input) differs between parses.
    if (first.year, first.month, first.day) != (second.year, second.month, second.day):
        return None
    return first


class ValidateIncidentDate(Action):
    """Normalize the incident_date slot to MM/DD/YYYY, or reject and re-ask.

    Rasa Pro CALM runs validate_<slot_name> actions automatically every time the
    slot is collected. The incident_date slot is filled `from_llm`, which stores
    whatever the user typed ("June 30th 2026", "6/30/2026", "last Tuesday"). We
    resolve/normalize that into a single canonical format; anything we can't turn
    into a full date is rejected so the collect step asks again, instead of the
    previous strict-regex loop.
    """

    def name(self) -> Text:
        return "validate_incident_date"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        raw = tracker.get_slot("incident_date")

        # validate_<slot> also runs when the collect step first activates, before
        # the user has answered. Do nothing while the slot is empty so the step
        # asks normally, instead of rejecting a value that was never given.
        if not isinstance(raw, str) or not raw.strip():
            return []

        parsed = _parse_full_date(raw, datetime.now())
        if parsed is None:
            # Reject: clearing the slot makes the collect step re-ask the user.
            dispatcher.utter_message(response="utter_invalid_date")
            return [SlotSet("incident_date", None)]

        # Normalize, overwriting whatever the LLM extracted.
        return [SlotSet("incident_date", parsed.strftime(DATE_FORMAT))]
