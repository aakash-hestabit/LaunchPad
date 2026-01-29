from autogen_core.tools import FunctionTool
import io
import contextlib
import traceback

def execute_python(code: str) -> str:
    """
    Execute Python code and return stdout or error.
    This function MUST remain deterministic and side-effect free.
    """
    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {}, {})
        output = stdout.getvalue()
        return output if output.strip() else "Execution finished with no output."

    except Exception:
        return "Execution Error:\n" + traceback.format_exc()


code_executor_tool = FunctionTool(
    execute_python,
    name="execute_python",
    description="Execute Python code and return stdout or execution errors.",
    strict=True
)