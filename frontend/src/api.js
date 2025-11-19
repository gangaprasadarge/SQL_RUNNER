const API_BASE = process.env.REACT_APP_API || "https://sql-runner-backend-tr4a.onrender.com/api";

async function request(url, method = "GET", body = null) {
  const token = localStorage.getItem("token");

  const res = await fetch(API_BASE + url, {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: token ? `Bearer ${token}` : "",
    },
    body: body ? JSON.stringify(body) : null,
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}

export async function login(email, password) {
  return request("/login/", "POST", { email, password });
}

export async function signup(name, email, password) {
  return request("/signup/", "POST", { name, email, password });
}

export async function getProfile() {
  return request("/profile/", "GET");
}

export async function fetchTables() {
  return request("/list-tables/", "GET");
}

export async function fetchTableInfo(table) {
  return request(`/table-info/${table}/`, "GET");
}

export async function runQuery(query) {
  return request("/run-query/", "POST", { query });
}
