# code_executor.py
# Windows-compatible safe Python code executor

import sys
import io
import traceback
import contextlib


def execute_python(code: str) -> dict:
    """
    Safely execute Python code in an isolated namespace.
    Returns { output, error, success }

    Safety measures:
    - Separate namespace (no access to globals)
    - stdout/stderr captured
    - Blocks dangerous imports
    """
    # Block dangerous operations
    blocked = [
        "import os",
        "import sys",
        "import subprocess",
        "import socket",
        "__import__",
        "open(",
        "exec(",
        "eval(",
        "compile("
    ]
    for b in blocked:
        if b in code:
            return {
                "output":  "",
                "error":   f"Blocked: '{b}' is not allowed in sandboxed execution.",
                "success": False
            }

    # Capture stdout and stderr
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # Safe builtins — only harmless functions allowed
    safe_builtins = {
        "print":      print,
        "len":        len,
        "range":      range,
        "enumerate":  enumerate,
        "zip":        zip,
        "map":        map,
        "filter":     filter,
        "sorted":     sorted,
        "reversed":   reversed,
        "sum":        sum,
        "min":        min,
        "max":        max,
        "abs":        abs,
        "round":      round,
        "int":        int,
        "float":      float,
        "str":        str,
        "bool":       bool,
        "list":       list,
        "dict":       dict,
        "set":        set,
        "tuple":      tuple,
        "type":       type,
        "isinstance": isinstance,
        "issubclass": issubclass,
        "hasattr":    hasattr,
        "getattr":    getattr,
        "repr":       repr,
        "hash":       hash,
        "id":         id,
        "any":        any,
        "all":        all,
    }

    safe_globals = {"__builtins__": safe_builtins}

    try:
        with contextlib.redirect_stdout(stdout_capture):
            with contextlib.redirect_stderr(stderr_capture):
                exec(code, safe_globals)   # noqa: S102

        output = stdout_capture.getvalue()
        error  = stderr_capture.getvalue()

        return {
            "output":  output if output.strip() else "(Code ran successfully — no output)",
            "error":   error,
            "success": True
        }

    except Exception:
        return {
            "output":  stdout_capture.getvalue(),
            "error":   traceback.format_exc(),
            "success": False
        }
