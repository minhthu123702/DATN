const columnLabels = {
  id: "STT",
  input: "Đầu vào",
  expected_output: "Kết quả mong đợi",
  actual_output: "Kết quả thực tế",
  branch: "Nhánh kiểm thử",
  passed: "Trạng thái",
  description: "Mô tả",
  username: "Tên đăng nhập",
  password: "Mật khẩu",
  email: "Email",
  confirm_password: "Xác nhận mật khẩu",
  keyword: "Từ khóa",
  role: "Vai trò",
  status: "Trạng thái tài khoản",
  name: "Tên",
  phone: "Số điện thoại",
  address: "Địa chỉ",
  quantity: "Số lượng",
  price: "Giá",
  product_id: "Mã sản phẩm",
  payment_method: "Phương thức thanh toán",
  employee_code: "Mã nhân viên",
};

function getColumns(testCases) {
  const priority = [
    "id",
    "expected_output",
    "actual_output",
    "branch",
    "passed",
    "description",
  ];

  const allKeys = new Set();

  testCases.forEach((item) => {
    Object.keys(item).forEach((key) => allKeys.add(key));
  });

  const dynamicKeys = Array.from(allKeys).filter(
    (key) => !priority.includes(key)
  );

  return [
    "id",
    ...dynamicKeys,
    "expected_output",
    "actual_output",
    "branch",
    "passed",
    "description",
  ].filter((key) => allKeys.has(key));
}

function renderValue(value) {
  if (typeof value === "boolean") {
    return value ? "Đúng" : "Sai";
  }

  if (value === null || value === undefined) {
    return "";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

function getColumnLabel(column) {
  return columnLabels[column] || column;
}

export default function TestCaseTable({ testCases }) {
  if (!testCases || testCases.length === 0) {
    return (
      <section className="card table-card">
        <h2>Bảng dữ liệu kiểm thử</h2>
        <p>Không có test case.</p>
      </section>
    );
  }

  const columns = getColumns(testCases);

  return (
    <section className="card table-card">
      <h2>Bảng dữ liệu kiểm thử tối ưu</h2>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column}>{getColumnLabel(column)}</th>
              ))}
            </tr>
          </thead>

          <tbody>
            {testCases.map((item, index) => (
              <tr key={index}>
                {columns.map((column) => (
                  <td key={column}>
                    {column === "passed" ? (
                      <span className={item.passed ? "pass" : "fail"}>
                        {item.passed ? "ĐẠT" : "KIỂM TRA"}
                      </span>
                    ) : (
                      renderValue(item[column])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}