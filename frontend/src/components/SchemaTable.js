import React from "react";

export default function SchemaTable({ columns }) {
  if (!columns || columns.length === 0) return "No schema";

  return (
    <table className="schema-table">
      <thead>
        <tr>
          <th>Column</th>
          <th>Type</th>
          <th>PK</th>
          <th>Not Null</th>
          <th>Default</th>
        </tr>
      </thead>

      <tbody>
        {columns.map((col, i) => (
          <tr key={i}>
            <td>{col.name}</td>
            <td>{col.type}</td>
            <td>{col.pk}</td>
            <td>{col.notnull}</td>
            <td>{col.dflt_value ?? "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
