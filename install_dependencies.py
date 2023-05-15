import subprocess
import sys

def install_missing_dependencies(error):
    # Проверяем, что ошибка является ошибкой импорта модуля
    if isinstance(error, ModuleNotFoundError):
        module_name = str(error).split("'")[1] # Получаем название модуля из ошибки
        print(f"Module {module_name} not found. Installing...")

        try:
            # Используем subprocess для установки модуля через pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            print(f"Successfully installed {module_name}.")

        except subprocess.CalledProcessError as e:
            print(f"Failed to install {module_name}. Error: {e}")

def install_dependencies():
    # Пример использования функции
    try:
        import discord
        import pynacl
    except Exception as e:
        install_missing_dependencies(e)