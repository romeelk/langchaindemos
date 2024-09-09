from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL()

malicious_file_read = "f = open('main.py', 'r')\nprint(f.read())"

response = python_repl.run("for i in range(1,10):\
                                print(i)")
print(response)


malicious_response = python_repl.run(malicious_file_read)
print(malicious_response)

