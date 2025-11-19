import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { resetPassword } from "../users_api";
import "./AuthPage.css";

export default function ResetPassword({ uid, token }) {
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");

  async function handleReset() {
    setError("");
    const res = await resetPassword(uid, token, password);

    if (res.success) {
      setMsg("Password updated! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1500);
    } else {
      setError(res.error || "Failed to reset password");
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Reset Password</h2>

        {msg && <p className="auth-success">{msg}</p>}
        {error && <p className="auth-error">{error}</p>}

        <input
          type="password"
          placeholder="Enter New Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleReset}>Update Password</button>
      </div>
    </div>
  );
}
