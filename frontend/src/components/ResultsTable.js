import React from "react";

export default function ResultsTable({ result }) {
  if (!result) return null;
  if (result.error) return <div className="error">{result.error}</div>;
  if (result.message)
    return <div className="message">{result.message} Rows affected: {result.rows_affected}</div>;

  if (!result.columns || result.columns.length === 0) return null;

  return (
    <div className="results">
      <table>
        <thead>
          <tr>
            {result.columns.map((c) => (
              <th key={c}>{c}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {result.rows.map((r, i) => (
            <tr key={i}>
              {result.columns.map((c) => (
                <td key={c}>{r[c] === null ? "" : String(r[c])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
