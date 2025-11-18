import React, { useState } from "react";
import { login, signup, forgotPassword } from "../users_api";
import "./AuthPage.css";
import { useNavigate } from "react-router-dom";
import logo from "../assets/sql-logo.webp";

const LOGO_FALLBACK = "/logo192.png";

export default function AuthPage({ onLogin }) {
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);
  const [forgotMode, setForgotMode] = useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");

  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (forgotMode) {
      const res = await forgotPassword(email);
      if (res.success) {
        alert("Password reset link sent!");
        setForgotMode(false);
      } else {
        setError(res.error || "Unable to send reset link");
      }
      return;
    }

    if (isLogin) {
      try {
        const res = await login(email, password);
        if (res && res.access) {
          onLogin(res.access, res.refresh);
          navigate("/");
        } else {
          setError(res && res.error ? res.error : "Invalid login credentials");
        }
      } catch (err) {
        setError("Login failed. Check network/console for details.");
      }
      return;
    }

    if (!name.trim()) {
      setError("Name is required");
      return;
    }

    if (password !== confirm) {
      setError("Passwords do not match");
      return;
    }

    const res = await signup(name, email, password);
    if (res.success) {
      alert("Signup successful!");
      setIsLogin(true);
    } else {
      setError(res.error || "Signup failed");
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-left">
        <img
          src={logo}
          alt="Logo"
          className="auth-logo"
          onError={(e) => {
            e.currentTarget.onerror = null;
            e.currentTarget.src = LOGO_FALLBACK;
          }}
        />
      </div>

      <div className="auth-right">
        <div className="auth-box">
          <h1 className="auth-title">
            {forgotMode ? "Forgot Password" : isLogin ? "Login" : "Sign Up"}
          </h1>

          {error && <p className="auth-error">{error}</p>}

          <form onSubmit={handleSubmit}>
            {!isLogin && !forgotMode && (
              <input
                type="text"
                placeholder="Full Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            )}

            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            {!forgotMode && (
              <>
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />

                {!isLogin && (
                  <input
                    type="password"
                    placeholder="Confirm Password"
                    value={confirm}
                    onChange={(e) => setConfirm(e.target.value)}
                    required
                  />
                )}
              </>
            )}

            <button type="submit" className="auth-btn">
              {forgotMode
                ? "Send Reset Link"
                : isLogin
                ? "Login"
                : "Create Account"}
            </button>
          </form>

          {isLogin && !forgotMode && (
            <p className="auth-forgot" onClick={() => setForgotMode(true)}>
              Forgot Password?
            </p>
          )}

          {!forgotMode && (
            <p className="auth-toggle">
              {isLogin ? "Don't have an account?" : "Already registered?"}
              <span onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? " Sign Up" : " Login"}
              </span>
            </p>
          )}

          {forgotMode && (
            <p className="auth-toggle">
              <span onClick={() => setForgotMode(false)}>Back to Login</span>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
