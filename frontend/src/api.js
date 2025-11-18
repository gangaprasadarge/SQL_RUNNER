const API_BASE = process.env.REACT_APP_API_BASE;
// const API_BASE = "http://localhost:8000/api";

function authHeader() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function refreshToken() {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) return null;

  try {
    const res = await fetch(`${API_BASE}/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh }),
    });

    if (!res.ok) return null;

    const data = await res.json();
    if (data.access) {
      localStorage.setItem("token", data.access);
      return data.access;
    }
  } catch (_) {
    return null;
  }

  return null;
}

async function handle401(originalRequest) {
  const newToken = await refreshToken();
  if (newToken) return originalRequest();
  localStorage.removeItem("token");
  localStorage.removeItem("refresh");
  window.location.href = "/login";
  return null;
}

export async function runQuery(query) {
  const request = () =>
    fetch(`${API_BASE}/run_query/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeader(),
      },
      body: JSON.stringify({ query }),
    });

  let res = await request();
  if (res.status === 401) return handle401(() => runQuery(query));
  return res.json();
}

export async function fetchTables() {
  const request = () =>
    fetch(`${API_BASE}/tables/`, { headers: authHeader() });

  let res = await request();
  if (res.status === 401) return handle401(() => fetchTables());
  return res.json();
}

export async function fetchTableInfo(table) {
  const request = () =>
    fetch(`${API_BASE}/table_info/${table}/`, { headers: authHeader() });

  let res = await request();
  if (res.status === 401) return handle401(() => fetchTableInfo(table));
  return res.json();
}

export async function getProfile() {
  const request = () =>
    fetch(`${API_BASE}/profile/`, { headers: authHeader() });

  let res = await request();
  if (res.status === 401) return handle401(() => getProfile());
  return res.json();
}
