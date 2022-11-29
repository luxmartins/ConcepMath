#TODO: Add GUI (v2.0.0)
#TODO: Optimize?

#TODO: Stylize calculation frame

from random import randint
import tkinter as tk
import tkinter.font as tkFont
import winsound as ws
import customtkinter as ct

global_padding = (10, 10)

class operations():
    "Decorative class used to group respective methods visually"

    @staticmethod
    def addition() -> int:
        "Adds two random integers and returns the sum"
        a,b = randint(0,9), randint(0,9)
        lbl_specified_exercise.configure(text=f"{a} + {b} = ")
        return a+b

    @staticmethod
    def subtraction() -> int:
        "Subtracts two random integers and returns the difference"
        a,b = randint(0,9), randint(0,9)
        while a<b:
            a,b = randint(0,9), randint(0,9)
        lbl_specified_exercise.configure(text=f"{a} - {b} = ")
        return a-b
    
    @staticmethod
    def multiplication() -> int:
        "Multiplies two random integers and returns the product"
        a,b = randint(0,9), randint(0,9)
        lbl_specified_exercise.configure(text=f"{a} x {b} = ")
        return a*b

    @staticmethod
    def division() -> int:
        "Divides two random integers and returns the quotient"
        a,b = randint(0,10), randint(1,10)
        lbl_specified_exercise.configure(text=f"{a*b} : {b} = ")
        return (a*b)/b

    @staticmethod
    def mixed_problems():
        "Calls a random operation method and returns its output"
        input_option_dict = {1 : operations.addition, 2: operations.subtraction, 3: operations.multiplication, 4: operations.division, 5: operations.mixed_problems}
        return input_option_dict[randint(1,5)]()
        
# Sets the title on the calculation screen
def title_set(name: str):
    lbl_title_calculation.configure(text=name)

# Defines needed variables and calls the corresponding functions
def game_loop(operation, operation_str:str=None):
    "Defines needed variables and calls the corresponding functions."
    global correct_answer
    global current_operation
    frm_calculation.lift() # Makes the exercise visible
    if operation_str != None:
        title_set(operation_str)
    current_operation = operation
    correct_answer = operation()

# Using a class to organize methods that handle user actions
class handlers:
    
    # Called when the "check_answer" button is pressed
    @staticmethod
    def check_button_handler(event=None):
        "Checks if the answer is correct, updates counters accordingly and reruns the gameloop function"
        try:
            user_input = int(ent_answer_space.get()) # Checks if the inputted answer is an integer
            lbl_wrong_answer.configure(text="")
            if correct_answer == user_input: # Checks if the answer is correct or not and updates the counters accordingly
                counters.increase_correct_count()
                lbl_count_right.configure(text=f"Certo: {counters.amount_correct}")
            else:
                counters.increase_wrong_count()
                lbl_count_wrong.configure(text=f"Erro: {counters.amount_wrong}")
                lbl_wrong_answer.configure(text=f"A resposta correta era:  {int(correct_answer)}")
            ent_answer_space.delete(0, "end") # Clears entry box
            game_loop(current_operation)
        except ValueError: # Warns user that only numbers are permitted
                lbl_wrong_answer.configure(text="Apenas números são permitidos!")
                ent_answer_space.delete(0, "end") # Clears entry box

    # Called when the "end_calculations" button is pressed
    @staticmethod
    def return_to_main_menu():
        "Returns to main menu and resets the calculation screen"
        frm_calculation.lower() # Hides calculation screen
        # Resets calculation screen
        lbl_wrong_answer.configure(text="")
        counters.reset()
        lbl_count_right.configure(text=f"Correto: {counters.amount_correct}")
        lbl_count_wrong.configure(text=f"Erro: {counters.amount_wrong}")
        root.focus() # Prevents the entry box from receiving input while in the menu screen

"""
Plays sound effect when called. Numbers under 3 will play a random "correct" effect sound while
anything above 3 will result in a random "wrong" sound effect
"""

def SoundEffect(RandInt):
    sounds = {1:'Sound1Correct.wav', 2:'Sound2Correct.wav', 3:'Sound3Correct.wav', 4:"Sound4Wrong.wav"}
    ws.PlaySound("Sound Effects\\" + sounds[RandInt], ws.SND_FILENAME)

# A simple class to eliminate the need of global variables and group similar methods related to the counters
class counters:

    amount_wrong, amount_correct = 0, 0

    def reset():
        "Resets counters on calculation screen"
        counters.amount_wrong, counters.amount_correct = 0, 0
    
    def increase_correct_count():
        "Increases correct counter by one on calculation screen"
        counters.amount_correct +=1
        SoundEffect(randint(1,3))
    
    def increase_wrong_count():
        "Decreases correct counter by one on calculation screen"
        counters.amount_wrong +=1
        SoundEffect(4)

# Defining the root window
root = tk.Tk()
root.title("Exercícios de Matemática v3.0.0")
root.rowconfigure(1, minsize=825, weight=1, )
root.columnconfigure(1, minsize=500, weight=1)
root.resizable(width=False, height=False)

title_font = tkFont.Font(family="Arial", size=28, weight="bold") # Font object used for the title


# Frame containing the main menu widgets
frm_home = tk.Frame(root, background="#272B34")
frm_home.rowconfigure(0, weight=1, minsize=175)
frm_home.rowconfigure(1, minsize=500, weight=1)
frm_home.rowconfigure(2, minsize=150, weight=1)
frm_home.columnconfigure(0, weight=1, minsize=500)
frm_home.grid(row=1, column=1, sticky="nesw")
# Creating frame for the menu
frm_menu = tk.Frame(frm_home, background="#272B34") #frm == frame
frm_menu.grid(row=1, column=0, sticky="nesw", pady=global_padding[1])
frm_menu.rowconfigure([0,1,2], minsize=150, weight=1)
frm_menu.columnconfigure([0,1,2,3,4,5], minsize=100, weight=1)

# Creating header
lbl_title = tk.Label(frm_home, text="Exercícios de Matemática", bg="#4C797B", font=title_font, fg="#FFFFFF")
lbl_title.grid(row=0, column=0, sticky="nesw", pady=(0, global_padding[1]*2))

# Creating addition button
btn_addition = ct.CTkButton(frm_menu, text="Soma", command=lambda: game_loop(operations.addition, "Soma"), fg_color="#F28963", hover_color="#D67451",border=0, corner_radius=15, text_color="#FFFFFF", text_font=("Arial",12,'bold'))
btn_addition.grid(row=0, column=1, columnspan=2, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

# Creating subtraction button
btn_subtraction = ct.CTkButton(frm_menu, text="Subtrair", command=lambda: game_loop(operations.subtraction, "Subtrair"), fg_color="#F28963", hover_color="#D67451",border=0, corner_radius=15, text_color="#FFFFFF", text_font=("Arial",12,'bold'))
btn_subtraction.grid(row=0, column=3, columnspan=2, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

# Creating multiplication button
btn_multiplication = ct.CTkButton(frm_menu, text="Multiplicar", command=lambda: game_loop(operations.multiplication, "Multiplicar"), fg_color="#F28963", hover_color="#D67451",border=0, corner_radius=15, text_color="#FFFFFF", text_font=("Arial",12,'bold'))
btn_multiplication.grid(row=1, column=1, columnspan=2, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

# Creating division button
btn_division = ct.CTkButton(frm_menu, text="Dividir", command=lambda: game_loop(operations.division, "Dividir"), fg_color="#F28963", hover_color="#D67451",border=0, corner_radius=15, text_color="#FFFFFF", text_font=("Arial",12,'bold'))
btn_division.grid(row=1, column=3, columnspan=2, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

# Creating mixed_problems button
btn_mixed_problems = ct.CTkButton(frm_menu, text="Problemas mistos", command=lambda: game_loop(operations.mixed_problems, "Problemas mistos"), fg_color="#F28963", hover_color="#D67451",border=0, corner_radius=15, text_color="#FFFFFF", text_font=("Arial",12,'bold'))
btn_mixed_problems.grid(row=2, column=1, columnspan=4, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

# Creating footer
lbl_copyright = tk.Label(frm_home, text="\u00A9 2022 Educação de matemática", bg="#202020", fg="white")
lbl_copyright.grid(row=2, column=0, sticky="nesw", pady=(global_padding[1]*2, 0))


# Creating calculation frame
frm_calculation = tk.Frame(root, background="#272B34") #alterar a cor do fundo aqui
frm_calculation.rowconfigure([0,1,2,3,4,5], minsize=100, weight=1)
frm_calculation.rowconfigure(0, weight=1, minsize=175)
frm_calculation.rowconfigure(5, minsize=150, weight=1)
frm_calculation.columnconfigure([0,1,2,3], minsize=100, weight=1)
frm_calculation.grid(row=1, column=1, sticky="nesw")
frm_calculation.lower() # Hides frame initially

# Creating header
lbl_title_calculation = tk.Label(frm_calculation, text="Exercícios de Matemática", bg="#4C797B", font=title_font, fg="white")
lbl_title_calculation.grid(row=0, column=0, columnspan=5, sticky="nesw", pady=(0, global_padding[1]*2))

# Creating end_calculations button
btn_end_calculations = ct.CTkButton(frm_calculation, text="Menu", command=handlers.return_to_main_menu, width=70, height=50, fg_color="#F28963", hover_color="#D67451",border=0, corner_radius=10, text_color="#FFFFFF", text_font=("Arial",12,'bold'))
btn_end_calculations.grid(row=1, column=3, sticky="ne", padx= global_padding[1], pady=global_padding[1])

# Creating specified_exercise label, ent_answer_space entry box and check_answer btn
lbl_specified_exercise =tk.Label(frm_calculation, font=("Arial",30), fg="#FFFFFF", bg="#272B34")
lbl_specified_exercise.grid(row=2, column=0, columnspan=2, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

ent_answer_space = ct.CTkEntry(frm_calculation,text_font=("Arial", 25), width=200, bg="#393939", corner_radius=15)
ent_answer_space.grid(row=2, column=2, sticky="ns", padx= global_padding[0], pady=global_padding[1])
#add photoimage
photo = tk.PhotoImage(file="btn.png")

btn_check_answer = tk.Button(frm_calculation, image = photo, command=handlers.check_button_handler, bg="#272B34", background='#272B34', border=0, activebackground='#272B34', width=200)
btn_check_answer.grid(row=2, column=3, padx= global_padding[0], pady=global_padding[1])

# Creating wrong_answer label
lbl_wrong_answer = tk.Label(frm_calculation, fg="red", font=("Arial", 15), bg="#272B34")
lbl_wrong_answer.grid(row=3, column=0, columnspan=4, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

# Creating count_right and count_wrong labels
lbl_count_right = ct.CTkLabel(frm_calculation, text="Correto: 0", fg_color="#4C797B", corner_radius=10)
lbl_count_right.grid(row=4, column=0,columnspan=2, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

lbl_count_wrong = ct.CTkLabel(frm_calculation, text="Erro: 0", fg_color="#C14E63", corner_radius=10)
lbl_count_wrong.grid(row=4, column=2,columnspan=2, sticky="nesw", padx= global_padding[0], pady=global_padding[1])

# Creating footer
lbl_copyright = tk.Label(frm_calculation, text="\u00A9 2022 Edicação de matemática", bg="#202020", fg="white")
lbl_copyright.grid(row=5, column=0, columnspan=5, sticky="nesw", pady=(global_padding[1]*2, 0))

ent_answer_space.bind("<Return>", handlers.check_button_handler)

# Function called upon runtime as a script
def main():
    root.mainloop()  

# Only runs the script if it is run directly and not imported as an external file
if __name__ == '__main__':
    main()