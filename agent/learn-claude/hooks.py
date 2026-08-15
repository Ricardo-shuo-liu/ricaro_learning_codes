import os
import subprocess
from pathlib import Path
import json
try:
    import readline
    readline.parse_and_bind('set bind-tty-special-chars off')
    readline.parse_and_bind('set input-meta on')
    readline.parse_and_bind('set output-meta on')
    readline.parse_and_bind('set convert-meta off')
except ImportError:
    pass

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


WORKDIR = Path.cwd()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

model = os.getenv("LLM_MODEL_ID")

SYSTEM = f"You are a coding agent at {WORKDIR}. Use tools to solve tasks. Act, don't explain."



def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=WORKDIR,
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"


def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path


def run_read(path: str, limit: int | None = None) -> str:
    try:
        lines = safe_path(path).read_text().splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more lines)"]
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def run_write(path: str, content: str) -> str:
    try:
        file_path = safe_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = safe_path(path)
        text = file_path.read_text()
        if old_text not in text:
            return f"Error: text not found in {path}"
        file_path.write_text(text.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"


def run_glob(pattern: str) -> str:
    import glob as g
    try:
        results = []
        for match in g.glob(pattern, root_dir=WORKDIR):
            if (WORKDIR / match).resolve().is_relative_to(WORKDIR):
                results.append(match)
        return "\n".join(results) if results else "(no matches)"
    except Exception as e:
        return f"Error: {e}"

TOOLS=[
    {
        "type":"function",
        "function":{
            "name":"bash",
            "description":"Run a shell command.",
            "parameters":{
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"read_file",
            "description":"Read file contents.",
            "parameters":{
                "type":"object",
                "properties": {"path": {"type": "string"}, "limit": {"type": "integer"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Replace exact text in a file once.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_text": {"type": "string"},
                    "new_text": {"type": "string"}
                },
                "required": ["path", "old_text", "new_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "glob",
            "description": "Find files matching a glob pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"}
                },
                "required": ["pattern"]
            }
        }
    }
]


TOOL_HANDLERS = {
    "bash": run_bash,
    "read_file": run_read,
    "write_file": run_write,
    "edit_file": run_edit,
    "glob": run_glob,
}


HOOKS = {"UserPromptSubmit": [], "PreToolUse": [], "PostToolUse": [], "Stop": []}

def register_hook(event: str, callback):
    HOOKS[event].append(callback)

def trigger_hooks(event: str, *args):
    for callback in HOOKS[event]:
        result = callback(*args)
        if result is not None:  # A hook result blocks this tool call.
            return result
    return None

DENY_LIST = ["rm -rf /", "sudo", "shutdown", "reboot", "mkfs", "dd if="]
DESTRUCTIVE = ["rm ", "> /etc/", "chmod 777"]

def permission_hook(tc):
    """PreToolUse: s03 check_permission() logic moved here."""
    args = json.loads(tc.function.arguments)
    if tc.function.name == "bash":
        for pattern in DENY_LIST:
            if pattern in args.get("command", ""):
                print(f"\n\033[31m[blocked] '{pattern}'\033[0m")
                return "Permission denied by deny list"
        for kw in DESTRUCTIVE:
            if kw in args.get("command", ""):
                print(f"\n\033[33m[permission] Potentially destructive command\033[0m")
                args_str = [f"{name}={value}" for name,value in args.items()]
                arg_text = ", ".join(args_str)
                print(f"   Tool: {tc.function.name}({arg_text})")
                choice = input("   Allow? [y/N] ").strip().lower()
                if choice not in ("y", "yes"):
                    return "Permission denied by user"
    if tc.function.name in ("read_file", "write_file", "edit_file"):
        path = args.get("path", "")
        if not (WORKDIR / path).resolve().is_relative_to(WORKDIR):
            print(f"\n\033[33m[permission] Access outside workspace\033[0m")
            args_str = [f"{name}={value}" for name,value in args.items()]
            arg_text = ", ".join(args_str)
            print(f"   Tool: {tc.function.name}({arg_text})")
            choice = input("   Allow? [y/N] ").strip().lower()
            if choice not in ("y", "yes"):
                return "Permission denied by user"
    return None

def log_hook(tc):
    """PreToolUse: log every tool call."""
    args = json.loads(tc.function.arguments)
    args_preview = str(list(args.values())[:2])[:60]
    print(f"\033[90m[HOOK] {tc.function.name}({args_preview})\033[0m")
    return None

def large_output_hook(tc,
                      output):
    """PostToolUse: warn on large output."""
    if len(str(output)) > 100000:
        print(f"\033[33m[HOOK] Large output from {tc.function.arguments}: {len(str(output))} chars\033[0m")
    return None

# UserPromptSubmit hook: log user input before it reaches the LLM
def context_inject_hook(query: str):
    print(f"\033[90m[HOOK] UserPromptSubmit: working in {WORKDIR}\033[0m")
    return None

# Stop hook: print summary when loop is about to exit
def summary_hook(messages: list):
    tool_count = 0
    for m in messages:
        if m["role"] =="tool":
            tool_count += 1
    print(f"\033[90m[HOOK] Stop: session used {tool_count} tool calls\033[0m")
    return None

register_hook("UserPromptSubmit", context_inject_hook)
register_hook("PreToolUse", permission_hook)
register_hook("PreToolUse", log_hook)
register_hook("PostToolUse", large_output_hook)
register_hook("Stop", summary_hook)


def agent_loop(messages: list):
    while True:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            max_tokens=8000,
        )
        choice = resp.choices[0]
        msg = choice.message

        messages.append(msg.model_dump())

        if choice.finish_reason != "tool_calls":
            force = trigger_hooks("Stop", messages)
            if force:
                messages.append({"role": "user", "content": force})
                continue
            return

        for tc in msg.tool_calls:
            blocked = trigger_hooks("PreToolUse", tc)

            if blocked:
                messages.append({"role": "tool",
                                 "tool_call_id": tc.id,
                                "content": str(blocked) })
                continue
            func_name = tc.function.name
            
            args = json.loads(tc.function.arguments)
            handler = TOOL_HANDLERS.get(func_name)
            out = handler(**args)
            trigger_hooks("PostToolUse", tc, out)

            messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": out
                })


if __name__ == "__main__":
    print("s04: Hooks - extension logic on hooks, loop stays clean")
    print("Enter a question, press Enter to send. Type q to quit.\n")

    history = [{"role": "system", "content": SYSTEM}]

    while True:
        try:
            query = input("\033[36m >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        q = query.strip().lower()
        if q in ("q", "exit", ""):
            break
        history.append({"role": "user", "content": query})
        agent_loop(history)
        last_msg = history[-1]
        content = last_msg.get("content")
        if content:
            print(f"\033[32mAgent:\033[0m {content}")
        print()