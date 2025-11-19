import React, { useEffect, useState } from "react";
import { fetchTables } from "../api";

export default function TableList({ onSelectTable }) {
  const [tables, setTables] = useState([]);

  async function loadTables() {
    const res = await fetchTables();

    if (res && res.tables) {
      // show only these tables
      const allowedTables = ["customers", "orders", "shippings"];

      const filtered = res.tables.filter((t) =>
        allowedTables.includes(t.toLowerCase())
      );

      setTables(filtered);
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
