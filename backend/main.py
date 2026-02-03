from __future__ import annotations

import argparse
import json

from backend.models.state import DailyResult, ProblemResult, UserState
from backend.services.system import DEFAULT_SYSTEM


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Solo Leveling System backend")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("daily", help="Generate today's daily plan")

    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate a day's results")
    evaluate_parser.add_argument("--date", required=True)
    evaluate_parser.add_argument("--results", required=True, help="JSON array of problem results")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "daily":
        plan = DEFAULT_SYSTEM.generate_daily_plan()
        print(json.dumps(plan.to_json(), indent=2))
        return

    if args.command == "evaluate":
        results_payload = json.loads(args.results)
        problems = [
            ProblemResult(
                title=item["title"],
                difficulty=item["difficulty"],
                time_minutes=item["time_minutes"],
                hints_used=item.get("hints_used", False),
                result=item["result"],
            )
            for item in results_payload
        ]
        daily_result = DailyResult(date=args.date, problems=problems)
        state = UserState()
        updated_state, summary = DEFAULT_SYSTEM.evaluate_day(state, daily_result)
        print(json.dumps({"summary": summary, "state": updated_state.to_json()}, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
