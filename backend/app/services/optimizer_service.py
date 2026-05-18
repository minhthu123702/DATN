from app.services.genetic_algorithm import run_genetic_algorithm
from app.services.hill_climbing import run_hill_climbing


def optimize_test_cases(schema: dict, initial_cases: list):
    ga_result = run_genetic_algorithm(
        schema=schema,
        initial_cases=initial_cases,
    )

    hc_result = run_hill_climbing(
        schema=schema,
        test_cases=ga_result,
    )

    for index, item in enumerate(hc_result):
        item["id"] = index + 1

    return hc_result