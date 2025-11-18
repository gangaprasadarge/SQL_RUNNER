import React, { useState } from "react";
import { signup } from "../users_api";
import "./AuthPage.css";

export default function SignupPage({ onSignupSuccess }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");

  async function handleSignup(e) {
    e.preventDefault();
    setError("");

    if (password !== confirm) {
      setError("Passwords do not match");
      return;
    }

    const res = await signup(name, email, password);

    if (res.success) {
      alert("Account created successfully! Please login.");
      onSignupSuccess();
    } else {
      setError(res.error || "Signup failed");
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Create Account</h2>

        {error && <p className="auth-error">{error}</p>}

        <form onSubmit={handleSignup}>
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Create Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Confirm Password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />

          <button type="submit">Sign Up</button>
        </form>

        <p className="toggle-text">
          Already have an account? <span onClick={onSignupSuccess}>Login</span>
        </p>
      </div>
    </div>
  );
}
