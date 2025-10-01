AI Agent Project

This project is a simple file + Python execution agent. It can:

List files in a directory: Shows file size and whether it’s a directory.
Read file content: Reads up to MAX_CHARACTERS (default: 10,000). Cuts off with a notice if longer.
Write files safely: Makes directories if needed and writes text content.
Run Python scripts: Executes .py files in a controlled working directory with optional args.

Safety checks

Always keeps actions inside the permitted working_directory.
Returns error messages if trying to go outside, or if wrong file types are used.
Uses try/except everywhere to avoid crashing.

Usage

Get a Gemini API key from the official site:
👉 https://aistudio.google.com/app/apikey
Create a .env file in the root of the project with:
GEMINI_API_KEY=your_api_key_here


Run the agent in the terminal with uv:
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20"

That’s it — the agent will take your instruction, create or edit files, and run Python code when needed.
