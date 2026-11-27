from agent import Agent

tests = [
    (
        "Population lookup",
        "What was the population of the United States in 2022?",
        lambda r: r.get("country") == "USA"
        and r.get("year") == 2022
        and isinstance(r.get("value"), (int, float))
    ),
    (
        "Country comparison",
        "Compare the population of the United States and Canada in 2022.",
        lambda r: len(r.get("observations", [])) == 2
        and "difference" in r.get("result", {})
    ),
    (
        "Population change",
        "How did the population of the United States change between 2010 and 2022?",
        lambda r: "percent_change" in r.get("result", {})
    ),
    (
        "Missing information",
        "What was the population?",
        lambda r: r.get("error") == "Please provide more information"
    ),
    (
        "Out-of-scope request",
        "Write me a chocolate cake recipe.",
        lambda r: r.get("error") == "Request outside supported scope"
    )
]

passed = 0

for name, question, check in tests:
    print(f"\nTesting: {name}", flush=True)

    result = Agent().run(question)
    success = check(result)

    if success:
        passed += 1
        print("PASS")
    else:
        print("FAIL")

    print(result)

print(f"\nFinal score: {passed}/{len(tests)}")
print(f"Success rate: {passed / len(tests) * 100:.1f}%")