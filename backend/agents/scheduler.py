from __future__ import annotations

from dataclasses import replace
from datetime import date
from typing import Optional

from backend.models.state import UserState


class Scheduler:
    def apply_daily_reset(self, state: UserState, today: Optional[str] = None) -> UserState:
        current = today or date.today().isoformat()
        if state.last_active_date is None:
            return state
        last = date.fromisoformat(state.last_active_date)
        now = date.fromisoformat(current)
        if (now - last).days > 1:
            state.streak_days = 0
            state.weekly_streak = 0
        return state

    def advance_topic(self, state: UserState) -> UserState:
        return replace(state, topic_cursor=state.topic_cursor + 1)
