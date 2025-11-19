const API_BASE = "https://sql-runner-backend-tr4a.onrender.com/api";

export async function login(email, password) {
  try {
    console.log("Sending request to:", `${API_BASE}/login/`);
    const res = await fetch(`${API_BASE}/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json().catch(() => null);
    if (res.ok) return data || {};
    return { error: (data && data.detail) || "Login failed" };
  } catch (e) {
    return { error: "Network error. Please check your connection." };
  }
}

export async function signup(name, email, password) {
  try {
    console.log("Sending request to:", `${API_BASE}/signup/`);
    const res = await fetch(`${API_BASE}/signup/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password })
    });

    const data = await res.json().catch(() => null);
    if (res.ok) return data || {};
    return { error: (data && (data.error || data.detail)) || `Request failed (${res.status})` };
  } catch (err) {
    return { error: "Network error. Please check your connection or API URL." };
  }
}

export async function forgotPassword(email) {
  try {
    const res = await fetch(`${API_BASE}/forgot-password/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });

    const data = await res.json().catch(() => null);
    if (res.ok) return data || { success: true };
    return { error: (data && (data.error || data.detail)) || `Request failed (${res.status})` };
  } catch (err) {
    return { error: "Network error. Please check your connection or API URL." };
  }
}

export async function resetPassword(uid, token, new_password) {
  try {
    const res = await fetch(`${API_BASE}/reset-password/${uid}/${token}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ new_password })
    });

    const data = await res.json().catch(() => null);
    if (res.ok) return data || { success: true };
    return { error: (data && (data.error || data.detail)) || `Request failed (${res.status})` };
  } catch (err) {
    return { error: "Network error. Please check your connection or API URL." };
  }
}

export async function refreshToken() {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) return null;

  const res = await fetch(`${API_BASE}/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh })
  });

  const data = await res.json();

  if (data.access) {
    localStorage.setItem("token", data.access);
    return data.access;
  }

  return null;
}
