from __future__ import annotations

from copilot import CopilotClient
from copilot.session import PermissionHandler

from markdown_formatting.clean_copilot_response import clean_copilot_response


# 整形指示とMarkdown本文を区切り、Copilotへ送るリクエストを組み立てる。
def build_format_request(format_instructions: str, markdown_text: str) -> str:
    return (
        f"{format_instructions.strip()}\n\n"
        "以下の <markdown_document> 内が今回の整形対象です。"
        "説明やコードフェンスを付けず、整形後のMarkdown全文だけを返してください。\n\n"
        "<markdown_document>\n"
        f"{markdown_text}\n"
        "</markdown_document>"
    )


# Copilotセッションを作成し、1件のMarkdownを指示に従って整形する。
async def format_with_copilot(
    client: CopilotClient,
    format_instructions: str,
    markdown_text: str,
    model: str,
) -> str:
    # ファイル操作などのツールを持たない、Markdown整形専用セッションを作る。
    session = await client.create_session(
        on_permission_request=PermissionHandler.approve_all,
        model=model,
        available_tools=[],
    )
    try:
        # 整形指示と本文をまとめて送り、応答が完了するまで待機する。
        response = await session.send_and_wait(
            build_format_request(format_instructions, markdown_text)
        )

        if response is None or not hasattr(response.data, "content"):
            raise RuntimeError("Copilot did not return a Markdown response.")

        # 応答に付加されることがあるコードフェンスを取り除いて返す。
        return clean_copilot_response(response.data.content)
    finally:
        # 成否にかかわらず、ファイルごとのセッションを確実に切断する。
        await session.disconnect()
