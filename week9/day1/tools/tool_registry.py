from autogen_core.tools import FunctionTool
from tools.web_search import search_and_clean

print("importing the tool")
web_search_tool = FunctionTool(
    search_and_clean,
    description="Search the web and return cleaned factual results."
)
print(web_search_tool)