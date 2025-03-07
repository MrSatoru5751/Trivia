import tkinter as tk
from tkinter import messagebox
import random
from loader import load_questions, get_question

class TriviaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Game")
        
        self.language = None
        self.difficulty = "Fácil" 
        self.questions = []
        self.question_index = 0
        self.score = 0

        self.create_language_selection()

    def create_language_selection(self):
        """Initial screen to select the language"""
        self.clear_window()

        tk.Label(self.root, text="Elige tu idioma", font=("Arial", 14)).pack(pady=20)
        
        tk.Button(self.root, text="Español", font=("Arial", 12), command=lambda: self.set_language("es")).pack(pady=10)

    def set_language(self, language):
        """Save the language and shows the main menu"""
        self.language = language
        self.create_main_menu()

    def create_main_menu(self):
        """Main menu with some options"""
        self.clear_window()

        tk.Label(self.root, text="Menú Principal", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Jugar", font=("Arial", 12), command=self.start_game).pack(pady=10)
        tk.Button(self.root, text="Seleccionar Dificultad", font=("Arial", 12), command=self.select_difficulty).pack(pady=10)
        tk.Button(self.root, text="Información", font=("Arial", 12), command=self.show_info).pack(pady=10)

    def select_difficulty(self):
        """In this screen the user can select the difficulty"""
        self.clear_window()

        tk.Label(self.root, text="Selecciona una dificultad", font=("Arial", 14)).pack(pady=20)

        tk.Radiobutton(self.root, text="Fácil", variable=self.difficulty, value="Easy", command=lambda: self.set_difficulty("Easy")).pack()
        tk.Radiobutton(self.root, text="Medio", variable=self.difficulty, value="Medium", command=lambda: self.set_difficulty("Medium")).pack()

        tk.Button(self.root, text="Volver", font=("Arial", 12), command=self.create_main_menu).pack(pady=20)

    def set_difficulty(self, difficulty):
        """Guarda la dificultad seleccionada y vuelve al menú principal"""
        self.difficulty = difficulty
        messagebox.showinfo("Dificultad seleccionada", f"Has seleccionado: {difficulty}")
        self.create_main_menu()

    def show_info(self):
        """Show some information about the game"""
        messagebox.showinfo("Información", "Este es un juego de trivia donde debes responder preguntas correctamente para ganar puntos.\n Son +10 puntos por cada respuesta correcta y -15 por cada incorrecta.")
        
    def start_game(self):
        """Load the questions and start the game"""
        categories = ["movies"] # In a future there will be more categories
        category = random.choice(categories)  # The category is random

        all_questions = load_questions(category, self.language)
        self.questions = [q for q in all_questions if q["difficulty"] == self.difficulty]
        self.question_index = 0
        self.score = 0

        if not self.questions:
            messagebox.showerror("Error", "No hay preguntas disponibles.")
            return

        self.create_game_interface()

    def create_game_interface(self):
        """Create the interface for the trivia game"""
        self.clear_window()

        self.question_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400)
        self.question_label.pack(pady=20)

        self.answer_buttons = []
        for i in range(4):
            btn = tk.Button(self.root, text="", font=("Arial", 12), width=30, command=lambda i=i: self.verify_answer(i))
            btn.pack(pady=5)
            self.answer_buttons.append(btn)

        self.score_label = tk.Label(self.root, text=f"Puntaje: {self.score}", font=("Arial", 12), fg="green")
        self.score_label.pack(pady=10)

        tk.Button(self.root, text="Volver al Menú", font=("Arial", 12), command=self.create_main_menu).pack(pady=10)

        self.show_question()

    def show_question(self):
        """Shows the next question"""
        question = get_question(self.questions, self.question_index)
        if question:
            self.question_label.config(text=question["question"])
            for i, option in enumerate(question["options"]):
                self.answer_buttons[i].config(text=option)
        else:
            messagebox.showinfo("Fin del Juego", f"Juego terminado. Puntaje final: {self.score}")
            self.create_main_menu()

    def verify_answer(self, index):
        """Verify the selected answer"""
        question = get_question(self.questions, self.question_index)
        if not question:
            return
        
        correct_answer = question["answer"]
        
        if self.answer_buttons[index].cget("text") == correct_answer:
            self.score += 10
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
        else:
            self.score -= 15
            messagebox.showerror("Incorrecto", f"La respuesta correcta es: {correct_answer}")

        self.score_label.config(text=f"Puntaje: {self.score}")

        # Next question
        self.question_index += 1
        if self.question_index < len(self.questions):
            self.show_question()
        else:
            messagebox.showinfo("Fin del Juego", f"Juego terminado. Puntaje final: {self.score}")
            self.create_main_menu()

    def clear_window(self):
        """Delete all the element in the actual window"""
        for widget in self.root.winfo_children():
            widget.destroy()
