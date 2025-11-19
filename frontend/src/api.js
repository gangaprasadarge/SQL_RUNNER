const API_BASE = process.env.REACT_APP_API_URL;

function authHeader() {
  return {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  };
}

async function request(url, method = "GET", body = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      ...authHeader(),
    },
  };
  if (body) options.body = JSON.stringify(body);

  const res = await fetch(`${API_BASE}${url}`, options);

  if (res.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
    window.location.href = "/login";
    return;
  }

  return res.json();
}

export async function login(data) {
  return request("/login/", "POST", data);
}

export async function signup(data) {
  return request("/signup/", "POST", data);
}

export async function runQuery(query) {
  return request("/run-query/", "POST", { query });
}

export async function listTables() {
  return request("/list-tables/", "GET");
}

export async function tableInfo(table) {
  return request(`/table-info/${table}/`, "GET");
}

export async function getProfile() {
  return request("/profile/", "GET");
}
