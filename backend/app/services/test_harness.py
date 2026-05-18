def is_empty(value):
    return value is None or value == ""


def contains_special_chars(value):
    if not isinstance(value, str):
        return False

    dangerous_chars = ["'", '"', "--", ";", " OR ", " or ", "<script", "</script>"]

    for item in dangerous_chars:
        if item in value:
            return True

    return False


def validate_field(field: dict, value):
    name = field.get("name")
    field_type = field.get("type", "string")

    if field.get("required", False) and is_empty(value):
        return {
            "actual_output": f"{name}_empty",
            "branch": f"{name.upper()}_EMPTY",
        }

    if is_empty(value):
        return None

    if field.get("check_special_chars", False) and contains_special_chars(value):
        return {
            "actual_output": "special_character_detected",
            "branch": "SPECIAL_CHARACTER_DETECTED",
        }

    if field_type == "email":
        if not isinstance(value, str) or "@" not in value or "." not in value:
            return {
                "actual_output": "invalid_email",
                "branch": "INVALID_EMAIL",
            }

    if field_type == "string":
        if "min_length" in field and len(str(value)) < field["min_length"]:
            return {
                "actual_output": f"{name}_too_short",
                "branch": f"{name.upper()}_TOO_SHORT",
            }

        if "max_length" in field and len(str(value)) > field["max_length"]:
            return {
                "actual_output": f"{name}_too_long",
                "branch": f"{name.upper()}_TOO_LONG",
            }

    if field_type in ["number", "integer"]:
        try:
            numeric_value = float(value)
        except Exception:
            return {
                "actual_output": f"invalid_{name}",
                "branch": f"INVALID_{name.upper()}",
            }

        if "min" in field and numeric_value < field["min"]:
            return {
                "actual_output": f"invalid_{name}",
                "branch": f"{name.upper()}_LESS_THAN_MIN",
            }

        if "max" in field and numeric_value > field["max"]:
            return {
                "actual_output": f"invalid_{name}",
                "branch": f"{name.upper()}_GREATER_THAN_MAX",
            }

    if field_type == "enum":
        allowed_values = field.get("allowed_values", [])

        if value not in allowed_values:
            return {
                "actual_output": f"invalid_{name}",
                "branch": f"INVALID_{name.upper()}",
            }

    return None


def execute_test_case(schema: dict, test_case: dict):
    fields = schema.get("fields", [])
    success_output = schema.get("success_output", "success")

    for field in fields:
        name = field.get("name")
        value = test_case.get(name)

        error = validate_field(field, value)

        if error:
            actual_output = error["actual_output"]
            branch = error["branch"]

            return {
                **test_case,
                "actual_output": actual_output,
                "branch": branch,
                "passed": actual_output == test_case.get("expected_output"),
            }

    return {
        **test_case,
        "actual_output": success_output,
        "branch": "SUCCESS",
        "passed": success_output == test_case.get("expected_output"),
    }


def execute_test_suite(schema: dict, test_cases: list):
    executed = []

    for index, test_case in enumerate(test_cases):
        copied = dict(test_case)
        copied["id"] = index + 1
        executed.append(execute_test_case(schema, copied))

    return executed