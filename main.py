import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *

#HARD CODED PROMPT:________________________________________________________________________________

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

#_________________________________________________________________________________________________
#################bulding the SCHEMA for the functions function:##################################

#get_files_info
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

#get_file_content
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the file contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Required file path, relative to the working directory. Relative file_path must be provided.",
            ),
        },
    ),
)

#run_python_file
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with args as a list of argument: returns a string with STDOUT, STDERR and exit code, if it applies, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Required file path, relative to the working directory. Relative file_path must be provided."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="OPTIONA, NOT REQUIRED! List of string, the default value is []. The arguments to be used in the function.",
                required=[]
            ),
        },
    ),
)

#run_write_file
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes into a target file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Required file path of the file, relative to the working directory. Relative file_path must be provided."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String to be written to the target file"
            ),
        },
    ),
)


#AVAILABLE FUNCTIONS create with types.Tool:
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
#_________________________________________________________________________________________________

#FUNCTION THAT CALLS FUNCTIONS FOR THE AI:

#1st Create a dictionary with the available functions:
FUNCTIONS = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}
#FUNCTION CALLER
def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    kwargs = dict(function_call_part.args or {})
    if name == "run_python_file": kwargs.setdefault("args", [])
    kwargs["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {name}({kwargs})")
    else:
        print(f" - Calling function: {name}")
    #TEST if function is valid:
    if name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )   
    #function executed, returning a typecontent:
    result = FUNCTIONS[name](**kwargs)
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=name,
            response={"result": result},
        )],
    )



load_dotenv()


def eprint(msg):
    print(msg, file=sys.stderr)

def main():
    verbose = False

    if len(sys.argv) < 2:
        eprint("Please enter a query in quotes.")
        sys.exit(1) #can also use return, i used sys.exit because this tiny script was originally in global scope

    if sys.argv[-1] == "--verbose":
        verbose = True
        user_prompt = " ".join(sys.argv[1:-1])
    else:
        user_prompt = " ".join(sys.argv[1:])
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: 
        print("GEMINI_API_KEY NOT SET, visit Google AI Studio.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for i in range(20):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents= messages, config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt)
            )
        except Exception as exc:
            eprint(f"API error: {exc}")
            sys.exit(1)

        for cand in response.candidates or []:
            messages.append(cand.content)
    

        if response.function_calls:
            for function in response.function_calls:
                tool_content = call_function(function, verbose)
                #append the response:
                fr = tool_content.parts[0].function_response
                messages.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=fr.name,
                                response=fr.response,
                            )                  
                        ],
                    )
                )
            continue
        
        if response.text:
            print(response.text)
            break
        if not response.function_calls and not response.text:
            break

    

    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")




if __name__ == "__main__":
    main()