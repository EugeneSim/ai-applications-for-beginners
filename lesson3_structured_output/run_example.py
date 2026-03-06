"""
Lesson 3 demo: structured output extraction.

Extract typed Pydantic objects from text using
agent(prompt, structured_output_model=MyModel).

Usage:
  python run_example.py
  python run_example.py "Eugene Sim is an aspiring data engineer based in Singapore."
  python run_example.py --meeting "Daily standup, March 6, 2025. Attendees: Eugene, Priya. Actions: send report."
"""

import argparse

from structured_agent import (
    MeetingSummary,
    PersonInfo,
    extract_meeting,
    extract_person,
)

PERSON_SAMPLE = "Eugene Sim, 28, is an aspiring data engineer based in Singapore."
MEETING_SAMPLE = (
    "Daily standup, March 6, 2025 at 10am in Room Singapore. "
    "Attendees: Eugene, Priya. Actions: send sprint report, update backlog."
)


def _print_person(person: PersonInfo) -> None:
    """Print PersonInfo fields (handles None)."""
    print("Structured output (PersonInfo):")
    print(f"  name: {person.name}")
    print(f"  age: {person.age}")
    print(f"  occupation: {person.occupation}")
    print(f"  location: {person.location}")


def _print_meeting(summary: MeetingSummary) -> None:
    """Print MeetingSummary fields."""
    print("Structured output (MeetingSummary):")
    print(f"  title: {summary.title}")
    print(f"  date: {summary.date}")
    print(f"  participants: {summary.participants}")
    print(f"  action_items: {summary.action_items}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract PersonInfo or MeetingSummary from text.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to extract from (optional; without it, runs built-in samples).",
    )
    parser.add_argument(
        "--meeting",
        "-m",
        action="store_true",
        help="Extract as MeetingSummary instead of PersonInfo.",
    )
    args = parser.parse_args()

    if args.text:
        if args.meeting:
            print("Extracting MeetingSummary...\n")
            _print_meeting(extract_meeting(args.text))
        else:
            print("Extracting PersonInfo...\n")
            _print_person(extract_person(args.text))
        return

    # No text: run both samples
    print("=== PersonInfo sample ===\n")
    print("Text:", PERSON_SAMPLE)
    _print_person(extract_person(PERSON_SAMPLE))

    print("\n=== MeetingSummary sample ===\n")
    print("Text:", MEETING_SAMPLE)
    _print_meeting(extract_meeting(MEETING_SAMPLE))


if __name__ == "__main__":
    main()
