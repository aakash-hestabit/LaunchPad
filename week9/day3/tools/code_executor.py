from autogen_core.tools import FunctionTool
import asyncio
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool

work_dir = "./code_output"
executor = LocalCommandLineCodeExecutor(work_dir=work_dir, timeout=100)
code_tool =  PythonCodeExecutionTool(executor)