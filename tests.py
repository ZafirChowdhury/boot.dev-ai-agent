from functions.get_files_info import get_files_info

print(get_files_info("calculator", "../"))
print(get_files_info("calculator", "./"))
print(get_files_info("calculator", "/something"))

print(get_files_info("calculator"))
print(get_files_info("calculator", "pkg"))

print(get_files_info("calculator", "main.py"))
print(get_files_info("calculator", "something"))