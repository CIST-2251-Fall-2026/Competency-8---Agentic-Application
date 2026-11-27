import json
import ollama
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
from tools import (
    INDICATORS,
    find_indicator,
    get_data,
    compare_values,
    calculate_change
)

MODEL = "qwen3:4b"


class AgentPlan(BaseModel):
    action: Literal[
        "lookup", "compare", "change", "clarify", "refuse"
    ]
    indicator: str = Field(description="Supported World Bank indicator code")
    countries: list[str] = Field(max_length=2)
    years: list[int] = Field(
    max_length=2,
    description="Complete four-digit years, such as 2010 and 2022"
)


def log(event, data):
    with open("trajectory.jsonl", "a") as file:
        file.write(json.dumps({
            "time": datetime.now().isoformat(),
            "event": event,
            "data": data
        }) + "\n")


class Agent:
    def __init__(self):
        self.context = {}

    def run(self, question, offline=False):
        log("question", question)

        prompt = f"""
        You are a World Bank research assistant.
        Supported indicators: {INDICATORS}
        Always select the correct indicator code from the supported indicators.
        Population uses SP.POP.TOTL.
        Never leave the indicator empty for lookup, compare, or change.
        Return all required fields in the structured plan.
        Previous context: {self.context}

        Use ISO three-letter country codes.
        United States = USA, Canada = CAN, Mexico = MEX.
        China = CHN, India = IND, Japan = JPN.
        Always populate the countries list when a country is mentioned.
        Always populate the years list when a year is mentioned.
        Never leave required parameters empty.
        Use clarify if required information is missing.
        Use lookup for one country and year.
        Use compare for two countries in the same year.
        Use change for one country across two years.
        Clarify missing information.
        Use refuse for any question unrelated to World Bank data.
        Examples of unrelated requests include recipes, jokes, and stories.
        Use clarify only for World Bank questions with missing information.
        Prioritize refuse over clarify for unrelated requests.
        Never invent data.
        Always use complete four-digit years.
        Never shorten or truncate a year.
        For a change between 2010 and 2022, return years [2010, 2022].

        Question: {question}
        """

        try:
            response = ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                format=AgentPlan.model_json_schema(),
                think=False,
                options={"temperature": 0}
            )

            plan = AgentPlan.model_validate_json(
                response.message.content
            )

            log("plan", plan.model_dump())

            result = self.execute(plan, offline)
            log("result", result)

            if "error" not in result:
                self.context = plan.model_dump()

            return result

        except Exception as error:
            log("error", str(error))
            return {"error": str(error)}

    def execute(self, plan, offline):
        if plan.action == "refuse":
            return {"error": "Request outside supported scope"}

        if plan.action == "clarify":
            return {"error": "Please provide more information"}

        matches = find_indicator(plan.indicator)

        if not plan.indicator or len(matches) != 1:
            return {"error": "Unknown or ambiguous indicator"}

        indicator = next(iter(matches))

        expected = {
            "lookup": (1, 1),
            "compare": (2, 1),
            "change": (1, 2)
        }

        if (len(plan.countries), len(plan.years)) != expected[plan.action]:
            return {"error": "Missing or invalid parameters"}

        def retrieve(country, year):
            result = get_data(country, indicator, year, offline)
            log("get_data", result)
            return result

        first = retrieve(plan.countries[0], plan.years[0])

        if "error" in first or plan.action == "lookup":
            return first

        if plan.action == "compare":
            second = retrieve(plan.countries[1], plan.years[0])
        else:
            second = retrieve(plan.countries[0], plan.years[1])

        if "error" in second:
            return second

        if plan.action == "compare":
            result = compare_values(first["value"], second["value"])
        else:
            result = calculate_change(first["value"], second["value"])

        log(plan.action, result)

        return {
            "observations": [first, second],
            "result": result
        }


if __name__ == "__main__":
    agent = Agent()

    print("World Bank Research Assistant")
    print("Type exit to quit.")

    while True:
        question = input("\nAsk a question: ")

        if question.lower() == "exit":
            break

        print(json.dumps(agent.run(question), indent=2))