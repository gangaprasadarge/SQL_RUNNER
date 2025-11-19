const API_BASE = process.env.REACT_APP_API_BASE || "https://sql-runner-backend-tr4a.onrender.com/api";

function authHeader() {
  const token = localStorage.getItem("token");
  if (!token) return {};
  return { "Authorization": `Bearer ${token}` };
}

export async function runQuery(query) {
  const request = () => fetch(`${API_BASE}/run-query/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeader()
    },
    body: JSON.stringify({ query })
  });
  const res = await request();
  const data = await res.json();
  return { status: res.status, data };
}

export async function getTables() {
  const res = await fetch(`${API_BASE}/list-tables/`, {
    method: "GET",
    headers: {
      ...authHeader()
    }
  });
  const data = await res.json();
  return { status: res.status, data };
}

export async function getTableInfo(tableName) {
  const res = await fetch(`${API_BASE}/table-info/${encodeURIComponent(tableName)}/`, {
    method: "GET",
    headers: {
      ...authHeader()
    }
  });
  const data = await res.json();
  return { status: res.status, data };
}
