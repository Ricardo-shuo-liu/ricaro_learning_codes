import os
import subprocess

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path="/home/ricaedo/ricaro_learning_codes/agent/.env",
            override=True)


try:
    import readline
    readline.parse_and_bind('set bind-tty-special-chars off')
    readline.parse_and_bind('set input-meta on')
    readline.parse_and_bind('set output-meta on')
    readline.parse_and_bind('set convert-meta off')
except ImportError:
    pass


client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

model = os.getenv("LLM_MODEL_ID")

SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."

TOOLS = [{
    "type": "function",
    "function": {
        "name": "bash",
        "description": "Run a shell command.",
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    }
}]


def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command,
                           shell=True,
                           cwd=os.getcwd(),
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"


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
            if msg.content:
                print(f"\n🤖 Agent: {msg.content}")
            return

        for tc in msg.tool_calls:
            func_name = tc.function.name
            import json
            args = json.loads(tc.function.arguments)

            if func_name == "bash":
                cmd = args["command"]
                print(f"\033[33m$ {cmd}\033[0m")
                output = run_bash(cmd)
                print(output[:200])

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": output
                })


if __name__ == "__main__":
    print("s01: Agent Loop (OpenAI compatible version)")
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
        print()