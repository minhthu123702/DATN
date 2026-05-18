def evaluate_suite(schema: dict, test_cases: list):
    expected_outputs = set(schema.get("expected_outputs", []))

    if not expected_outputs:
        expected_outputs = set()

        for item in test_cases:
            if item.get("expected_output"):
                expected_outputs.add(item.get("expected_output"))

    covered_outputs = set()

    passed_count = 0

    for test_case in test_cases:
        actual_output = test_case.get("actual_output")

        if actual_output:
            covered_outputs.add(actual_output)

        if test_case.get("passed"):
            passed_count += 1

    total_outputs = len(expected_outputs)
    covered_count = len(covered_outputs.intersection(expected_outputs))

    if total_outputs == 0:
        output_coverage = 0
    else:
        output_coverage = covered_count / total_outputs

    if len(test_cases) == 0:
        pass_score = 0
    else:
        pass_score = passed_count / len(test_cases)

    fitness = (0.7 * output_coverage + 0.3 * pass_score) * 100

    return {
        "fitness": round(fitness, 2),
        "coverage": round(output_coverage, 4),
        "covered_outputs": sorted(list(covered_outputs.intersection(expected_outputs))),
        "total_outputs": total_outputs,
    }


def calculate_fitness(schema: dict, test_cases: list):
    return evaluate_suite(schema, test_cases)["fitness"]