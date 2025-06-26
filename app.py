import tkinter as tk
import random

flashcards = [
    {"question": "What is the capital of France?", "correct": "Paris", "wrong": "Rome"},
    {"question": "Who developed Python?", "correct": "Guido van Rossum", "wrong": "James Gosling"},
    {"question": "What is 3 x 4?", "correct": "12", "wrong": "9"},
    {"question": "Square root of 16?", "correct": "4", "wrong": "8"},
    {"question": "Which is the Red Planet?", "correct": "Mars", "wrong": "Venus"}
]

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🧠 Flashcard Quiz App")
        self.master.geometry("750x500")

        self.dark_mode = False  # Track mode
        self.themes = {
            True: {  # Dark
                "bg": "#2E2E2E", "fg": "#FFFFFF", "card_bg": "#3C3C3C",
                "btn1": "#4FC3F7", "btn2": "#FFD54F", "text1": "#000000", "highlight": "#90CAF9"
            },
            False: {  # Light
                "bg": "#E8F0FE", "fg": "#2C3E50", "card_bg": "#FFFFFF",
                "btn1": "#03A9F4", "btn2": "#FFC107", "text1": "#000000", "highlight": "#90CAF9"
            }
        }

        self.reset_quiz()

    def reset_quiz(self):
        self.score = 0
        self.current = 0
        self.timer_seconds = 5
        self.timer_id = None
        self.incorrect_answers = []
        self.total_questions = len(flashcards)

        self.create_widgets()
        self.next_question()

    def create_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        theme = self.themes[self.dark_mode]
        self.master.configure(bg=theme["bg"])

        top_frame = tk.Frame(self.master, bg=theme["bg"])
        top_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.score_label = tk.Label(top_frame, text=f"Score: {self.score}",
                                    font=("Segoe UI", 12, "bold"), bg=theme["bg"], fg=theme["fg"])
        self.score_label.pack(side="right")

        self.timer_label = tk.Label(top_frame, text=f"⏳ Time Left: {self.timer_seconds}s",
                                    font=("Segoe UI", 12), bg=theme["bg"], fg="#FF5252")
        self.timer_label.pack(side="right", padx=10)

        toggle_btn = tk.Button(top_frame, text="🌗 Toggle Mode", font=("Segoe UI", 10),
                               command=self.toggle_mode, bg=theme["highlight"], fg=theme["text1"], bd=0)
        toggle_btn.pack(side="left")

        self.card_frame = tk.Frame(self.master, bg=theme["card_bg"], padx=25, pady=25,
                                   highlightbackground=theme["highlight"], highlightthickness=2)
        self.card_frame.place(relx=0.5, rely=0.3, anchor="center", width=600, height=150)

        self.question_label = tk.Label(self.card_frame, text="", font=("Segoe UI", 14),
                                       wraplength=550, bg=theme["card_bg"], fg=theme["fg"], justify="center")
        self.question_label.pack(expand=True)

        self.option1 = tk.Button(self.master, text="", width=30, height=2,
                                 command=lambda: self.check_answer(self.option1["text"]),
                                 bg=theme["btn1"], fg=theme["text1"], font=("Segoe UI", 12), bd=0)
        self.option1.place(relx=0.3, rely=0.7, anchor="center")

        self.option2 = tk.Button(self.master, text="", width=30, height=2,
                                 command=lambda: self.check_answer(self.option2["text"]),
                                 bg=theme["btn2"], fg=theme["text1"], font=("Segoe UI", 12), bd=0)
        self.option2.place(relx=0.7, rely=0.7, anchor="center")

        self.result_label = tk.Label(self.master, text="", font=("Segoe UI", 13),
                                     bg=theme["bg"], fg=theme["fg"])
        self.result_label.place(relx=0.5, rely=0.88, anchor="center")

    def next_question(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        if self.current >= self.total_questions:
            self.show_final_result()
            return

        self.timer_seconds = 5
        self.update_timer()

        self.question = flashcards[self.current]
        self.question_label.config(text=f"Q{self.current + 1}: {self.question['question']}")

        options = [self.question["correct"], self.question["wrong"]]
        random.shuffle(options)

        self.option1.config(text=options[0], state="normal")
        self.option2.config(text=options[1], state="normal")

        self.countdown()

    def update_timer(self):
        self.timer_label.config(text=f"⏳ Time Left: {self.timer_seconds}s")

    def countdown(self):
        if self.timer_seconds > 0:
            self.update_timer()
            self.timer_seconds -= 1
            self.timer_id = self.master.after(1000, self.countdown)
        else:
            self.skip_question()

    def check_answer(self, selected):
        self.option1.config(state="disabled")
        self.option2.config(state="disabled")

        if selected == self.question["correct"]:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.incorrect_answers.append({
                "question": self.question["question"],
                "correct": self.question["correct"]
            })

        self.current += 1
        self.master.after(500, self.next_question)

    def skip_question(self):
        self.incorrect_answers.append({
            "question": self.question["question"],
            "correct": self.question["correct"]
        })
        self.current += 1
        self.next_question()

    def show_final_result(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        theme = self.themes[self.dark_mode]
        self.master.configure(bg=theme["bg"])

        tk.Label(self.master, text="🎉 Quiz Completed!", font=("Segoe UI", 22, "bold"),
                 bg=theme["bg"], fg="#81C784").pack(pady=20)

        tk.Label(self.master, text=f"Your Score: {self.score} / {self.total_questions}",
                 font=("Segoe UI", 15), bg=theme["bg"], fg=theme["fg"]).pack(pady=10)

        if self.incorrect_answers:
            tk.Label(self.master, text="❌ Missed Questions:", font=("Segoe UI", 13, "underline"),
                     bg=theme["bg"], fg="#FF6F61").pack()

            missed_frame = tk.Frame(self.master, bg=theme["bg"])
            missed_frame.pack(pady=5)
            for item in self.incorrect_answers:
                tk.Label(missed_frame, text=f"• {item['question']} → ✅ {item['correct']}",
                         font=("Segoe UI", 11), bg=theme["bg"], fg=theme["fg"]).pack(anchor="w")

        btn_frame = tk.Frame(self.master, bg=theme["bg"])
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="🔁 Restart", command=self.reset_quiz,
                  font=("Segoe UI", 12), bg="#AED581", fg="black", width=15).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="❌ Exit", command=self.master.quit,
                  font=("Segoe UI", 12), bg="#FF8A65", fg="black", width=15).grid(row=0, column=1, padx=10)

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        self.create_widgets()
        self.next_question()

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
