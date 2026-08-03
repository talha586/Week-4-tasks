import unittest
from unittest.mock import patch

from Skill import web_search


class ToolLoggingTests(unittest.TestCase):
    def test_prehook_logs_tool_call_before_execution(self) -> None:
        calls = []

        def fake_tool(query: str, serp_key: str | None = None) -> dict:
            calls.append((query, serp_key))
            return {"ok": True}

        wrapped_tool = web_search.with_prehook("fake_tool", fake_tool)

        with patch("builtins.print") as mock_print:
            result = wrapped_tool("weather", serp_key="abc123")

        self.assertEqual(result, {"ok": True})
        self.assertEqual(calls, [("weather", "abc123")])
        mock_print.assert_called_once()
        self.assertIn("Prehook: calling tool 'fake_tool'", mock_print.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
