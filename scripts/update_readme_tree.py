import os
import pathspec
import re

README_PATH = "README.md"
START_MARK = "<!-- BEGIN FILE TREE -->"
END_MARK = "<!-- END FILE TREE -->"
DESCRIPTION_COLUMN = 60  # где должна начинаться колонка с описанием

def load_gitignore():
    try:
        with open(".gitignore", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return pathspec.PathSpec.from_lines("gitwildmatch", lines)
    except FileNotFoundError:
        return pathspec.PathSpec([])

def extract_existing_descriptions(readme_text):
    """Извлекает описания файлов из текущего дерева"""
    tree_block = re.search(f"{START_MARK}.*?```(.*?)```.*?{END_MARK}", readme_text, re.DOTALL)
    if not tree_block:
        return {}
    lines = tree_block.group(1).strip().splitlines()
    description_map = {}
    for line in lines:
        if "—" in line:
            path_part = line.split("—")[0].rstrip()
            desc = line.split("—", 1)[1].strip()
            description_map[path_part] = desc
    print(description_map)
    return description_map

def generate_tree_lines(ignore_spec, existing_descriptions):
    raw_lines = []
    spec = load_gitignore()

    def walk(dir_path, prefix=""):
        entries = sorted(os.listdir(dir_path))
        entries = [e for e in entries if not ignore_spec.match_file(os.path.join(dir_path, e))]
        for index, name in enumerate(entries):
            full_path = os.path.join(dir_path, name)
            connector = "└── " if index == len(entries) - 1 else "├── "
            rel_path = os.path.relpath(full_path, ".").replace("\\", "/")

            # Пропускаем .git и .gitlab
            if rel_path in [".git"]:
                continue

            # Проверка игнора
            if spec.match_file(rel_path):
                continue


            line_prefix = f"{prefix}{connector}{name}"
            raw_lines.append((line_prefix, existing_descriptions.get(line_prefix)))
            if os.path.isdir(full_path):
                new_prefix = prefix + ("    " if index == len(entries) - 1 else "│   ")
                walk(full_path, new_prefix)

    raw_lines.insert(0, (".", existing_descriptions.get(".")))
    walk('.')

    max_length = max(len(line) for line, _ in raw_lines)
    max_length = max(max_length + 2, DESCRIPTION_COLUMN)

    result = []
    for line, desc in raw_lines:
        if desc:
            padding = " " * (max_length - len(line))
            result.append(f"{line}{padding}— {desc}")
        else:
            result.append(line)

    return result

def update_readme(tree_lines):
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme = f.read()
    except FileNotFoundError:
        readme = ""

    tree_block = (
        f"{START_MARK}\n"
        "```\n" +
        "\n".join(tree_lines) +
        "\n```\n" +
        f"{END_MARK}"
    )

    if START_MARK in readme and END_MARK in readme:
        updated = re.sub(
            f"{START_MARK}.*?{END_MARK}",
            tree_block,
            readme,
            flags=re.DOTALL
        )
    else:
        updated = readme.strip() + "\n\n" + tree_block

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)

def main():
    ignore_spec = load_gitignore()
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_text = f.read()
    except FileNotFoundError:
        readme_text = ""

    existing_descriptions = extract_existing_descriptions(readme_text)
    tree_lines = generate_tree_lines(ignore_spec, existing_descriptions)
    update_readme(tree_lines)

if __name__ == "__main__":
    main()
