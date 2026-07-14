from __future__ import annotations

MARKDOWN_FENCES = {"```", "```md", "```markdown"}


# Copilotの応答から不要なコードフェンスを除き、Markdown本文を整える。
def clean_copilot_response(response_text: str) -> str:
    text = response_text.strip()
    lines = text.splitlines()

    if len(lines) >= 2 and lines[0].strip().lower() in MARKDOWN_FENCES:
        if lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1]).strip()

    if not text:
        raise ValueError("Copilot returned an empty Markdown document.")

    return f"{text}\n"
