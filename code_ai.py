# code_ai.py
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST  = os.getenv("OLLAMA_HOST",  "http://10.22.39.192:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5vl:latest")

SUPPORTED_LANGUAGES = [
    "python", "javascript", "typescript", "sql",
    "bash", "java", "c", "cpp", "go", "rust",
    "html", "css", "yaml", "json"
]

FENCE = "```"   # backtick fence stored as variable — avoids f-string syntax errors


def call_llm(prompt: str, max_tokens: int = 2048) -> str:
    """Call Qwen on remote GPU."""
    resp = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model":   OLLAMA_MODEL,
            "prompt":  prompt,
            "stream":  False,
            "options": {"temperature": 0.1, "num_predict": max_tokens}
        },
        timeout=180
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


def extract_code_blocks(text: str) -> list:
    """Extract all code blocks from markdown response."""
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    blocks  = []
    for lang, code in matches:
        blocks.append({
            "language": lang.lower() if lang else "text",
            "code":     code.strip()
        })
    if not blocks and text.strip():
        blocks.append({"language": "text", "code": text.strip()})
    return blocks


# ── Mode 1: Generate code ─────────────────────────────────────────────────────

def generate_code(description: str, language: str = "python", context: str = "") -> dict:
    """Generate code from a plain English description."""
    context_section = f"\nCONTEXT / EXISTING CODE:\n{context}\n" if context else ""

    prompt = (
        f"You are an expert {language} programmer.\n"
        f"Write clean, well-commented, production-quality code based on the description below.\n\n"
        f"DESCRIPTION:\n{description}\n"
        f"{context_section}\n"
        f"REQUIREMENTS:\n"
        f"- Write in {language}\n"
        f"- Include docstrings and inline comments\n"
        f"- Handle edge cases and errors\n"
        f"- Include a usage example at the bottom as a comment\n"
        f"- Follow best practices for {language}\n\n"
        f"Provide ONLY the code in a markdown code block. No explanations before or after."
    )

    response = call_llm(prompt, max_tokens=2048)
    blocks   = extract_code_blocks(response)

    return {
        "response":     response,
        "code_blocks":  blocks,
        "primary_code": blocks[0]["code"] if blocks else response,
        "language":     language
    }


# ── Mode 2: Explain code ──────────────────────────────────────────────────────

def explain_code(code: str, detail_level: str = "standard") -> str:
    """Explain what code does in plain English."""
    detail_map = {
        "brief":    "Give a 3-4 sentence high-level summary only.",
        "standard": "Explain the overall purpose, then walk through each major section.",
        "detailed": "Explain every line or block, including why each decision was made."
    }
    detail_instruction = detail_map.get(detail_level, detail_map["standard"])

    prompt = (
        f"You are an expert code reviewer and teacher.\n"
        f"Explain the following code clearly to a developer.\n\n"
        f"{detail_instruction}\n\n"
        f"Include:\n"
        f"1. What this code does (purpose)\n"
        f"2. How it works (logic walkthrough)\n"
        f"3. Key design decisions or patterns used\n"
        f"4. Any potential issues or limitations\n\n"
        f"CODE:\n{FENCE}\n{code}\n{FENCE}\n\n"
        f"Explain in clear, plain English:"
    )

    return call_llm(prompt, max_tokens=1024)


# ── Mode 3: Find and fix bugs ─────────────────────────────────────────────────

def find_and_fix_bugs(code: str, error_message: str = "", language: str = "python") -> dict:
    """Find bugs and return fixed code."""
    error_section = f"\nERROR MESSAGE:\n{error_message}\n" if error_message else ""

    prompt = (
        f"You are an expert {language} debugger.\n"
        f"Analyse this code, find ALL bugs, and provide a fixed version.\n\n"
        f"CODE:\n{FENCE}{language}\n{code}\n{FENCE}\n"
        f"{error_section}\n"
        f"Provide your response in this exact format:\n\n"
        f"## BUGS FOUND\n"
        f"List each bug as:\n"
        f"- Bug N: [description of the bug and why it is wrong]\n\n"
        f"## FIXED CODE\n"
        f"{FENCE}{language}\n"
        f"[complete fixed code with # FIXED: comments marking each change]\n"
        f"{FENCE}\n\n"
        f"## EXPLANATION\n"
        f"Brief explanation of all changes made."
    )

    response = call_llm(prompt, max_tokens=2048)
    blocks   = extract_code_blocks(response)

    fixed_code = ""
    for block in blocks:
        if block["language"] in (language, "text") and len(block["code"]) > 10:
            fixed_code = block["code"]
            break

    return {
        "response":   response,
        "fixed_code": fixed_code,
        "has_fix":    bool(fixed_code)
    }


# ── Mode 4: Refactor code ─────────────────────────────────────────────────────

def refactor_code(code: str, language: str = "python", goals: list = None) -> dict:
    """Refactor code for better quality."""
    default_goals = [
        "improve readability",
        "better variable names",
        "extract repeated logic into functions",
        "add type hints (if Python)",
        "remove dead code",
        "follow language best practices"
    ]
    refactor_goals = goals or default_goals
    goals_text     = "\n".join(f"- {g}" for g in refactor_goals)

    prompt = (
        f"You are an expert {language} software engineer.\n"
        f"Refactor this code to be cleaner and more maintainable.\n"
        f"Do NOT change the behaviour - only improve the code quality.\n\n"
        f"REFACTORING GOALS:\n{goals_text}\n\n"
        f"ORIGINAL CODE:\n{FENCE}{language}\n{code}\n{FENCE}\n\n"
        f"Provide:\n\n"
        f"## REFACTORED CODE\n"
        f"{FENCE}{language}\n"
        f"[complete refactored code]\n"
        f"{FENCE}\n\n"
        f"## CHANGES MADE\n"
        f"List each improvement made as a bullet point."
    )

    response = call_llm(prompt, max_tokens=2048)
    blocks   = extract_code_blocks(response)

    refactored = ""
    for block in blocks:
        if block["language"] in (language, "text") and len(block["code"]) > 10:
            refactored = block["code"]
            break

    return {
        "response":        response,
        "refactored_code": refactored,
        "original_code":   code
    }


# ── Mode 5: Generate unit tests ───────────────────────────────────────────────

def generate_tests(code: str, language: str = "python", framework: str = "pytest") -> dict:
    """Generate unit tests for given code."""
    prompt = (
        f"You are an expert {language} test engineer.\n"
        f"Write comprehensive unit tests for the following code using {framework}.\n\n"
        f"CODE TO TEST:\n{FENCE}{language}\n{code}\n{FENCE}\n\n"
        f"Write tests covering:\n"
        f"1. Happy path - normal expected inputs\n"
        f"2. Edge cases - empty input, None, zero, empty list etc.\n"
        f"3. Error cases - invalid inputs, exceptions that should be raised\n"
        f"4. Boundary conditions - min/max values\n\n"
        f"{FENCE}{language}\n"
        f"[complete test file with all test cases]\n"
        f"{FENCE}\n\n"
        f"Make tests self-contained and runnable."
    )

    response = call_llm(prompt, max_tokens=2048)
    blocks   = extract_code_blocks(response)

    test_code = ""
    for block in blocks:
        if block["language"] in (language, "text") and len(block["code"]) > 10:
            test_code = block["code"]
            break

    return {
        "response":  response,
        "test_code": test_code,
        "framework": framework
    }


# ── Mode 6: Pair programming chat ────────────────────────────────────────────

def pair_program(message: str, history: list, language: str = "python") -> str:
    """Multi-turn pair programming conversation."""
    history_text = ""
    for msg in history[-6:]:
        role         = "Developer" if msg["role"] == "user" else "AI Pair Programmer"
        history_text += f"{role}: {msg['content']}\n\n"

    prompt = (
        f"You are an expert AI pair programmer.\n"
        f"You are helping a developer solve coding problems through conversation.\n"
        f"Primary language context: {language}\n\n"
        f"When providing code solutions use markdown code blocks with language specified.\n"
        f"Keep explanations concise and practical.\n"
        f"Ask clarifying questions if the problem is unclear.\n\n"
        f"CONVERSATION HISTORY:\n{history_text}\n"
        f"Developer: {message}\n\n"
        f"AI Pair Programmer:"
    )

    return call_llm(prompt, max_tokens=1024)


# ── Code quality analysis ─────────────────────────────────────────────────────

def analyse_code_quality(code: str, language: str = "python") -> dict:
    """Quick code quality analysis."""
    prompt = (
        f"Analyse this {language} code for quality. Be brief and specific.\n\n"
        f"CODE:\n{FENCE}{language}\n{code[:2000]}\n{FENCE}\n\n"
        f"Rate each dimension 1-10 and give one specific improvement suggestion:\n\n"
        f"READABILITY: [score]/10 - [one suggestion]\n"
        f"EFFICIENCY: [score]/10 - [one suggestion]\n"
        f"ERROR HANDLING: [score]/10 - [one suggestion]\n"
        f"BEST PRACTICES: [score]/10 - [one suggestion]\n"
        f"OVERALL: [score]/10 - [one sentence verdict]"
    )

    response = call_llm(prompt, max_tokens=512)

    scores = {}
    for line in response.split("\n"):
        for dim in ["READABILITY", "EFFICIENCY", "ERROR HANDLING",
                    "BEST PRACTICES", "OVERALL"]:
            if line.startswith(dim):
                match = re.search(r"(\d+)/10", line)
                if match:
                    scores[dim.lower().replace(" ", "_")] = int(match.group(1))

    return {"response": response, "scores": scores}
