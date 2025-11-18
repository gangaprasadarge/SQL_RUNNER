import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders SQL Runner title", () => {
  render(<App />);
  const title = screen.getAllByText(/SQL Runner/i)[0];
  expect(title).toBeInTheDocument();
});
