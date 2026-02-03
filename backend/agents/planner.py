from __future__ import annotations

from datetime import date
from typing import Dict, List, Tuple

from backend.models.state import DailyPlan, QuestTask, UserState


TOPIC_SEQUENCE: List[Tuple[str, List[str]]] = [
    ("Arrays", ["Two pointers", "Sliding window", "Prefix sums"]),
    ("Hashing", ["Frequency maps", "Set membership"]),
    ("Stacks", ["Monotonic stack", "Bracket matching"]),
    ("Binary Search", ["Lower/upper bound", "Binary search on answer"]),
    ("Trees", ["DFS", "BFS", "Binary lifting"]),
    ("Graphs", ["BFS", "DFS", "Dijkstra"]),
    ("DP", ["1D DP", "2D DP", "Knapsack"]),
]


class DailyPlanner:
    def __init__(self, target_months: int = 6) -> None:
        self.target_months = target_months

    def build_daily_plan(self, state: UserState, plan_date: str | None = None) -> DailyPlan:
        today = plan_date or date.today().isoformat()
        topic_index = state.topic_cursor % len(TOPIC_SEQUENCE)
        topic, subtopics = TOPIC_SEQUENCE[topic_index]
        difficulty_tag = self._difficulty_tag(state)

        main_quests = self._main_quests(topic, subtopics, difficulty_tag)
        side_quests = self._side_quests(topic)
        bonus_quests = self._bonus_quests(difficulty_tag, topic)

        xp_per_task = {
            "easy": 50,
            "medium": 120,
            "hard": 240,
            "review": 40,
            "concept": 60,
            "contest": 300,
        }
        total_xp = sum(task.xp * task.count for task in main_quests + side_quests + bonus_quests)

        return DailyPlan(
            date=today,
            main_quests=main_quests,
            side_quests=side_quests,
            bonus_quests=bonus_quests,
            xp_per_task=xp_per_task,
            total_xp_available=total_xp,
            streak_status={
                "daily_streak": state.streak_days,
                "weekly_streak": state.weekly_streak,
            },
            difficulty_tag=difficulty_tag,
        )

    def _difficulty_tag(self, state: UserState) -> str:
        if state.level <= 2:
            return "easy"
        if state.level <= 5:
            return "normal"
        return "hard"

    def _main_quests(self, topic: str, subtopics: List[str], tag: str) -> List[QuestTask]:
        if tag == "easy":
            return [
                QuestTask(
                    title=f"Solve 2 Easy problems: {topic}",
                    topic=topic,
                    difficulty="easy",
                    count=2,
                    xp=50,
                ),
                QuestTask(
                    title=f"Solve 1 Medium problem: {subtopics[0]}",
                    topic=subtopics[0],
                    difficulty="medium",
                    count=1,
                    xp=120,
                ),
            ]
        if tag == "normal":
            return [
                QuestTask(
                    title=f"Solve 2 Medium problems: {topic}",
                    topic=topic,
                    difficulty="medium",
                    count=2,
                    xp=120,
                ),
                QuestTask(
                    title=f"Solve 1 Medium problem: {subtopics[1]}",
                    topic=subtopics[1],
                    difficulty="medium",
                    count=1,
                    xp=120,
                ),
            ]
        return [
            QuestTask(
                title=f"Solve 2 Medium problems: {topic}",
                topic=topic,
                difficulty="medium",
                count=2,
                xp=120,
            ),
            QuestTask(
                title=f"Solve 1 Hard problem: {subtopics[2]}",
                topic=subtopics[2],
                difficulty="hard",
                count=1,
                xp=240,
            ),
        ]

    def _side_quests(self, topic: str) -> List[QuestTask]:
        return [
            QuestTask(
                title=f"Review one editorial: {topic} patterns", 
                topic=topic,
                difficulty="concept",
                count=1,
                xp=60,
            ),
            QuestTask(
                title="Re-solve 1 previously missed problem",
                topic="Revision",
                difficulty="review",
                count=1,
                xp=40,
            ),
        ]

    def _bonus_quests(self, tag: str, topic: str) -> List[QuestTask]:
        if tag == "hard":
            return [
                QuestTask(
                    title=f"Time-boxed Hard sprint: 1 problem ({topic})",
                    topic=topic,
                    difficulty="hard",
                    count=1,
                    xp=240,
                )
            ]
        return []
