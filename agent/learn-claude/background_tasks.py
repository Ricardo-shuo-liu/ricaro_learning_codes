import atexit
import glob
import os
import signal
import subprocess
import threading
import time
from pathlib import Path

try:
    import readline
    readline.parse_and_bind("set bind‑tty‑special‑chars off")
    readline.parse_and_bind("set input‑meta on")
    readline.parse_and_bind("set output‑meta on")
    readline.parse_and_bind("set convert‑meta off")
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
MODEL = os.environ["LLM_MODEL_ID"]

SYSTEM = (
    f"You are a coding agent at {WORKDIR}. Use tools to solve tasks. "
    "Set run_in_background to true only for independent Bash commands."
)

# -- From s04: tool implementations --
_shell_processes: set[subprocess.Popen] = set()
_shell_process_lock = threading.RLock()


def _stop_process_group(process: subprocess.Popen):
    """Stop processes that remain in the command's original process group."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except (ProcessLookupError, OSError):
            return
        time.sleep(0.05)


def _stop_all_shell_processes():
    with _shell_process_lock:
        processes = list(_shell_processes)
        for process in processes:
            _stop_process_group(process)


def _handle_termination_signal(signum, _frame):
    _stop_all_shell_processes()
    raise SystemExit(128 + signum)


atexit.register(_stop_all_shell_processes)
signal.signal(signal.SIGTERM, _handle_termination_signal)


def _run_bash_process(command: str) -> tuple[str, int | None]:
    process = None
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=WORKDIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        with _shell_process_lock:
            _shell_processes.add(process)
        stdout, stderr = process.communicate(timeout=120)
        output = (stdout + stderr).strip()
        return (output[:50000] if output else "(no output)"), process.returncode
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)", None
    except OSError as error:
        return f"Error: {type(error).__name__}: {error}", None
    finally:
        if process is not None:
            _stop_process_group(process)
            try:
                process.wait(timeout=0.2)
            except subprocess.TimeoutExpired:
                pass
        with _shell_process_lock:
            if process is not None:
                _shell_processes.discard(process)


def _format_bash_result(output: str, exit_code: int | None) -> str:
    if exit_code in (0, None):
        return output
    return f"Error: command exited with status {exit_code}\n{output}"


def run_bash(command: str, run_in_background: bool = False) -> str:
    return _format_bash_result(*_run_bash_process(command))


def run_read(path: str, limit: int | None = None) -> str:
    try:
        file_path = (WORKDIR / path).resolve()
        lines = file_path.read_text(encoding="utf-8").splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more lines)"]
        return "\n".join(lines)
    except Exception as error:
        return f"Error: {error}"


def run_write(path: str, content: str) -> str:
    try:
        file_path = (WORKDIR / path).resolve()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as error:
        return f"Error: {error}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = (WORKDIR / path).resolve()
        text = file_path.read_text(encoding="utf-8")
        if old_text not in text:
            return f"Error: text not found in {path}"
        file_path.write_text(text.replace(old_text, new_text, 1), encoding="utf-8")
        return f"Edited {path}"
    except Exception as error:
        return f"Error: {error}"


def run_glob(pattern: str) -> str:
    try:
        matches = sorted({
            match
            for match in glob.glob(pattern, root_dir=WORKDIR, recursive=True)
            if (WORKDIR / match).resolve().is_relative_to(WORKDIR)
        })
        shown = matches[:200]
        if len(matches) > 200:
            shown.append("... (more matches omitted; narrow the pattern)")
        return "\n".join(shown) if shown else "(no matches)"
    except Exception as error:
        return f"Error: {error}"


# OpenAI function calling tools schema
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "run_in_background": {"type": "boolean"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "limit": {"type": "integer"}
                },
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
            "description": "Find files matching a glob pattern; ** matches recursively.",
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

# -- hooks and permission checks --
HOOKS = {"UserPromptSubmit": [], "PreToolUse": [], "PostToolUse": [], "Stop": []}


def register_hook(event: str, callback):
    HOOKS[event].append(callback)


def trigger_hooks(event: str, *args):
    for callback in HOOKS[event]:
        result = callback(*args)
        if result is not None:
            return result
    return None


DENY_LIST = ["rm -rf /", "sudo", "shutdown", "reboot", "mkfs", "dd if="]
DESTRUCTIVE = ["rm ", "> /etc/", "chmod 777"]


# 适配OpenAI：block 改为简单dict，name/input
def permission_hook(block: dict):
    if block["name"] == "bash":
        command = block["input"].get("command", "")
        for pattern in DENY_LIST:
            if pattern in command:
                print(f"\n\033[31m[blocked] '{pattern}'\033[0m")
                return "Permission denied by deny list"
        if any(keyword in command for keyword in DESTRUCTIVE):
            print("\n\033[33m[permission] Potentially destructive command\033[0m")
            print(f"   Tool: {block['name']}({block['input']})")
            choice = input("   Allow? [y/N] ").strip().lower()
            if choice not in ("y", "yes"):
                return "Permission denied by user"

    if block["name"] in ("read_file", "write_file", "edit_file"):
        path = block["input"].get("path", "")
        if not (WORKDIR / path).resolve().is_relative_to(WORKDIR):
            print("\n\033[33m[permission] Access outside workspace\033[0m")
            print(f"   Tool: {block['name']}({block['input']})")
            choice = input("   Allow? [y/N] ").strip().lower()
            if choice not in ("y", "yes"):
                return "Permission denied by user"
    return None


def log_hook(block: dict):
    preview = str(list(block["input"].values())[:2])[:60]
    print(f"\033[90m[HOOK] {block['name']}({preview})\033[0m")
    return None


def large_output_hook(block: dict, output):
    if len(str(output)) > 100000:
        print(
            f"\033[33m[HOOK] Large output from {block['name']}: "
            f"{len(str(output))} chars\033[0m"
        )
    return None


def context_inject_hook(query: str):
    print(f"\033[90m[HOOK] UserPromptSubmit: working in {WORKDIR}\033[0m")
    return None


def summary_hook(messages: list):
    tool_count = sum(1 for m in messages if m["role"] == "tool")
    print(f"\033[90m[HOOK] Stop: session used {tool_count} tool calls\033[0m")
    return None


register_hook("UserPromptSubmit", context_inject_hook)
register_hook("PreToolUse", permission_hook)
register_hook("PreToolUse", log_hook)
register_hook("PostToolUse", large_output_hook)
register_hook("Stop", summary_hook)


def call_tool(block: dict) -> str:
    handler = TOOL_HANDLERS.get(block["name"])
    try:
        output = handler(**block["input"]) if handler else f"Unknown: {block['name']}"
    except Exception as error:
        output = f"Error: {error}"
    return str(output)


# -- s11 BackgroundManager 完全复用逻辑，内部改为dict结构，不再用claude object block --
class BackgroundManager:
    def __init__(self):
        self.tasks: dict[str, dict] = {}
        self.results: dict[str, str] = {}
        self._ready: list[str] = []
        self._counter = 0
        self._lock = threading.Lock()

    def start(self, block: dict) -> str:
        """block: dict {"id":..., "name":"bash","input": {...}}"""
        if block["name"] != "bash":
            raise ValueError("Only Bash commands can run in the background")
        command = block["input"].get("command")
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Bash command cannot be empty")

        with self._lock:
            self._counter += 1
            task_id = f"bg_{self._counter:04d}"
            self.tasks[task_id] = {
                "tool_use_id": block["id"],
                "command": command,
                "status": "running",
            }

        thread = threading.Thread(
            target=self._run,
            args=(task_id, command),
            daemon=True,
        )
        try:
            thread.start()
        except Exception:
            with self._lock:
                self.tasks.pop(task_id, None)
            raise
        print(f"  [background] started {task_id}: {command[:60]}")
        return task_id

    def _run(self, task_id: str, command: str):
        try:
            output, exit_code = _run_bash_process(command)
            result = _format_bash_result(output, exit_code)
            status = "completed" if exit_code == 0 else "failed"
        except Exception as error:
            result = f"Error: {type(error).__name__}: {error}"
            status = "failed"

        with self._lock:
            task = self.tasks.get(task_id)
            if task is None:
                return
            task["status"] = status
            self.results[task_id] = result
            self._ready.append(task_id)

    def collect(self) -> list[str]:
        with self._lock:
            ready = []
            for task_id in self._ready:
                task = self.tasks.pop(task_id, None)
                result = self.results.pop(task_id, "")
                if task is not None:
                    ready.append((task_id, task, result))
            self._ready.clear()

        notifications = []
        for task_id, task, result in ready:
            notifications.append(
                f"<task_notification>\n"
                f"  <task_id>{task_id}</task_id>\n"
                f"  <status>{task['status']}</status>\n"
                f"  <command>{task['command']}</command>\n"
                f"  <summary>{result[:500]}</summary>\n"
                f"</task_notification>"
            )
            print(f"  [background] collected {task_id}: {task['status']}")
        return notifications


BACKGROUND = BackgroundManager()


def should_run_background(tool_name: str, tool_input: dict) -> bool:
    return (
        tool_name == "bash"
        and tool_input.get("run_in_background") is True
    )


def start_background_task(block: dict) -> str:
    return BACKGROUND.start(block)


def collect_background_results() -> list[str]:
    return BACKGROUND.collect()


def inject_background_results(messages: list) -> int:
    """OpenAI消息注入：后台通知作为普通user文本"""
    notifications = collect_background_results()
    if not notifications:
        return 0
    text = "\n".join(notifications)
    if messages and messages[-1]["role"] == "user":
        old = messages[-1]["content"] or ""
        messages[-1]["content"] = f"{old}\n{text}"
    else:
        messages.append({"role": "user", "content": text})
    return len(notifications)


def execute_tool(block: dict) -> str:
    """block dict: id,name,input"""
    blocked = trigger_hooks("PreToolUse", block)
    if blocked is not None:
        return str(blocked)

    if should_run_background(block["name"], block["input"]):
        try:
            task_id = start_background_task(block)
            output = (
                f"[Background task {task_id} started] "
                "The result will be collected on a later turn."
            )
        except Exception as error:
            output = f"Error: {error}"
    else:
        output = call_tool(block)

    trigger_hooks("PostToolUse", block, output)
    return output


# OpenAI agent_loop
def agent_loop(messages: list):
    while True:
        inject_background_results(messages)
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            max_tokens=8000,
        )
        choice = resp.choices[0]
        msg = choice.message
        messages.append(msg.model_dump(exclude_none=True))

        tool_calls = msg.tool_calls
        if not tool_calls:
            force = trigger_hooks("Stop", messages)
            if force:
                messages.append({"role": "user", "content": force})
                continue
            return

        # OpenAI tool_calls -> 内部block字典
        for tc in tool_calls:
            import json
            fn = tc.function
            try:
                input_args = json.loads(fn.arguments)
            except json.JSONDecodeError:
                input_args = {}
            block = {
                "id": tc.id,
                "name": fn.name,
                "input": input_args
            }
            tool_output = execute_tool(block)
            # OpenAI 独立role=tool消息
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": tool_output
            })


if __name__ == "__main__":
    print("s11-openai: Background Tasks - explicit background Bash execution")
    print("Enter a question, press Enter to send. Type q to quit.\n")
    history = []
    while True:
        try:
            query = input("\033[36m>> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        trigger_hooks("UserPromptSubmit", query)
        history.append({"role": "user", "content": query})
        agent_loop(history)
        # print latest assistant text
        last = history[-1]
        if last["role"] == "assistant" and last.get("content"):
            print(last["content"])
        print()
