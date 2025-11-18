import React from "react";
import { FiDatabase } from "react-icons/fi";

export default function TableList({ tables, onSelect, selected }) {
  return (
    <div className="table-list">
      <ul>
        {tables.map((t) => (
          <li
            key={t}
            className={t === selected ? "active" : ""}
            onClick={() => onSelect(t)}
          >
            <FiDatabase size={16} style={{ marginRight: 8 }} />
            {t}
          </li>
        ))}
      </ul>
    </div>
  );
}
