// src/App.js
import "./App.css";
import React, { useEffect, useState, useCallback } from "react";
import QueryEditor from "./components/QueryEditor";
import TableList from "./components/TableList";
import ResultsTable from "./components/ResultsTable";
import {
  runQuery as apiRunQuery,
  fetchTables as apiFetchTables,
  fetchTableInfo as apiFetchTableInfo,
  getProfile as apiGetProfile,
} from "./api";
import SchemaTable from "./components/SchemaTable";
import AuthPage from "./pages/AuthPage";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState(null);
  const [tableInfo, setTableInfo] = useState(null);
  const [history, setHistory] = useState([]);
  const [profile, setProfile] = useState(null);

  const [leftWidth, setLeftWidth] = useState(260);
  const [rightWidth, setRightWidth] = useState(320);
  const [draggingLeft, setDraggingLeft] = useState(false);
  const [draggingRight, setDraggingRight] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // LOGIN
  function handleLogin(access, refresh) {
    localStorage.setItem("token", access);
    localStorage.setItem("refresh", refresh);
    setToken(access);
    setQuery("");
    setHistory([]);
  }

  // LOGOUT
  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
    setToken(null);
    setTables([]);
    setSelectedTable(null);
    setTableInfo(null);
    setProfile(null);
  }

  // LOAD PROFILE + TABLES
  useEffect(() => {
    if (token) {
      loadProfile();
      loadTables();
    }
  }, [token]);

  async function loadProfile() {
    try {
      const p = await apiGetProfile();
      if (p && !p.error) setProfile(p);
    } catch {}
  }

  // LOAD ONLY 3 MAIN TABLES
  async function loadTables() {
  try {
    const r = await apiFetchTables();

    if (r && r.tables) {
      const allowed = ["customers", "orders", "shippings"];
      const filtered = r.tables.filter((t) =>
        allowed.includes(t.toLowerCase())
      );

      setTables(filtered);
      setSelectedTable(null);
      setTableInfo(null);
    }
  } catch (err) {
    console.error("Table load error:", err);
  }
}


  // LOAD SCHEMA + SAMPLE ROWS
  async function loadTableInfo(name) {
    try {
      const info = await apiFetchTableInfo(name);
      if (!info.error) setTableInfo(info);
    } catch {}
  }

  // RUN QUERY — NOW CHECKS FOR ";" AT END
  async function onRun() {
    setLoading(true);
    setError(null);
    setResult(null);

    // 🔴 DO NOT EXECUTE IF QUERY DOES NOT END WITH ";"
    if (!query.trim().endsWith(";")) {
      setError("✖ Add ';' at the end of your SQL query.");
      setLoading(false);
      return;
    }

    try {
      const r = await apiRunQuery(query);
      if (r.error) setError(r.error);
      else {
        setResult(r);
        if (!history.includes(query)) setHistory([query, ...history].slice(0, 30));
      }
    } catch (err) {
      setError(String(err));
    }

    setLoading(false);
  }

  // SELECT TABLE
  async function onSelectTable(name) {
    setSelectedTable(name);
    await loadTableInfo(name);
    setQuery();
  }

  // PANEL DRAGGING
  const startLeftDrag = () => setDraggingLeft(true);
  const startRightDrag = () => setDraggingRight(true);

  const stopDrag = useCallback(() => {
    setDraggingLeft(false);
    setDraggingRight(false);
  }, []);

  const handleMove = useCallback(
    (e) => {
      if (draggingLeft) setLeftWidth(Math.max(180, e.clientX));
      if (draggingRight) {
        const total = window.innerWidth;
        setRightWidth(Math.max(200, total - e.clientX));
      }
    },
    [draggingLeft, draggingRight]
  );

  useEffect(() => {
    window.addEventListener("mousemove", handleMove);
    window.addEventListener("mouseup", stopDrag);
    return () => {
      window.removeEventListener("mousemove", handleMove);
      window.removeEventListener("mouseup", stopDrag);
    };
  }, [handleMove, stopDrag]);

  if (!token || token === "null" || token === "undefined") {
  return <AuthPage onLogin={handleLogin} />;
}


  return (
    <div className="layout">
      {/* LEFT SIDEBAR */}
      <div className="sidebar" style={{ width: leftWidth }}>
        <h1 className="main-title">SQL Runner</h1>
        <div className="sub-title">Run SQL — Django + React</div>

        <TableList tables={tables} selected={selectedTable} onSelect={onSelectTable} />

        <h2 className="side-heading">Recent Queries</h2>
        <ul className="recent-list">
          {history.map((q, i) => (
            <li key={i} onClick={() => setQuery(q)}>
              {q}
            </li>
          ))}
        </ul>

        <div className="sidebar-bottom">
          {profile && <div className="user-info"><span className="email">{profile.username}</span></div>}
          <button className="logout-btn" onClick={logout}>Logout</button>
        </div>
      </div>

      <div className="drag-divider" onMouseDown={startLeftDrag}></div>

      {/* CENTER */}
      <div className="center">
        <div className="editor-card">
          <div className="card-title">SQL Editor</div>
          <QueryEditor query={query} setQuery={setQuery} onRun={onRun} />
        </div>

        <div className="output-card">
          <div className="card-title">Output</div>
          {loading && <div className="loading">Running query...</div>}
          {error && <div className="error-box">{error}</div>}
          <ResultsTable result={result} />
        </div>
      </div>

      <div className="drag-divider" onMouseDown={startRightDrag}></div>

      {/* SCHEMA PANEL */}
      <div className="schema-panel" style={{ width: rightWidth }}>
        <div className="schema-title">{selectedTable || "No table selected"}</div>
        <div className="schema-sub">Schema</div>

        <div className="schema-box">
          {tableInfo ? (
            <SchemaTable
              columns={tableInfo.columns}
              sampleRows={tableInfo.sample_rows}
            />
          ) : (
            "Select a table to view schema"
          )}
        </div>
      </div>
    </div>
  );
}
