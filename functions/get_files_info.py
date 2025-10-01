import os
import subprocess

#CONSTANTS
MAX_CHARACTERS = 10_000

def get_files_info(working_directory, directory="."):
	fullpath = os.path.join(working_directory, directory)
	abs_work = os.path.abspath(working_directory)
	abs_target = os.path.abspath(fullpath)
	#checking if the directory is outside of the working_directory or not a directory
	if not (abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	if not os.path.isdir(abs_target):
		return f'Error: "{directory}" is not a directory'
	#Catching all possible errors with try/except:
	try:
		contents = sorted(os.listdir(path=abs_target))
		dir_contents = ""
		for content in contents:
			c_path = os.path.join(abs_target, content)
			c_size = os.path.getsize(c_path)
			c_isdir = os.path.isdir(c_path)
			dir_contents += f" - {content}: file_size={c_size} bytes, is_dir={c_isdir}\n"
		return dir_contents
	except Exception as e:
		return f"Error: {e}"


def get_file_content(working_directory, file_path):
	fullpath = os.path.join(working_directory, file_path)
	abs_work = os.path.abspath(working_directory)
	abs_target = os.path.abspath(fullpath)
	#same as before
	if not (abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
		return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
	#must be a file
	if not os.path.isfile(abs_target):
		return f'Error: File not found or is not a regular file: "{file_path}"'
	
	try:
		#we open the file safely with a with statement
		with open(abs_target, "r") as f:
			file_content_string = f.read(MAX_CHARACTERS + 1)
		if len(file_content_string) > MAX_CHARACTERS:
			file_content_string = file_content_string[:MAX_CHARACTERS] + f'[...File "{file_path}" truncated at 10000 characters]'
		return file_content_string
	except Exception as e:
		return f"Error: {e}"
	

#Time to write files:

def write_file(working_directory, file_path, content):
	fullpath = os.path.join(working_directory, file_path)
	abs_work = os.path.abspath(working_directory)
	abs_target = os.path.abspath(fullpath)
	#checking if the filepath is within the working path
	if not(abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	#TRY-EXCEPT, for catching erros
	try:
		dir_path = os.path.dirname(abs_target)
		os.makedirs(dir_path, exist_ok=True)
		with open(abs_target, "w") as r: r.write(content)
		return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
	except Exception as e:
		return f"Error: {e}"


#Run Python:

def run_python_file(working_directory, file_path, args=[]):
	fullpath = os.path.join(working_directory, file_path)
	abs_work = os.path.abspath(working_directory)
	abs_target = os.path.abspath(fullpath)
	#once agan, checking if thte filepath is within the working path
	if not(abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
	#we check if the path exists:
	if not os.path.exists(fullpath):
		return f'Error: File "{file_path}" not found.'
	#checking if the file is .py
	if not fullpath.endswith(".py"):
		return f'Error: "{file_path}" is not a Python file.'
	
	try:
		#Executing the python file to create a completed_process object
		completed_process = subprocess.run(["python", file_path, *args], capture_output=True, text=True, timeout=30, cwd=working_directory)
		#returning completed_process error or no output and
		#returning string of stdout and stderr
		output = f"STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}"
		if completed_process.stdout == "" and completed_process.stderr == "": output = "No output produced."
		if completed_process.returncode != 0 : output +=  f" Process exited with code {completed_process.returncode}"
		return output
	except Exception as e:
		return f"Error: executing Python file: {e}"






			



