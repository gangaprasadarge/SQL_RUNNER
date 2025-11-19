import React, { useEffect, useState } from "react";
import { fetchTables } from "../api";

export default function TableList({ onSelect, selected }) {
  const [tables, setTables] = useState([]);

  async function loadTables() {
    const res = await fetchTables();

    if (res && res.tables) {
      const allowed = ["customers", "orders", "shippings"];
      const filtered = res.tables.filter(t =>
        allowed.includes(t.toLowerCase())
      );
      setTables(filtered);
    } else {
      setTables([]);
    }
  }

  useEffect(() => {
    loadTables();
  }, []);

  return (
    <div className="table-list">
      {tables.map((t) => (
        <button
  key={t}
  className={`table-btn ${selected === t ? "active-table" : ""}`}
  onClick={() => onSelectTable(t)}
>
  {t}
</button>

      ))}
    </div>
  );
}
