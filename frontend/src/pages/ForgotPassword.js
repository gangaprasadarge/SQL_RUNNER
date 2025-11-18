import React, { useState } from "react";
import { sendResetOTP } from "../users_api";

export default function ForgotPassword({ onNext }) {
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");

  async function handleSendOTP() {
    const res = await sendResetOTP(username);
    if (res.success) onNext(username);
    else setError(res.error);
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Forgot Password</h2>

        {error && <p className="auth-error">{error}</p>}

        <input
          placeholder="Enter Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <button onClick={handleSendOTP}>Send OTP</button>
      </div>
    </div>
  );
}
