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

  // called after successful login
  function handleLogin(access, refresh) {
    localStorage.setItem("token", access);
    localStorage.setItem("refresh", refresh);
    setQuery("");
    setHistory([]);
    setResult(null);
    setToken(access);
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
    setToken(null);
    setQuery("");
    setHistory([]);
    setResult(null);
    setProfile(null);
    setTables([]);
    setSelectedTable(null);
    setTableInfo(null);
  }

  // load tables + profile whenever token is available
  useEffect(() => {
    if (token) {
      loadProfile();
      loadTables();
    }
  }, [token]);

  // load profile (safe/robust)
  async function loadProfile() {
    try {
      const p = await apiGetProfile();
      // apiGetProfile should return an object like { username:..., email:..., id:... }
      if (p && !p.error) {
        setProfile(p);
      } else {
        // If token expired / unauthorized, force logout
        if (p && p.detail === "Authentication credentials were not provided.") {
          logout();
        }
      }
    } catch (err) {
      // don't crash app on profile load error
      console.error("loadProfile error:", err);
    }
  }

  // load tables and auto-select first table
  async function loadTables() {
    setError(null);
    try {
      const r = await apiFetchTables();
      if (r && r.tables) {
        setTables(r.tables);
        // if there's no selected table or selected not in list, pick first
        if (!selectedTable || !r.tables.includes(selectedTable)) {
          const first = r.tables.length ? r.tables[0] : null;
          setSelectedTable(first);
          if (first) {
            // fetch its info
            await loadTableInfo(first);
          } else {
            setTableInfo(null);
          }
        } else {
          // refresh info for existing selected table
          await loadTableInfo(selectedTable);
        }
      } else if (r && r.error) {
        setError(r.error);
      } else {
        setTables([]);
      }
    } catch (err) {
      console.error("loadTables error:", err);
      setError(String(err));
    }
  }

  // fetch schema + sample rows for a table
  async function loadTableInfo(name) {
    if (!name) return;
    setError(null);
    setTableInfo(null);
    try {
      const info = await apiFetchTableInfo(name);
      if (info && !info.error) {
        setTableInfo(info);
      } else if (info && info.error) {
        setError(info.error);
      } else {
        setTableInfo(null);
      }
    } catch (err) {
      console.error("loadTableInfo error:", err);
      setError(String(err));
    }
  }

  // triggered by user pressing Run
  async function onRun() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const r = await apiRunQuery(query);
      if (!r) {
        setError("No response from server");
      } else if (r.error) {
        setError(r.error);
      } else {
        // r may contain { columns, rows } or { message, rows_affected }
        setResult(r);
        if (query && !history.includes(query)) setHistory([query, ...history].slice(0, 30));
      }
    } catch (err) {
      console.error("onRun error:", err);
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  // user selects a table from the left list
  async function onSelectTable(name) {
    setSelectedTable(name);
    await loadTableInfo(name);
    // optionally set editor example query
    setQuery(`SELECT * FROM "${name}" LIMIT 100;`);
  }

  // drag handlers for resizing panels
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

  // if not logged in, show auth page
  if (!token) return <AuthPage onLogin={handleLogin} />;

  return (
    <div className="layout">
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
          {profile && (
            <div className="user-info">
              <span className="email">{profile.username || profile.email}</span>
            </div>
          )}
          <button className="logout-btn" onClick={logout}>
            Logout
          </button>
        </div>
      </div>

      <div className="drag-divider" onMouseDown={startLeftDrag}></div>

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

      <div className="schema-panel" style={{ width: rightWidth }}>
        <div className="schema-title">{selectedTable || "No table selected"}</div>
        <div className="schema-sub">Schema</div>

        <div className="schema-box">
          {tableInfo ? <SchemaTable columns={tableInfo.columns} sampleRows={tableInfo.sample_rows} /> : "Select a table to view schema"}
        </div>
      </div>
    </div>
  );
}
