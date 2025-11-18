import React from "react";
import CodeMirror from "@uiw/react-codemirror";
import { sql } from "@codemirror/lang-sql";
import { oneDark } from "@codemirror/theme-one-dark";

export default function QueryEditor({ query, setQuery, onRun, loading }) {
  return (
    <div className="query-editor">
      <CodeMirror
        value={query}
        height="180px"
        extensions={[sql()]}
        theme={oneDark}
        onChange={(value) => setQuery(value)}
      />

      <button className="run-btn" onClick={onRun}>
         ▶ Run Query
      </button>

    </div>
  );
}
