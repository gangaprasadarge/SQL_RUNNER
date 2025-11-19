import "./App.css";
import React, { useEffect, useState, useCallback } from "react";
import QueryEditor from "./components/QueryEditor";
import TableList from "./components/TableList";
import ResultsTable from "./components/ResultsTable";
import { runQuery, fetchTables, fetchTableInfo, getProfile } from "./api";
import SchemaTable from "./components/SchemaTable";
import AuthPage from "./pages/AuthPage";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [query, setQuery] = useState("select * from Customers");
  const [result, setResult] = useState(null);
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState("Customers");
  const [tableInfo, setTableInfo] = useState(null);
  const [history, setHistory] = useState([]);
  const [profile, setProfile] = useState(null);

  const [leftWidth, setLeftWidth] = useState(260);
  const [rightWidth, setRightWidth] = useState(320);
  const [draggingLeft, setDraggingLeft] = useState(false);
  const [draggingRight, setDraggingRight] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
  }

  useEffect(() => {
    if (token) {
      loadTables();
      loadProfile();
    }
  }, [token]);

  async function loadProfile() {
    const p = await getProfile();
    setProfile(p);
  }

  async function loadTables() {
    const r = await fetchTables();
    if (r.tables) setTables(r.tables);
  }

  async function onRun() {
    setLoading(true);
    setError(null);
    const r = await runQuery(query);
    if (r.error) {
      setError(r.error);
    } else {
      setResult(r);
      if (!history.includes(query)) setHistory([query, ...history]);
    }
    setLoading(false);
  }

  async function onSelectTable(name) {
    setSelectedTable(name);
    const info = await fetchTableInfo(name);
    setTableInfo(info);
  }

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

  if (!token) return <AuthPage onLogin={handleLogin} />;

  return (
    <div className="layout">
      <div className="sidebar" style={{ width: leftWidth }}>
        <h1 className="main-title">SQL Runner</h1>
        <div className="sub-title">Run SQL on SQLite — Django + React</div>

        <TableList
          tables={tables}
          selected={selectedTable}
          onSelect={onSelectTable}
        />

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
              <span className="email">{profile.username}</span>
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
        <div className="schema-title">{selectedTable}</div>
        <div className="schema-sub">Schema</div>

        <div className="schema-box">
          {tableInfo ? (
            <SchemaTable columns={tableInfo.columns} />
          ) : (
            "Select a table to view schema"
          )}
        </div>
      </div>
    </div>
  );
}
