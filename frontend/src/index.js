import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { BrowserRouter, Routes, Route, useParams } from "react-router-dom";
import AuthPage from "./pages/AuthPage";
import ResetPassword from "./pages/ResetPassword";
import ProtectedRoute from "./components/ProtectedRoute";

function ResetWrapper() {
  const { uid, token } = useParams();
  return <ResetPassword uid={uid} token={token} />;
}

function LoginWrapper() {
  function handleLogin(access, refresh) {
    localStorage.setItem("token", access);
    localStorage.setItem("refresh", refresh);
    window.location.href = "/";
  }
  return <AuthPage onLogin={handleLogin} />;
}

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/login" element={<LoginWrapper />} />
      <Route path="/reset-password/:uid/:token" element={<ResetWrapper />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <App />
          </ProtectedRoute>
        }
      />
    </Routes>
  </BrowserRouter>
);
