# GPT코드입니다. 제가짠거 아니에요
import os


def scan_for_todo(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for file_name in filenames:
            if file_name == "check_todo.py":
                continue
            if not (file_name.endswith(".todo") or file_name.endswith(".py")):
                continue
            relative_path = os.path.relpath(os.path.join(dirpath, file_name), root_dir)
            try:
                with open(
                    os.path.join(dirpath, file_name), "r", encoding="UTF-8"
                ) as file:
                    if file_name.endswith(".todo"):
                        print(f"TODO path: {relative_path}")
                        print(file.read().strip())
                    else:
                        for line in file:
                            if "TODO" in line:
                                print(f"TODO path: {relative_path}")
                                print(line.strip())
            except UnicodeDecodeError:
                print(f"Could not decode file: {relative_path}")


if __name__ == "__main__":
    project_root = "./"
    scan_for_todo(project_root)
