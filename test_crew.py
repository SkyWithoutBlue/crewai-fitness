import os
import sys
import io
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

print("Initializing LLM...")
llm = LLM(model="gemini/gemini-2.5-flash", api_key=key)

print("Creating Agent...")
agent = Agent(
    role="Test Agent",
    goal="Answer questions clearly",
    backstory="You are a helpful assistant",
    llm=llm,
    verbose=True
)

print("Creating Task...")
task = Task(
    description="Explain gravity in one sentence.",
    expected_output="A single sentence explanation.",
    agent=agent
)

print("Creating Crew...")
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

try:
    print("Running Crew...")
    result = crew.kickoff()
    print("RESULT SUCCESS:")
    print(result)
except Exception as e:
    print("RESULT ERROR:")
    import traceback
    traceback.print_exc()
