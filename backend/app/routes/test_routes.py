from typing import Optional, Dict, Any, List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.gemini_service import generate_test_plan
from app.services.optimizer_service import optimize_test_cases
from app.services.test_harness import execute_test_suite
from app.services.fitness_service import evaluate_suite
from app.services.export_service import export_to_excel

router = APIRouter()


class GenerateRequest(BaseModel):
    input_type: str = "requirement"
    content: str
    project_name: Optional[str] = "Generic Project"
    function_name: Optional[str] = "auto_detect"
    input_schema: Optional[Dict[str, Any]] = None


class ExportRequest(BaseModel):
    test_cases: List[Dict[str, Any]]


@router.post("/generate")
def generate_test_cases(request: GenerateRequest):
    test_plan = generate_test_plan(
        input_type=request.input_type,
        content=request.content,
        project_name=request.project_name,
        function_name=request.function_name or "auto_detect",
        input_schema=request.input_schema,
    )

    schema = test_plan["schema"]
    initial_cases = test_plan["test_cases"]

    optimized_cases = optimize_test_cases(
        schema=schema,
        initial_cases=initial_cases,
    )

    executed_cases = execute_test_suite(
        schema=schema,
        test_cases=optimized_cases,
    )

    metrics = evaluate_suite(
        schema=schema,
        test_cases=executed_cases,
    )

    return {
        "project_name": request.project_name,
        "function_name": schema.get("function_name", request.function_name),
        "input_type": request.input_type,
        "schema": schema,
        "initial_count": len(initial_cases),
        "optimized_count": len(optimized_cases),
        "fitness": metrics["fitness"],
        "coverage": metrics["coverage"],
        "covered_outputs": metrics["covered_outputs"],
        "total_outputs": metrics["total_outputs"],
        "test_cases": executed_cases,
    }


@router.post("/export-excel")
def export_excel(request: ExportRequest):
    file_stream = export_to_excel(request.test_cases)

    return StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=test_cases.xlsx"
        },
    )