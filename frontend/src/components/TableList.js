import React, { useEffect, useState } from "react";
import { getTables, getTableInfo } from "../api";

export default function TableList({ onSelectTable }) {
  const [tables, setTables] = useState([]);

  async function loadTables() {
    const res = await getTables();
    if (res.status === 200 && res.data && res.data.tables) {
      setTables(res.data.tables);
    } else {
      setTables([]);
      console.error("Failed to load tables", res);
    }
  }

  useEffect(() => {
    loadTables();
  }, []);

  return (
    <div className="table-list">
      {tables.map((t) => (
        <button key={t} className="table-btn" onClick={() => onSelectTable(t)}>
          {t}
        </button>
      ))}
    </div>
  );
}
