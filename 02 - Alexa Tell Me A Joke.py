import tkinter as tk
import random 

#This opens the randomJokes.txt file for the code to add the jokes.
try:
    with open("randomJokes.txt" , "r", encoding="utf-8") as F_Handle:
        Alexa_Jokes = F_Handle.readlines()
except FileNotFoundError:
    Alexa_Jokes = []

#This is for the list of jokes that is found in the file, and formats it in a way that -
#It'll only show the full text (Punchline) if the user clicks the Punchline button.
Alexa_Joke_List = []
for Joke_Line in Alexa_Jokes:
    Joke_Line = Joke_Line.strip()
    if '?' in Joke_Line:
        Parts = Joke_Line.split('?', 1)
        Setup = Parts[0].strip()
        Punchline = Parts[1].strip()
        Alexa_Joke_List.append((Setup, Punchline))


Root_Window = tk.Tk()
Root_Window.title("Alexa Tell Me A Joke")
Root_Window.geometry("600x600")
Root_Window.config(bg="#FFF5EE")

Current_Alexa_Joke = None

Label_Instruction = tk.Label(Root_Window, 
                             text="Type 'Alexa tell me a Joke' to get a joke:",
                             font=("Segoe Print", 12),
                             bg="#FFF5EE", 
                             fg="#3366AA")
Label_Instruction.pack(pady=10)

Entry_Command = tk.Entry(Root_Window, font=("Segoe Print", 12), width=40)
Entry_Command.pack(pady=5)

Label_Setup = tk.Label(Root_Window, 
                        text="", 
                        wraplength=400, 
                        font=("Segoe Print", 14, "bold"),
                        bg="#FFF5EE",
                        fg="#3366AA")
Label_Setup.pack(pady=15, padx=10)

Label_Punchline = tk.Label(Root_Window, 
                           text="", 
                           wraplength=400, 
                           font=("Segoe Print", 14, "italic"),
                           bg="#FFF5EE",
                           fg="#FFC0CB")
Label_Punchline.pack(pady=10, padx=10)

#This is where Alexa will tell the user a joke if the user types "Alexa tell me a joke"
def Tell_Alexa_Joke():
    global Current_Alexa_Joke
    Command_Text = Entry_Command.get().strip().lower()
    if Command_Text == "alexa tell me a joke":
        if Alexa_Joke_List:
            Current_Alexa_Joke = random.choice(Alexa_Joke_List) #Alexa will choose a random joke for the user.
            Setup_Text, _ = Current_Alexa_Joke
            Label_Setup.config(text=Setup_Text + "?")
            Label_Punchline.config(text="")
            Button_Punchline.pack()
            Entry_Command.delete(0, tk.END)
        else: 
            Label_Setup.config(text="No Alexa jokes available (File Load Error).")
            Label_Punchline.config(text="")
            Button_Punchline.pack_forget()
            
    else: #If the user inputs something incorrectly, it will loop and tell the user to try again.
        Label_Setup.config(text="Invalid command. Try 'Alexa tell me a Joke'.")
        Label_Punchline.config(text="")
        Button_Punchline.pack_forget()

#This will then display the punchline when the user clicks the Punchline Button.
def Show_Alexa_Punchline():
    if Current_Alexa_Joke:
        _, Punchline_Text = Current_Alexa_Joke
        Label_Punchline.config(text=Punchline_Text)
        Button_Punchline.pack_forget()

Button_Tell = tk.Button(Root_Window, 
                        text="Tell Joke", 
                        command=Tell_Alexa_Joke,
                        font=("Segoe Print", 12, "bold"),
                        bg="#C8E0F4", 
                        fg="#3366AA")
Button_Tell.pack(pady=5)

Button_Punchline = tk.Button(Root_Window, 
                             text="Show Punchline", 
                             command=Show_Alexa_Punchline,
                             font=("Segoe Print", 12, "bold"),
                             bg="#FFC0CB", 
                             fg="white")

Button_Quit = tk.Button(Root_Window, text="Quit", command=Root_Window.quit, fg="red", font=("Segoe Print", 12))
Button_Quit.pack(pady=10)

Root_Window.mainloop()
