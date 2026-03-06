"""
One-shot example: run the weather agent on a single question.
Set GROQ_API_KEY in the repo root .env (free at https://console.groq.com), then:
  python run_example.py
  python run_example.py "What's the weather in Tokyo?"
"""

import sys
from weather_agent import create_weather_agent

def main():
    question = sys.argv[1] if len(sys.argv) > 1 else "What's the weather in London?"
    agent = create_weather_agent()
    print(f"Question: {question}\n")
    response = agent(question)
    print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
