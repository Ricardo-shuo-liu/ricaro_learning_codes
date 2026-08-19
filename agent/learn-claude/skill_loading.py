import os
import subprocess
from pathlib import Path
import yaml
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
SKILLS_DIR = WORKDIR / "skills"

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)
MODEL = os.environ["LLM_MODEL_ID"]

# -- Skill catalog --
class SkillLoader:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.skills: dict[str, dict[str, str]] = {}
        self.scan()
    @staticmethod
    def parse_frontmatter(text: str) -> tuple[dict, str]:
        lines = text.splitlines(keepends=True)
        if not lines or lines[0].rstrip("\r\n") != "---":
            return {}, text
        closing_index = next(
            (index for index, line in enumerate(lines[1:], start=1)
             if line.rstrip("\r\n") == "---"),
            None,
        )
        if closing_index is None:
            return {}, text
        frontmatter = "".join(lines[1:closing_index])
        body = "".join(lines[closing_index + 1:]).strip()
        try:
            metadata = yaml.safe_load(frontmatter) or {}
        except yaml.YAMLError:
            metadata = {}
        if not isinstance(metadata, dict):
            metadata = {}
        return metadata, body
    def scan(self):
        self.skills.clear()
        if not self.skills_dir.exists():
            return
        skills_root = self.skills_dir.resolve()
        for manifest in sorted(self.skills_dir.glob("*/SKILL.md")):
            if (not manifest.is_file()
                    or not manifest.resolve().is_relative_to(skills_root)):
                continue
            content = manifest.read_text()
            metadata, body = self.parse_frontmatter(content)
            raw_name = metadata.get("name")
            name = raw_name.strip() if isinstance(raw_name, str) else ""
            name = name or manifest.parent.name
            raw_description = metadata.get("description")
            description = (raw_description.strip()
                           if isinstance(raw_description, str) else "")
            description = description or body.split("\n", 1)[0]
            description = " ".join(str(description).lstrip("# ").split())
            self.skills[name] = {
                "name": name,
                "description": description,
                "content": content,
            }
    def catalog(self) -> str:
        if not self.skills:
            return "(no skills found)"
        return "\n".join(
            f"- {skill['name']}: {skill['description']}"
            for skill in self.skills.values()
        )
    def load(self, name: str) -> str:
        skill = self.skills.get(name)
        if skill:
            return skill["content"]
        available = ", ".join(self.skills) or "none"
        return f"Error: Unknown skill '{name}'. Available: {available}"

SKILL_LOADER = SkillLoader(SKILLS_DIR)

def build_system_prompt() -> str:
    return (
        f"You are a coding agent at {WORKDIR}. Use tools to solve tasks. "
        "Act, don't explain.\n\n"
        f"Skills available:\n{SKILL_LOADER.catalog()}\n\n"
        "Use load_skill to read the full instructions when a skill applies."
    )
SYSTEM = build_system_prompt()

# -- Tools --
def run_bash(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, cwd=WORKDIR,
            capture_output=True, text=True, timeout=120,
        )
        output = (result.stdout + result.stderr).strip()
        return output[:50000] if output else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"

def run_read(path: str, limit: int | None = None) -> str:
    try:
        lines = (WORKDIR / path).resolve().read_text().splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more lines)"]
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

def run_write(path: str, content: str) -> str:
    try:
        file_path = (WORKDIR / path).resolve()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"

def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = (WORKDIR / path).resolve()
        text = file_path.read_text()
        if old_text not in text:
            return f"Error: text not found in {path}"
        file_path.write_text(text.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"

def run_glob(pattern: str) -> str:
    import glob
    try:
        matches = []
        for match in glob.glob(pattern, root_dir=WORKDIR):
            if (WORKDIR / match).resolve().is_relative_to(WORKDIR):
                matches.append(match)
        return "\n".join(matches) if matches else "(no matches)"
    except Exception as e:
        return f"Error: {e}"

TOOLS = [
    {"type": "function", "function": {
        "name": "bash",
        "description": "Run a shell command.",
        "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}
    }},
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read file contents.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["path"]}
    }},
    {"type": "function", "function": {
        "name": "write_file",
        "description": "Write content to a file.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}
    }},
    {"type": "function", "function": {
        "name": "edit_file",
        "description": "Replace exact text in a file once.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "old_text": {"type": "string"}, "new_text": {"type": "string"}}, "required": ["path", "old_text", "new_text"]}
    }},
    {"type": "function", "function": {
        "name": "glob",
        "description": "Find files matching a glob pattern.",
        "parameters": {"type": "object", "properties": {"pattern": {"type": "string"}}, "required": ["pattern"]}
    }},
    {"type": "function", "function": {
        "name": "load_skill",
        "description": "Load the full SKILL.md content by skill name.",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
    }},
]

TOOL_HANDLERS = {
    "bash": run_bash,
    "read_file": run_read,
    "write_file": run_write,
    "edit_file": run_edit,
    "glob": run_glob,
    "load_skill": SKILL_LOADER.load,
}

# -- Hooks --
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

class FakeToolBlock:
    """适配hook，模拟Claude tool_use block对象接口，原有hook完全不用改"""
    def __init__(self, name: str, tool_input: dict, tool_id: str):
        self.name = name
        self.input = tool_input
        self.id = tool_id

def permission_hook(block):
    """PreToolUse: block denied operations and ask about risky ones."""
    if block.name == "bash":
        command = block.input.get("command", "")
        for pattern in DENY_LIST:
            if pattern in command:
                print(f"\n\033[31m[blocked] '{pattern}'\033[0m")
                return "Permission denied by deny list"
        for keyword in DESTRUCTIVE:
            if keyword in command:
                print("\n\033[33m[permission] Potentially destructive command\033[0m")
                print(f"   Tool: {block.name}({block.input})")
                choice = input("   Allow? [y/N] ").strip().lower()
                if choice not in ("y", "yes"):
                    return "Permission denied by user"
    if block.name in ("read_file", "write_file", "edit_file"):
        path = block.input.get("path", "")
        if not (WORKDIR / path).resolve().is_relative_to(WORKDIR):
            print("\n\033[33m[permission] Access outside workspace\033[0m")
            print(f"   Tool: {block.name}({block.input})")
            choice = input("   Allow? [y/N] ").strip().lower()
            if choice not in ("y", "yes"):
                return "Permission denied by user"
    return None

def log_hook(block):
    """PreToolUse: log every tool call."""
    args_preview = str(list(block.input.values())[:2])[:60]
    print(f"\033[90m[HOOK] {block.name}({args_preview})\033[0m")
    return None

def large_output_hook(block, output):
    """PostToolUse: warn on large output."""
    if len(str(output)) > 100000:
        print(f"\033[33m[HOOK] Large output from {block.name}: {len(str(output))} chars\033[0m")
    return None

def context_inject_hook(query: str):
    """UserPromptSubmit: log the working directory."""
    print(f"\033[90m[HOOK] UserPromptSubmit: working in {WORKDIR}\033[0m")
    return None

def summary_hook(messages: list):
    """Stop: print the number of tool results in this message list."""
    tool_count = 0
    for msg in messages:
        if msg.get("role") == "tool":
            tool_count +=1
    print(f"\033[90m[HOOK] Stop: session used {tool_count} tool calls\033[0m")
    return None

register_hook("UserPromptSubmit", context_inject_hook)
register_hook("PreToolUse", permission_hook)
register_hook("PreToolUse", log_hook)
register_hook("PostToolUse", large_output_hook)
register_hook("Stop", summary_hook)

def execute_tool(fake_block) -> str:
    blocked = trigger_hooks("PreToolUse", fake_block)
    if blocked:
        return str(blocked)
    handler = TOOL_HANDLERS.get(fake_block.name)
    try:
        output = handler(**fake_block.input) if handler else f"Unknown: {fake_block.name}"
    except Exception as e:
        output = f"Error: {e}"
    trigger_hooks("PostToolUse", fake_block, output)
    return str(output)

def agent_loop(messages: list):
    while True:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"system","content":SYSTEM}] + messages,
            tools=TOOLS,
            max_tokens=8000,
        )
        choice = resp.choices[0]
        assistant_msg = choice.message
        # 追加assistant消息到history
        messages.append(assistant_msg.model_dump(exclude_none=True))

        tool_calls = assistant_msg.tool_calls
        if not tool_calls:
            force = trigger_hooks("Stop", messages)
            if force:
                messages.append({"role":"user","content":force})
                continue
            return

        for tc in tool_calls:
            # OpenAI tool_call 转成原来hook需要的block对象
            func_name = tc.function.name
            func_args = json.loads(tc.function.arguments)
            fake_block = FakeToolBlock(name=func_name, tool_input=func_args, tool_id=tc.id)
            tool_out = execute_tool(fake_block)
            # OpenAI标准tool消息追加
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": tool_out
            })

if __name__ == "__main__":
    print("s07: Skill Loading - catalog first, full content on demand")
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
        # 打印最后一条assistant文本
        last_assistant = history[-1]
        if last_assistant.get("role") == "assistant" and last_assistant.get("content"):
            print(last_assistant["content"])
        print()
