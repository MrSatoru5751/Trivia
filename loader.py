import json
import os

# Path of the questions
base_path = os.path.join(os.path.dirname(__file__), "Questions")

# Load the data of the JSIN file
def load_questions(category, language="es"):
    file_path = os.path.join(base_path, f"{category.lower()}_{language}.json")
    
    if not os.path.exists(file_path):
        print(f"There is no existing file: {file_path}")
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error al leer el archivo JSON: {file_path}")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

# Get an specific question
def get_question(questions, index):
    if index < len(questions):
        return questions[index]
    return None
