import os

codeowners_path = "./.gitlab/CODEOWNERS"
author = "@saboleznov"

with open(codeowners_path, "w", encoding='UTF-8') as f:
    f.write(f"* {author}\n")  # Правило по умолчанию для всех файлов
    for root, _, files in os.walk("."):
        if ".git" in root or ".gitlab" in root:
            continue
        for file in files:
            path = os.path.join(root, file).lstrip("./").replace('\\', '/')
            f.write(f"{path} {author}\n")
