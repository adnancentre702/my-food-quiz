import tkinter as tk
from tkinter import messagebox, font
import random

# --- Game Data ---
CATEGORIES = {
    'world': {'name': 'World Cuisine', 'icon': '🍕', 'color': '#F97316'},
    'ingredients': {'name': 'Ingredients', 'icon': '🥕', 'color': '#22C55E'},
    'sweets': {'name': 'Sweets & Desserts', 'icon': '🍦', 'color': '#EC4899'},
    'beverages': {'name': 'Beverages', 'icon': '☕', 'color': '#B45309'},
}

QUESTIONS = [
    {'id': 1, 'category': 'world', 'question': "Which country is the origin of the 'Caesar Salad'?", 'options': ["Italy", "United States", "Mexico", "France"], 'correct': 2, 'explanation': "Contrary to popular belief, it was invented by Caesar Cardini in Tijuana, Mexico.", 'difficulty': 'Medium'},
    {'id': 2, 'category': 'world', 'question': "What is the primary grain used in Japanese 'Sake'?", 'options': ["Wheat", "Barley", "Rice", "Corn"], 'correct': 2, 'explanation': "Sake is made by fermenting rice that has been polished to remove the bran.", 'difficulty': 'Easy'},
    {'id': 3, 'category': 'world', 'question': "Which distinct flavor is 'Umami'?", 'options': ["Sweet", "Salty", "Savory", "Bitter"], 'correct': 2, 'explanation': "Umami is the savory taste, often found in broths and cooked meats.", 'difficulty': 'Easy'},
    {'id': 4, 'category': 'world', 'question': "In which country would you find 'Pad Thai'?", 'options': ["Vietnam", "Thailand", "Malaysia", "Indonesia"], 'correct': 1, 'explanation': "Pad Thai is a stir-fried rice noodle dish from Thailand.", 'difficulty': 'Easy'},
    {'id': 5, 'category': 'ingredients', 'question': "Saffron comes from which flower?", 'options': ["Orchid", "Crocus", "Lily", "Rose"], 'correct': 1, 'explanation': "Saffron threads are the stigmas of the Crocus sativus flower.", 'difficulty': 'Hard'},
    {'id': 6, 'category': 'ingredients', 'question': "What is the main ingredient in Tofu?", 'options': ["Chickpeas", "Soybeans", "Lentils", "Almonds"], 'correct': 1, 'explanation': "Tofu is made by coagulating soy milk from soybeans.", 'difficulty': 'Easy'},
    {'id': 7, 'category': 'ingredients', 'question': "What pastry is used for Baklava?", 'options': ["Puff Pastry", "Shortcrust", "Phyllo", "Choux"], 'correct': 2, 'explanation': "Baklava uses layers of thin phyllo dough.", 'difficulty': 'Medium'},
    {'id': 8, 'category': 'sweets', 'question': "Tiramisu contains coffee-soaked...?", 'options': ["Panna Cotta", "Cannoli", "Ladyfingers", "Gelato"], 'correct': 2, 'explanation': "Tiramisu is made with coffee-soaked ladyfingers and mascarpone.", 'difficulty': 'Medium'},
    {'id': 9, 'category': 'sweets', 'question': "Macarons are primarily made from which nut flour?", 'options': ["Peanut", "Hazelnut", "Almond", "Walnut"], 'correct': 2, 'explanation': "Traditional French macarons use finely ground almond flour.", 'difficulty': 'Medium'},
    {'id': 10, 'category': 'beverages', 'question': "Which country consumes the most coffee per capita?", 'options': ["USA", "Italy", "Finland", "Brazil"], 'correct': 2, 'explanation': "Finland consistently tops the charts for coffee consumption.", 'difficulty': 'Hard'},
    {'id': 11, 'category': 'beverages', 'question': "Earl Grey tea is flavored with oil of which fruit?", 'options': ["Lemon", "Bergamot Orange", "Lime", "Grapefruit"], 'correct': 1, 'explanation': "Earl Grey is flavored with oil of bergamot orange.", 'difficulty': 'Medium'}
]

class FoodQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Foodie Quiz Master 👨‍🍳")
        self.root.geometry("500x700")
        self.root.configure(bg="#F8FAFC")
        
        self.header_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.sub_font = font.Font(family="Helvetica", size=14)
        self.norm_font = font.Font(family="Helvetica", size=11)
        self.bold_font = font.Font(family="Helvetica", size=11, weight="bold")

        self.score = 0
        self.streak = 0
        self.timer = 15
        self.current_q_index = 0
        self.selected_category = None
        self.active_questions = []
        self.lifelines = {'fifty': True, 'hint': True}
        self.timer_id = None
        
        self.setup_menu_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_menu_screen(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#F8FAFC", padx=20, pady=40)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="👨‍🍳", font=("Helvetica", 60), bg="#F8FAFC").pack(pady=10)
        tk.Label(frame, text="Foodie Quiz", font=self.header_font, bg="#F8FAFC", fg="#1E293B").pack()
        tk.Label(frame, text="Test your knowledge!", font=self.sub_font, bg="#F8FAFC", fg="#64748B").pack(pady=(0, 30))

        tk.Button(frame, text="🍽️ Mix All Categories", font=self.bold_font, bg="#F97316", fg="white", command=lambda: self.start_game(None), padx=20, pady=15).pack(fill="x", pady=10)

        for cat_id, cat_data in CATEGORIES.items():
            tk.Button(frame, text=f"{cat_data['icon']} {cat_data['name']}", font=self.norm_font, bg="white", command=lambda c=cat_id: self.start_game(c), padx=20, pady=10).pack(fill="x", pady=5)

    def start_game(self, category_id):
        self.selected_category = category_id
        if category_id:
            self.active_questions = [q for q in QUESTIONS if q['category'] == category_id]
        else:
            self.active_questions = list(QUESTIONS)
            random.shuffle(self.active_questions)
        
        self.score = 0
        self.streak = 0
        self.current_q_index = 0
        self.load_question()

    def load_question(self):
        self.timer = 15
        self.setup_game_screen()
        self.start_timer()

    def setup_game_screen(self):
        self.clear_window()
        top_bar = tk.Frame(self.root, bg="white", padx=15, pady=10)
        top_bar.pack(fill="x")
        
        self.lbl_score = tk.Label(top_bar, text=f"Score: {self.score}", font=self.bold_font, bg="white")
        self.lbl_score.pack(side="left")
        
        self.lbl_timer = tk.Label(top_bar, text=f"⏰ 00:{self.timer}", font=("Courier", 14, "bold"), bg="white")
        self.lbl_timer.pack(side="right")

        self.current_q = self.active_questions[self.current_q_index]
        q_frame = tk.Frame(self.root, bg="#F8FAFC", padx=20, pady=20)
        q_frame.pack(expand=True, fill="both")

        tk.Label(q_frame, text=self.current_q['question'], font=("Helvetica", 14, "bold"), bg="#F8FAFC", wraplength=400).pack(pady=20)

        self.option_buttons = []
        for idx, text in enumerate(self.current_q['options']):
            btn = tk.Button(q_frame, text=text, font=self.norm_font, bg="white", command=lambda i=idx: self.handle_answer(i), pady=10)
            btn.pack(fill="x", pady=5)
            self.option_buttons.append(btn)

    def start_timer(self):
        if self.timer_id: self.root.after_cancel(self.timer_id)
        self.update_timer()

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1
            self.lbl_timer.config(text=f"⏰ 00:{self.timer:02d}")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.handle_answer(-1)

    def handle_answer(self, choice_idx):
        if self.timer_id: self.root.after_cancel(self.timer_id)
        correct = self.current_q['correct']
        
        if choice_idx == correct:
            self.score += 100
            messagebox.showinfo("Correct!", self.current_q['explanation'])
        else:
            messagebox.showerror("Wrong!", self.current_q['explanation'])

        if self.current_q_index < len(self.active_questions) - 1:
            self.current_q_index += 1
            self.load_question()
        else:
            messagebox.showinfo("Finished", f"Your final score: {self.score}")
            self.setup_menu_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodQuizApp(root)
    root.mainloop()