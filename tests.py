from functions.get_files_info import get_files_info, get_file_content, write_file, run_python_file

#TEST FOR get_files_info
def test_get_files_info():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)

#TEST for get_file_content
def test_get_file_content ():
    result = get_file_content("calculator", "main.py")
    print("TEST 2.1")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("TEST 2.2")
    print(result)
    print("")

    result = get_file_content("calculator", "/bin/cat")
    print("TEST 2.3")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("TEST 2.4")
    print(result)
    print("")

#TEST write_file
def test_write_file():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("TEST 3.1")
    print(result)
    print("")

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("TEST 3.2")
    print(result)
    print("")

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("TEST 3.3")
    print(result)
    print("")

#TEST run_python_file
def test_run_python_file():
    result = run_python_file("calculator", "main.py")
    print("TEST 4.1")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("TEST 4.2")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("TEST 4.4")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("TEST 4.5")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py") 
    print("TEST 4.6")
    print(result)
    print("")


if __name__ == "__main__":
    #test_get_file_content()
    #test_get_files_info():
    #test_write_file()
    test_run_python_file()