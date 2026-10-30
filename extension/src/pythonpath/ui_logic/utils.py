import os
import sys
import re

def is_older(v1: str, v2: str) -> bool:
    """Compares two version strings (e.g., '1.2.3' and '1.3.0'). Returns True if v1 is older than v2."""
    v1_parts = [int(p) for p in v1.split(".")]
    v2_parts = [int(p) for p in v2.split(".")]

    return v1_parts < v2_parts


# sh/ollama/ is deprecated in favour of sh/, but still accepted.
# Longest first so sh/ollama/ is stripped before the generic sh/ prefix.
SELF_HOSTED_PREFIXES = ("sh/ollama/", "sh/")


def is_self_hosted(model: str, model_url: str = "") -> bool:
    """Returns True if the model should be routed directly to the self-hosted / custom endpoint.
    This is triggered if model starts with 'sh/' or if a custom Model URL is provided.
    """
    if model.startswith("sh/"):
        return True
    if model_url and model_url.strip():
        return True
    return False


def self_hosted_model(model: str) -> str:
    for prefix in SELF_HOSTED_PREFIXES:
        if model.startswith(prefix):
            return model[len(prefix) :]
    return model


def get_env_variable(var_name: str) -> str:
    """Retrieves an environment variable from os.environ, falling back to the Windows Registry on Windows."""
    if not var_name:
        return ""

    val = os.environ.get(var_name)
    if val:
        return val.strip()

    if sys.platform == "win32":
        try:
            import winreg

            for hive, subkey in [
                (winreg.HKEY_CURRENT_USER, r"Environment"),
                (
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                ),
            ]:
                try:
                    with winreg.OpenKey(hive, subkey) as k:
                        reg_val, _ = winreg.QueryValueEx(k, var_name)
                        if reg_val:
                            return str(reg_val).strip()
                except (FileNotFoundError, OSError):
                    continue
        except Exception:
            pass

    return ""


def resolve_api_key(api_key: str, model_url: str = "") -> str:
    """Resolves the API key string:
    - If user entered an environment variable name (e.g. 'OPENROUTER_API_KEY', '$VAR', '%VAR%'), resolves it.
    - If empty and model_url is an OpenRouter endpoint, tries to load OPENROUTER_API_KEY.
    - Otherwise returns the string as-is.
    """
    key = (api_key or "").strip()

    # Syntax like $OPENROUTER_API_KEY
    if key.startswith("$") and len(key) > 1:
        resolved = get_env_variable(key[1:])
        if resolved:
            return resolved

    # Syntax like %OPENROUTER_API_KEY%
    if key.startswith("%") and key.endswith("%") and len(key) > 2:
        resolved = get_env_variable(key[1:-1])
        if resolved:
            return resolved

    # Direct variable name e.g. OPENROUTER_API_KEY
    if key and (key.isupper() or "_" in key) and " " not in key:
        resolved = get_env_variable(key)
        if resolved:
            return resolved

    # If empty, check for known endpoint keys
    if not key:
        url_lower = (model_url or "").lower()
        if "openrouter" in url_lower:
            resolved = get_env_variable("OPENROUTER_API_KEY")
            if resolved:
                return resolved

        # Generic fallbacks
        for fallback_name in ("OPENAI_API_KEY", "LLM_API_KEY"):
            resolved = get_env_variable(fallback_name)
            if resolved:
                return resolved

    return key


def clean_markdown_text(text: str) -> str:
    """Cleans raw markdown syntax from an LLM response so it reads as plain, unadorned text in LibreOffice Writer."""
    if not text:
        return ""

    text = text.strip()

    # 1. Strip enclosing code fences (e.g. ```markdown ... ``` or ``` ... ```)
    fence_match = re.match(r"^```[a-zA-Z0-9_-]*\r?\n([\s\S]*?)\r?\n```$", text)
    if fence_match:
        text = fence_match.group(1).strip()
    else:
        text = re.sub(r"^```[a-zA-Z0-9_-]*\r?\n", "", text)
        text = re.sub(r"\r?\n```$", "", text)

    # 2. Strip conversational preambles/postambles commonly output by LLMs
    text = re.sub(
        r"^(?:Here (?:is|are) (?:the |an? )?(?:revised|edited|improved|rewritten|requested)?\s*(?:text|version|document|paragraph|sentence|response)?:\s*)\r?\n+",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\r?\n+(?:I hope this helps!?|Let me know if you (?:need|would like) (?:any )?(?:further|additional|other) (?:changes|edits|help)\.?).*$",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # 3. Strip bold and italic markdown markers while preserving the content
    text = re.sub(r"\*\*\*(.*?)\*\*\*", r"\1", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*([^\*\n]+)\*", r"\1", text)
    text = re.sub(r"___(.*?)___", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"_([^_\n]+)_", r"\1", text)

    # 4. Strip markdown heading tags (e.g. '### Heading' -> 'Heading')
    text = re.sub(r"(?m)^#{1,6}\s+", "", text)

    # 5. Strip inline code backticks (`code` -> code)
    text = re.sub(r"`([^`\n]+)`", r"\1", text)

    # 6. Strip blockquote markers (> quote -> quote)
    text = re.sub(r"(?m)^>\s*", "", text)

    # 7. Strip markdown links [text](url) -> text (url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)

    return text.strip()
