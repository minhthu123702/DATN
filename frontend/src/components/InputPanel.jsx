import { useState } from "react";

const sampleRequirement = ``;

export default function InputPanel({ onGenerate, loading }) {
  const [projectName, setProjectName] = useState("Dự án kiểm thử tự động");
  const [inputType, setInputType] = useState("requirement");
  const [content, setContent] = useState(sampleRequirement);

  function handleSubmit(event) {
    event.preventDefault();

    if (!content.trim()) {
      alert("Vui lòng nhập yêu cầu chức năng cần kiểm thử.");
      return;
    }

    onGenerate({
      input_type: inputType,
      project_name: projectName,
      function_name: "auto_detect",
      content,
      input_schema: null,
    });
  }

  return (
    <section className="card input-panel">
      <h2>Nhập yêu cầu kiểm thử</h2>

      <form onSubmit={handleSubmit}>
        <label>Tên dự án</label>
        <input
          value={projectName}
          onChange={(event) => setProjectName(event.target.value)}
          placeholder="Ví dụ: Hệ thống quản lý người dùng"
        />

        <label>Loại đầu vào</label>
        <select
          value={inputType}
          onChange={(event) => setInputType(event.target.value)}
        >
          <option value="requirement">Yêu cầu chức năng</option>
          <option value="code">Mã nguồn / Hàm cần kiểm thử</option>
          <option value="api">Mô tả API</option>
        </select>

        <label>Yêu cầu chức năng</label>
        <textarea
          className="requirement-only-box"
          value={content}
          onChange={(event) => setContent(event.target.value)}
          placeholder="Nhập yêu cầu chức năng. Hệ thống sẽ tự phân tích field, rule validate và expected output..."
        />

        <button type="submit" disabled={loading}>
          {loading ? "Đang phân tích và sinh dữ liệu..." : "Sinh dữ liệu kiểm thử"}
        </button>
      </form>
    </section>
  );
}