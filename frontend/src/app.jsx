import { useState } from "react";
import { generateTestCases, exportExcel } from "./api";

import InputPanel from "./components/InputPanel";
import ResultPanel from "./components/ResultPanel";
import TestCaseTable from "./components/TestCaseTable";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleGenerate(inputData) {
    try {
      setLoading(true);
      setResult(null);

      const data = await generateTestCases(inputData);
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Lỗi khi gọi backend. Vui lòng kiểm tra FastAPI đã chạy chưa.");
    } finally {
      setLoading(false);
    }
  }

  async function handleExport() {
    if (!result || !result.test_cases) {
      alert("Chưa có dữ liệu kiểm thử để xuất Excel.");
      return;
    }

    await exportExcel(result.test_cases);
  }

  return (
    <div className="app">
      <header className="hero">
        <p className="tag">LLM + GA + Hill Climbing + Test Harness</p>

        <h1>Hệ thống tự động sinh dữ liệu kiểm thử</h1>

        <p>
          Hệ thống cho phép nhập yêu cầu chức năng bằng ngôn ngữ tự nhiên.
          Mô hình ngôn ngữ lớn sẽ tự phân tích yêu cầu, sinh dữ liệu kiểm thử ban đầu,
          sau đó Genetic Algorithm và Hill Climbing tối ưu để tạo ra bộ test data tốt hơn.
        </p>
      </header>

      <main className="layout">
        <InputPanel onGenerate={handleGenerate} loading={loading} />

        <section className="right-panel">
          {result ? (
            <>
              <ResultPanel result={result} onExport={handleExport} />
              <TestCaseTable testCases={result.test_cases} />
            </>
          ) : (
            <div className="empty-card">
              <h2>Chưa có kết quả</h2>
              <p>
                Nhập yêu cầu chức năng ở khung bên trái, sau đó bấm
                <b> Sinh dữ liệu kiểm thử</b>. Hệ thống sẽ tự phân tích yêu cầu,
                sinh test case và tối ưu bằng GA kết hợp Hill Climbing.
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}