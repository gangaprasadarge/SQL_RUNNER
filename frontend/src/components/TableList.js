import React, { useEffect, useState } from "react";
import { fetchTables } from "../api";

export default function TableList({ onSelect }) {
  const [tables, setTables] = useState([]);

  async function loadTables() {
    try {
      const res = await fetchTables();

      if (res && res.tables) {
        const allowed = ["customers", "orders", "shippings"];
        const filtered = res.tables.filter((t) =>
          allowed.includes(t.toLowerCase())
        );
        setTables(filtered);
      } else {
        setTables([]);
      }
    } catch (err) {
      console.error("Error loading tables", err);
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
          className="table-btn"
          onClick={() => onSelect(t)}   {/* FIXED HERE */}
        >
          {t}
        </button>
      ))}
    </div>
  );
}
