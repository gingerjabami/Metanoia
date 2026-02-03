from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Dict, Optional, Tuple

from backend.agents.evaluator import Evaluator
from backend.agents.planner import DailyPlanner
from backend.agents.scheduler import Scheduler
from backend.models.state import DailyPlan, DailyResult, UserState


class SoloLevelingSystem:
    def __init__(self) -> None:
        self.planner = DailyPlanner()
        self.scheduler = Scheduler()
        self.evaluator = Evaluator()

    def generate_daily_plan(self, state: Optional[UserState] = None, plan_date: Optional[str] = None) -> DailyPlan:
        current_state = state or UserState()
        current_state = self.scheduler.apply_daily_reset(current_state, plan_date)
        return self.planner.build_daily_plan(current_state, plan_date)

    def evaluate_day(self, state: UserState, results: DailyResult) -> Tuple[UserState, Dict[str, object]]:
        updated_state, summary = self.evaluator.evaluate(state, results)
        updated_state = self.scheduler.advance_topic(updated_state)
        return updated_state, summary.to_json()

    def serialize_state(self, state: UserState) -> Dict[str, object]:
        return asdict(state)


DEFAULT_SYSTEM = SoloLevelingSystem()


def daily_plan_json(plan_date: Optional[str] = None) -> Dict[str, object]:
    plan = DEFAULT_SYSTEM.generate_daily_plan(plan_date=plan_date)
    return plan.to_json()


def today() -> str:
    return date.today().isoformat()
