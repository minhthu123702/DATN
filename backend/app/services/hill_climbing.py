from app.services.test_harness import execute_test_suite
from app.services.fitness_service import calculate_fitness


def base_valid_case(schema: dict):
    case = {
        "id": 0,
        "expected_output": schema.get("success_output", "success"),
        "description": "Base valid case for Hill Climbing",
    }

    for field in schema.get("fields", []):
        name = field["name"]
        field_type = field.get("type", "string")

        if field_type == "email":
            case[name] = "user@gmail.com"
        elif field_type in ["number", "integer"]:
            case[name] = max(field.get("min", 1), 1)
        elif field_type == "boolean":
            case[name] = True
        elif field_type == "enum":
            values = field.get("allowed_values", ["valid"])
            case[name] = values[0]
        else:
            min_length = field.get("min_length", 3)
            case[name] = "x" * max(min_length, 3)

    return case


def local_candidates_for_field(schema: dict, field: dict):
    candidates = []

    name = field["name"]
    field_type = field.get("type", "string")

    base = base_valid_case(schema)

    if field.get("required", False):
        case = dict(base)
        case[name] = ""
        case["expected_output"] = f"{name}_empty"
        case["description"] = f"HC: empty value for {name}"
        candidates.append(case)

    if field.get("check_special_chars", False):
        case = dict(base)
        case[name] = "' OR '1'='1"
        case["expected_output"] = "special_character_detected"
        case["description"] = f"HC: special character for {name}"
        candidates.append(case)

    if field_type == "email":
        case = dict(base)
        case[name] = "abc.com"
        case["expected_output"] = "invalid_email"
        case["description"] = f"HC: invalid email for {name}"
        candidates.append(case)

    if field_type == "string":
        if "min_length" in field:
            case = dict(base)
            case[name] = "a"
            case["expected_output"] = f"{name}_too_short"
            case["description"] = f"HC: too short value for {name}"
            candidates.append(case)

        if "max_length" in field:
            case = dict(base)
            case[name] = "x" * (field["max_length"] + 5)
            case["expected_output"] = f"{name}_too_long"
            case["description"] = f"HC: too long value for {name}"
            candidates.append(case)

    if field_type in ["number", "integer"]:
        if "min" in field:
            case = dict(base)
            case[name] = field["min"] - 1
            case["expected_output"] = f"invalid_{name}"
            case["description"] = f"HC: smaller than min for {name}"
            candidates.append(case)

        if "max" in field:
            case = dict(base)
            case[name] = field["max"] + 1
            case["expected_output"] = f"invalid_{name}"
            case["description"] = f"HC: greater than max for {name}"
            candidates.append(case)

    if field_type == "enum":
        case = dict(base)
        case[name] = "invalid_enum_value"
        case["expected_output"] = f"invalid_{name}"
        case["description"] = f"HC: invalid enum for {name}"
        candidates.append(case)

    return candidates


def build_local_candidates(schema: dict):
    candidates = [base_valid_case(schema)]

    for field in schema.get("fields", []):
        candidates.extend(local_candidates_for_field(schema, field))

    return candidates


def run_hill_climbing(schema: dict, test_cases: list):
    current_suite = list(test_cases)
    current_fitness = calculate_fitness(schema, execute_test_suite(schema, current_suite))

    local_candidates = build_local_candidates(schema)

    for candidate in local_candidates:
        neighbor_suite = current_suite + [candidate]
        neighbor_fitness = calculate_fitness(schema, execute_test_suite(schema, neighbor_suite))

        if neighbor_fitness > current_fitness:
            current_suite = neighbor_suite
            current_fitness = neighbor_fitness

        if current_fitness >= 100:
            break

    final_suite = []
    seen = set()

    for case in current_suite:
        key = str(sorted(case.items()))

        if key not in seen:
            seen.add(key)
            final_suite.append(case)

    return final_suite