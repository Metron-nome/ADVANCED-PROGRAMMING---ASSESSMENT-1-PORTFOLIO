import tkinter as tk
from random import randint, choice

Difficulty_Level_Quiz = {
    "Easy": (1, 1, 0, 9),
    "Medium": (2, 2, 10, 99),
    "Hard": (4, 4, 1000, 9999)
}
Quiz_Length = 10
Max_Score = 100

Root_Window = tk.Tk()


Current_Problem_Set = []
Score = 0
Question_Index = 0
Difficulty_Level = ""
Attempts_Used = 0
Current_Correct_Answer = 0


Question_Label = None
Answer_Entry = None
Feedback_Label = None


def Clear_Window_Widgets():
    for Widget in Root_Window.winfo_children():
        Widget.destroy()

# The random number generator for each difficulty, since it's random, it's not a fixed set of numbers to guarantee a win.
# This will just allow the code to run through the numbers of the difficulty based on the difficulty the user chooses.
def Random_Int(Difficulty):
    _, _, Min_Val, Max_Val = Difficulty_Level_Quiz.get(Difficulty, (1, 1, 0, 9))
    return randint(Min_Val, Max_Val)

# The code will decide by itself if the questions will be either adding or subtracting.
def Decide_Operation():
    return choice(['+', '-'])

# This will display the result of the quiz based on the score of the user.
def Display_Results():
    Clear_Window_Widgets()

    tk.Label(Root_Window, text="Quiz Complete! Great Job!", font=("Segoe Print", 18, "bold"), fg="#3366AA").pack(pady=15)
    
  
    tk.Label(Root_Window, text="Your Final Score: {} out of {} Points".format(Score, Max_Score), font=("Segoe Print", 14)).pack(pady=5)

    #The grading system depending on the user's score.
    Grade = "F"
    if Score >= 50:
        Grade = "D"
    if Score >= 60:
        Grade = "C"
    if Score >= 70: 
        Grade = "B"
    if Score >= 80:
        Grade = "A"
    if Score >= 90: 
        Grade = "A+"
    
    

    tk.Label(Root_Window, text="Grade: {}".format(Grade),font=("Segoe Print", 16, "bold"), fg="#FFC0CB").pack(pady=10)
    tk.Button(Root_Window, text="Play Again", command=Display_Menu, width=15, bg="#C8E0F4", font=("Segoe Print", 12)).pack(pady=10)
    tk.Button(Root_Window, text="Exit Game", command=Root_Window.quit, width=15, bg="#FFC0CB", font=("Segoe Print", 12)).pack()

# Once the user finishes answering a question, it'll move on to the next one.
# However if the user is incorrect, the user has a few attempts left to try answering again before moving to the next one.
def Next_Question():
    global Question_Index
    Question_Index += 1
    if Question_Index < Quiz_Length:
        Display_Problem()
    else:
        Display_Results()

def Is_Correct(User_Answer):
    try:
        return int(User_Answer) == Current_Correct_Answer
    except ValueError:
        # User entered non-numeric input
        return False

# After the user submits their answer, it'll use an attempt.
# If the user is correct, it'll add points.
def Submit_Answer():
    global Score, Attempts_Used

    User_Answer = Answer_Entry.get().strip()

    if Is_Correct(User_Answer):
        
        Feedback_Label.config(text="That's correct!", fg="green")
        Points_Earned = 10 if Attempts_Used == 1 else 5
        Score += Points_Earned
        Root_Window.after(1000, Next_Question)
    else:
        Attempts_Used += 1
        if Attempts_Used <= 2:
            Feedback_Label.config(text="Oops, try that one again!.", fg="red")
            Answer_Entry.delete(0, tk.END)
        else:
            Feedback_Label.config(text=f"The correct answer was {Current_Correct_Answer}.", fg="red")
            Root_Window.after(1500, Next_Question)

# This is just the display for the questions of the math quiz.
def Display_Problem():
    global Current_Correct_Answer, Attempts_Used
    global Question_Label, Answer_Entry, Feedback_Label

   
    First_Number, Operation, Second_Number = Current_Problem_Set[Question_Index]

   
    if Operation == '-' and First_Number < Second_Number:
        First_Number, Second_Number = Second_Number, First_Number

    
    if Operation == '+':
        Current_Correct_Answer = First_Number + Second_Number
    else:
        Current_Correct_Answer = First_Number - Second_Number
        
    Attempts_Used = 1

    Question_Label.config(text=f"Question {Question_Index + 1}/{Quiz_Length}: What is {First_Number} {Operation} {Second_Number}?", font=("Segoe Print", 14))
    Answer_Entry.delete(0, tk.END)
    Feedback_Label.config(text="")
    Answer_Entry.focus_set()

# This generates the math questions for the quiz, which is using the Random_Int function and (Level) which is the difficulty.
def Generate_Problems(Level):
    global Current_Problem_Set
    Current_Problem_Set = []

   
    Question_Count = 0
    while Question_Count < Quiz_Length:
        Operation = Decide_Operation()
        First_Number = Random_Int(Level)
        Second_Number = Random_Int(Level)
        Current_Problem_Set.append((First_Number, Operation, Second_Number))
        Question_Count += 1

# The actual quiz starts here, where majority of the functions will be called here to begin the quiz.
def Start_Quiz(Level):
    global Difficulty_Level, Question_Index, Score
    
    global Question_Label, Answer_Entry, Feedback_Label 

    Difficulty_Level = Level
    Question_Index = 0
    Score = 0

    Generate_Problems(Level)
    Clear_Window_Widgets()

    tk.Label(Root_Window, text="Maths Quiz", font=("Segoe Print", 16, "bold"), fg="#3366AA").pack(pady=10)

    Question_Label = tk.Label(Root_Window, text="", font=("Segoe Print", 14), bg="#FFF5EE")
    Question_Label.pack(pady=15)

    Answer_Entry = tk.Entry(Root_Window, font=("Segoe Print", 14), justify="center", width=15)
    Answer_Entry.pack(pady=5)

    tk.Button(Root_Window, text="Submit Answer", command=Submit_Answer, width=15, bg="#FFC0CB", fg="white", font=("Segoe Print", 12, "bold")).pack(pady=10)
    Answer_Entry.bind('<Return>', lambda e: Submit_Answer())

    Feedback_Label = tk.Label(Root_Window, text="", font=("Segoe Print", 12))
    Feedback_Label.pack(pady=10)

    Display_Problem()

# The actual display menu for the Math Quiz
def Display_Menu():
    Clear_Window_Widgets()


    tk.Label(Root_Window, text="CHOOSE YOUR DIFFICULTY", font=("Segoe Print", 18, "bold"), fg="#3366AA").pack(fill='x', pady=20)

    
    tk.Button(Root_Window, text="1. Easy", 
              command=lambda level='Easy': Start_Quiz(level), 
              width=20, font=("Segoe Print", 12, "bold"), 
              bg="#C8E0F4", fg="#3366AA").pack(pady=8, padx=4)
    
    
    tk.Button(Root_Window, text="2. Medium", 
              command=lambda level='Medium': Start_Quiz(level),
              width=20, font=("Segoe Print", 12, "bold"), 
              bg="#C8E0F4", fg="#3366AA").pack(pady=8, padx=4)
              
   
    tk.Button(Root_Window, text="3. Hard", 
              command=lambda level='Hard': Start_Quiz(level),
              width=20, font=("Segoe Print", 12, "bold"), 
              bg="#C8E0F4", fg="#3366AA").pack(pady=8, padx=4)

# The main GUI of the app.
Root_Window.title("Maths Quiz")
Root_Window.geometry("400x450")
Root_Window.resizable(False, False)
Root_Window.config(bg="#FFF5EE")

Display_Menu()
Root_Window.mainloop()


