import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/test";

export async function generateTestCases(payload) {
  const response = await axios.post(`${API_BASE_URL}/generate`, payload);
  return response.data;
}

export async function exportExcel(testCases) {
  const response = await axios.post(
    `${API_BASE_URL}/export-excel`,
    {
      test_cases: testCases,
    },
    {
      responseType: "blob",
    }
  );

  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement("a");

  link.href = url;
  link.setAttribute("download", "test_cases.xlsx");
  document.body.appendChild(link);
  link.click();
  link.remove();
}