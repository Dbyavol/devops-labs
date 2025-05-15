import os


def read_gitignore():
    """Читает файл .gitignore и возвращает список игнорируемых путей."""
    ignore_paths = []
    try:
        with open(".gitignore", "r", encoding="UTF-8") as f:
            for line in f:
                # Убираем комментарии и пустые строки
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Добавляем путь в список игнорируемых
                ignore_paths.append(line)
    except FileNotFoundError:
        # Если .gitignore не найден, просто возвращаем пустой список
        pass
    return ignore_paths

def should_ignore(path, ignore_paths):
    """Проверяет, должен ли файл быть проигнорирован согласно .gitignore."""
    for ignore_pattern in ignore_paths:
        # Если путь начинается с игнорируемого шаблона, пропускаем его
        if path.startswith(ignore_pattern) or path == ignore_pattern:
            return True
    return False

def generate_codeowners(author="@saboleznov"):
    """Генерирует файл CODEOWNERS."""
    codeowners_path = "./.gitlab/CODEOWNERS"
    ignore_paths = read_gitignore()

    with open(codeowners_path, "w", encoding="UTF-8") as f:
        f.write(f"* {author}\n")  # Правило по умолчанию для всех файлов

        for root, _, files in os.walk("."):
            # Пропускаем директории .git и .gitlab
            if ".git" in root or ".gitlab" in root:
                continue

            for file in files:
                path = os.path.join(root, file).lstrip("./").replace("\\", "/")
                # Проверяем, должен ли файл быть проигнорирован
                if should_ignore(path, ignore_paths):
                    continue
                f.write(f"{path} {author}\n")


generate_codeowners()