def parse_last_line_as_int(llm_output: str, default: int = -1) -> int:
    """Safely parses the last line of LLM output as an integer."""
    try:
        last_line = llm_output.strip().split('\n')[-1]
        return int(last_line)
    except (ValueError, IndexError):
        return default 