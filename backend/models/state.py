from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional


@dataclass
class QuestTask:
    title: str
    topic: str
    difficulty: str
    count: int
    xp: int


@dataclass
class DailyPlan:
    date: str
    main_quests: List[QuestTask]
    side_quests: List[QuestTask]
    bonus_quests: List[QuestTask]
    xp_per_task: Dict[str, int]
    total_xp_available: int
    streak_status: Dict[str, int]
    difficulty_tag: str

    def to_json(self) -> Dict[str, object]:
        return {
            "date": self.date,
            "main_quests": [task.__dict__ for task in self.main_quests],
            "side_quests": [task.__dict__ for task in self.side_quests],
            "bonus_quests": [task.__dict__ for task in self.bonus_quests],
            "xp_per_task": self.xp_per_task,
            "total_xp_available": self.total_xp_available,
            "streak_status": self.streak_status,
            "difficulty_tag": self.difficulty_tag,
        }


@dataclass
class ProblemResult:
    title: str
    difficulty: str
    time_minutes: int
    hints_used: bool
    result: str


@dataclass
class DailyResult:
    date: str
    problems: List[ProblemResult]
    contest_participated: bool = False
    contest_rank: Optional[int] = None


@dataclass
class EvaluationSummary:
    date: str
    total_xp: int
    xp_breakdown: Dict[str, int]
    performance_notes: List[str]
    streak_status: Dict[str, int]
    level: int

    def to_json(self) -> Dict[str, object]:
        return {
            "date": self.date,
            "total_xp": self.total_xp,
            "xp_breakdown": self.xp_breakdown,
            "performance_notes": self.performance_notes,
            "streak_status": self.streak_status,
            "level": self.level,
        }


@dataclass
class UserState:
    level: int = 1
    streak_days: int = 0
    weekly_streak: int = 0
    last_active_date: Optional[str] = None
    topic_cursor: int = 0
    difficulty_bias: float = 1.0
    heatmap: Dict[str, float] = field(default_factory=dict)

    def apply_activity(self, activity_date: str, completion_ratio: float) -> None:
        self.heatmap[activity_date] = completion_ratio
        if self.last_active_date == activity_date:
            return
        if self.last_active_date:
            last = date.fromisoformat(self.last_active_date)
            current = date.fromisoformat(activity_date)
            if (current - last).days == 1:
                self.streak_days += 1
            else:
                self.streak_days = 1
        else:
            self.streak_days = 1
        self.weekly_streak = min(self.streak_days, 7)
        self.last_active_date = activity_date

    def to_json(self) -> Dict[str, object]:
        return {
            "level": self.level,
            "streak_days": self.streak_days,
            "weekly_streak": self.weekly_streak,
            "last_active_date": self.last_active_date,
            "topic_cursor": self.topic_cursor,
            "difficulty_bias": self.difficulty_bias,
            "heatmap": self.heatmap,
        }
