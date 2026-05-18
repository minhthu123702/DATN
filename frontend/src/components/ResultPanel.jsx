export default function ResultPanel({ result, onExport }) {
  return (
    <section className="card result-panel">
      <div className="result-header">
        <div>
          <h2>Kết quả tối ưu</h2>
          <p>
            Project: <b>{result.project_name}</b> | Function:{" "}
            <b>{result.function_name}</b>
          </p>
        </div>

        <button className="secondary-btn" onClick={onExport}>
          Xuất Excel
        </button>
      </div>

      <div className="metric-grid">
        <div className="metric-card">
          <span>Fitness</span>
          <strong>{result.fitness}%</strong>
        </div>

        <div className="metric-card">
          <span>Output Coverage</span>
          <strong>{Math.round(result.coverage * 100)}%</strong>
        </div>

        <div className="metric-card">
          <span>Initial Cases</span>
          <strong>{result.initial_count}</strong>
        </div>

        <div className="metric-card">
          <span>Optimized Cases</span>
          <strong>{result.optimized_count}</strong>
        </div>
      </div>

      <div className="branches">
        <h3>Output đã bao phủ</h3>

        <div className="branch-list">
          {result.covered_outputs && result.covered_outputs.length > 0 ? (
            result.covered_outputs.map((output) => (
              <span key={output}>{output}</span>
            ))
          ) : (
            <p>Chưa có output nào được bao phủ.</p>
          )}
        </div>
      </div>

      <details className="schema-preview">
        <summary>Xem schema hệ thống đang dùng</summary>
        <pre>{JSON.stringify(result.schema, null, 2)}</pre>
      </details>
    </section>
  );
}