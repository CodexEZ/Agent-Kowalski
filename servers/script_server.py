from fastmcp import FastMCP, Client
import asyncio
import uvicorn
import os
import subprocess
import sys
from loguru import logger

# Configure loguru
logger.remove()  # remove default handler
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>"
)

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastMCP()

# Define a safe workspace directory
WORKSPACE = os.path.abspath("./workspace")
os.makedirs(WORKSPACE, exist_ok=True)


@app.tool(description="List all Python scripts in the workspace.")
async def list_scripts() -> dict:
    try:
        files = [f for f in os.listdir(WORKSPACE) if f.endswith(".py")]
        logger.info(f"Listed {len(files)} scripts: {files}")
        return {"scripts": files}
    except Exception as e:
        logger.error(f"Error listing scripts: {e}")
        return {"error": str(e)}


@app.tool(description="Write (create/overwrite) a Python script in the workspace.")
def write_script(filename: str, code: str) -> dict:
    try:
        if not filename.endswith(".py"):
            logger.warning(f"Invalid filename: {filename}")
            return {"error": "Filename must end with .py"}
        filepath = os.path.join(WORKSPACE, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        logger.success(f"Script {filename} written successfully.")
        return {"success": f"Script {filename} written successfully."}
    except Exception as e:
        logger.error(f"Error writing script {filename}: {e}")
        return {"error": str(e)}


@app.tool(description="Read the contents of a Python script.")
def read_script(filename: str) -> dict:
    try:
        filepath = os.path.join(WORKSPACE, filename)
        if not os.path.exists(filepath):
            logger.warning(f"Tried to read non-existent script: {filename}")
            return {"error": f"{filename} does not exist"}
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info(f"Read script {filename} ({len(content)} chars).")
        return {"filename": filename, "content": content}
    except Exception as e:
        logger.error(f"Error reading script {filename}: {e}")
        return {"error": str(e)}


@app.tool(description="Run a Python script from the workspace and return its stdout/stderr.")
def run_script(filename: str, timeout:int = 30) -> dict:
    logger.info(f"running script {filename} with time out {timeout}s")
    try:
        filepath = os.path.join(WORKSPACE, filename)
        if not os.path.exists(filepath):
            logger.warning(f"Tried to run non-existent script: {filename}")
            return {"error": f"{filename} does not exist"}

        logger.info(f"Running script: {filename}")
        result = subprocess.run(
            [sys.executable, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout # prevent runaway scripts
        )

        logger.info(f"Execution finished (exit_code={result.returncode}).")
        if result.stderr:
            logger.error(f"Stderr: {result.stderr.strip()}")

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        logger.error(f"Script {filename} timed out.")
        return {"error": "Script execution timed out"}
    except Exception as e:
        logger.error(f"Error running script {filename}: {e}")
        return {"error": str(e)}


# Optional: Prompt template for "coding agent" behavior
@app.prompt(
    description="Generate, save, and run Python scripts as needed.",
    name="python_coder"
)
def python_coder() -> str:
    return """
    Task: Write or modify Python scripts, then run them.

    Steps for the model:
    1. If user asks to create or update a script:
       - Use `write_script` with filename + code.
    2. If user wants to see script contents:
       - Use `read_script`.
    3. If user wants to execute:
       - Use `run_script`.
    4. If needed, list available scripts with `list_scripts`.

    Important:
    - Always work inside the ./workspace directory.
    - Return stdout + stderr when executing.
    """


# Testing client
test_server = Client(app)

async def run_tests():
    async with test_server:
        logger.info("🔍 Running MCP tool tests...")
        await test_server.ping()
        tools = await test_server.list_tools()
        logger.info(f"Discovered tools: {[t.name for t in tools]}")

        # Write a script
        code = 'print("Hello from inside MCP!")'
        res = await test_server.call_tool("write_script", {"filename": "hello.py", "code": code})
        logger.debug(res.content[0].text)

        # Run script
        res = await test_server.call_tool("run_script", {"filename": "hello.py"})
        logger.debug(res.content[0].text)

        # Read script
        res = await test_server.call_tool("read_script", {"filename": "hello.py"})
        logger.debug(res.content[0].text)

        # List scripts
        res = await test_server.call_tool("list_scripts", {})
        logger.debug(res.content[0].text)


if __name__ == "__main__":
    logger.info("Running test cases 🏃‍♂️....")
    asyncio.run(run_tests())
    app.run(transport="streamable-http", host="0.0.0.0", port=8002)
