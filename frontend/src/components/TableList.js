import React, { useEffect, useState } from "react";
import { fetchTables } from "../api";

export default function TableList({ tables, selected, onSelect }) {
  const [filteredTables, setFilteredTables] = useState([]);

  useEffect(() => {
    loadTables();
  }, []);

  async function loadTables() {
    try {
      const res = await fetchTables();

      if (res && res.tables) {
        const allowed = ["customers", "orders", "shippings"];

        const cleaned = res.tables.filter((t) =>
          allowed.includes(t.toLowerCase())
        );

        setFilteredTables(cleaned);
      }
    } catch (err) {
      console.error("Failed to load tables:", err);
    }
  }

  return (
    <div className="table-list">
      {filteredTables.map((t) => (
        <button
          key={t}
          className={`table-btn ${selected === t ? "active" : ""}`}
          onClick={() => onSelect(t)}
        >
          {t}
        </button>
      ))}
    </div>
  );
}
