from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Tuple

from backend.models.state import DailyResult, EvaluationSummary, ProblemResult, UserState


DIFFICULTY_XP = {
    "easy": 50,
    "medium": 120,
    "hard": 240,
}


class Evaluator:
    def evaluate(self, state: UserState, result: DailyResult) -> Tuple[UserState, EvaluationSummary]:
        xp_breakdown: Dict[str, int] = {
            "problem_solving_xp": 0,
            "consistency_xp": 0,
            "challenge_xp": 0,
        }
        notes: List[str] = []
        solved = [problem for problem in result.problems if problem.result == "AC"]
        completion_ratio = self._completion_ratio(result.problems)

        for problem in solved:
            xp = self._base_xp(problem)
            xp_breakdown["problem_solving_xp"] += xp
            if problem.difficulty == "hard":
                xp_breakdown["challenge_xp"] += int(xp * 0.25)
            if problem.hints_used:
                xp_breakdown["problem_solving_xp"] -= int(xp * 0.2)
                notes.append(f"Hints used on {problem.title}: XP reduced.")
            if problem.time_minutes <= 30 and problem.difficulty == "medium":
                xp_breakdown["problem_solving_xp"] += 15

        if completion_ratio >= 0.7:
            xp_breakdown["consistency_xp"] += 40
        elif completion_ratio >= 0.4:
            xp_breakdown["consistency_xp"] += 20
        else:
            notes.append("Low completion ratio detected. Difficulty will be adjusted down.")

        if result.contest_participated:
            xp_breakdown["challenge_xp"] += 100
            notes.append("Contest participation logged.")

        total_xp = sum(xp_breakdown.values())
        state.apply_activity(result.date, completion_ratio)
        state = self._apply_leveling(state, total_xp)
        if completion_ratio < 0.4:
            state = replace(state, difficulty_bias=max(0.8, state.difficulty_bias - 0.1))
        else:
            state = replace(state, difficulty_bias=min(1.2, state.difficulty_bias + 0.05))

        summary = EvaluationSummary(
            date=result.date,
            total_xp=total_xp,
            xp_breakdown=xp_breakdown,
            performance_notes=notes,
            streak_status={
                "daily_streak": state.streak_days,
                "weekly_streak": state.weekly_streak,
            },
            level=state.level,
        )
        return state, summary

    def _base_xp(self, problem: ProblemResult) -> int:
        return DIFFICULTY_XP.get(problem.difficulty, 50)

    def _completion_ratio(self, problems: List[ProblemResult]) -> float:
        if not problems:
            return 0.0
        solved = sum(1 for problem in problems if problem.result == "AC")
        return solved / len(problems)

    def _apply_leveling(self, state: UserState, gained_xp: int) -> UserState:
        level_threshold = 500
        levels_gained = gained_xp // level_threshold
        if levels_gained <= 0:
            return state
        return replace(state, level=state.level + levels_gained)
