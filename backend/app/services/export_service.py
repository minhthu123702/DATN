from io import BytesIO
from openpyxl import Workbook


def export_to_excel(test_cases: list):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Test Cases"

    headers = [
        "ID",
        "Username",
        "Password",
        "Expected Output",
        "Actual Output",
        "Branch",
        "Passed",
        "Description",
    ]

    sheet.append(headers)

    for item in test_cases:
        sheet.append(
            [
                item.get("id", ""),
                item.get("username", ""),
                item.get("password", ""),
                item.get("expected_output", ""),
                item.get("actual_output", ""),
                item.get("branch", ""),
                item.get("passed", ""),
                item.get("description", ""),
            ]
        )

    for column_cells in sheet.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter

        for cell in column_cells:
            value = str(cell.value) if cell.value is not None else ""
            max_length = max(max_length, len(value))

        sheet.column_dimensions[column_letter].width = max_length + 3

    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)

    return stream