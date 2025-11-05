import tkinter as tk
from tkinter import scrolledtext, messagebox


BG_PRIMARY = '#F0F8FF'
BG_BUTTON = '#B0E0E6'
FG_BUTTON = '#36454F'
BG_ACCENT = '#ADD8E6'
TEXT_BOX_BG = 'white'
FONT_FAMILY = "Arial"

STUDENT_RECORDS = []

#This opens the student marks file.
try:
    with open('studentMarks.txt', 'r') as file:
        data_lines = file.readlines()
    
    if not data_lines:
        messagebox.showerror("Data Error", "studentMarks.txt is empty.")
        

    num_students = int(data_lines[0].strip())
    total_possible_score = 160

    for line in data_lines[1:num_students + 1]:
        parts = line.strip().split(',')
        
        if len(parts) < 6:
            continue

        student_code = int(parts[0])
        student_name = parts[1]
        
        cw_marks = [int(p) for p in parts[2:5]]
        exam_mark = int(parts[5])

        total_cw = sum(cw_marks)
        overall_score = total_cw + exam_mark
        percentage = (overall_score / total_possible_score) * 100
        
        #This calculates the marks in the text list of the student records if their percentage is low or high.
        #It will assign them a grade.
        if percentage >= 70:
            final_grade = 'A'
        elif percentage >= 60:
            final_grade = 'B'
        elif percentage >= 50:
            final_grade = 'C'
        elif percentage >= 40:
            final_grade = 'D'
        else:
            final_grade = 'F'
            
        STUDENT_RECORDS.append({
            'code': student_code,
            'name': student_name,
            'cw': cw_marks,
            'exam': exam_mark,
            'total_cw': total_cw,
            'overall': overall_score,
            'percentage': percentage,
            'grade': final_grade
        })

except FileNotFoundError:
    messagebox.showerror("Oops! File Missing", "Can't find 'studentMarks.txt'. Please check the 'resources/' folder.")
    
except Exception as e:
    messagebox.showerror("Data Formatting Issue", f"There was an error reading the data: {e}")
    

#This is the main GUI of the entire student manager application.
root = tk.Tk()
root.title("Student Manager")
root.config(bg=BG_PRIMARY)
root.resizable(False, False) 

text_area = scrolledtext.ScrolledText(root, width=70, height=20, 
                                     bg=TEXT_BOX_BG, 
                                     fg='#36454F', 
                                     font=(FONT_FAMILY, 10), 
                                     relief=tk.FLAT, bd=5)
text_area.pack(pady=15, padx=15)

text_area.tag_config('summary', foreground='#36454F', font=(FONT_FAMILY, 11, 'bold'))
text_area.tag_config('bold_name', font=(FONT_FAMILY, 10, 'bold'))
text_area.tag_config('highlight_grade', foreground='#00BFFF', font=(FONT_FAMILY, 10, 'bold'))

#This shows all individual student info in the application.
def show_one_student_info(student):
    text_area.insert(tk.END, f"Student Name: {student['name']}\n", 'bold_name')
    text_area.insert(tk.END, f"Student ID: {student['code']}\n")
    text_area.insert(tk.END, f"Coursework Total: {student['total_cw']} / 60\n")
    text_area.insert(tk.END, f"Final Exam Score: {student['exam']} / 100\n")
    text_area.insert(tk.END, f"Overall Percentage: {student['percentage']:.2f}%\n")
    text_area.insert(tk.END, f"Final Grade: {student['grade']}\n", 'highlight_grade')
    text_area.insert(tk.END, "\n" + "~" * 35 + "\n\n")

#This allows the user to view all of the student records in the file.
def handle_view_all():
    text_area.delete(1.0, tk.END)
    if not STUDENT_RECORDS:
        text_area.insert(tk.END, "The record book is empty.\n")
        return

    total_percentage_sum = sum(s['percentage'] for s in STUDENT_RECORDS)
    avg_percentage = total_percentage_sum / len(STUDENT_RECORDS)
    
    for student in STUDENT_RECORDS:
        show_one_student_info(student)
        
    text_area.insert(tk.END, f"\n CLASSROOM SNAPSHOT \n", 'summary')
    text_area.insert(tk.END, f"Total Students Enrolled: {len(STUDENT_RECORDS)}\n")
    text_area.insert(tk.END, f"The Class Average is: {avg_percentage:.2f}%\n")

#This allows the user to view a student's information individually using the Student ID.
def handle_view_individual():
    text_area.delete(1.0, tk.END)
    code_input = entry_code.get().strip()
    
    if not code_input:
        text_area.insert(tk.END, "Please type a student ID number into the box first!\n")
        return
        
    try:
        student_id = int(code_input)
        
        student = next((s for s in STUDENT_RECORDS if s['code'] == student_id), None)
        
        if student:
            text_area.insert(tk.END, f"--- LOOKING UP ID: {student_id} ---\n", 'summary')
            show_one_student_info(student)
        else:
            text_area.insert(tk.END, f"Sorry, student ID {student_id} was not found in the records.\n")
            
    except ValueError:
        text_area.insert(tk.END, "That doesn't look like a valid ID number.\n")

#This focuses on the user input where it'll allow them to see which one's the highest and lowest.
def handle_extrema(mode):
    text_area.delete(1.0, tk.END)
    
    if not STUDENT_RECORDS:
        text_area.insert(tk.END, "Can't find scores; no student records loaded.\n")
        return

    if mode == 'highest':
        best_student = max(STUDENT_RECORDS, key=lambda s: s['overall'])
        text_area.insert(tk.END, " TOP PERFORMER AWARD! \n", 'summary')
    else:
        best_student = min(STUDENT_RECORDS, key=lambda s: s['overall'])
        text_area.insert(tk.END, " NEEDS IMPROVEMENT ALERT! \n", 'summary')
        
    show_one_student_info(best_student)

input_frame = tk.Frame(root, bg=BG_PRIMARY)
input_frame.pack(pady=5)

tk.Label(input_frame, text="Enter Student ID:", bg=BG_PRIMARY, fg=FG_BUTTON, font=(FONT_FAMILY, 10, 'bold')).pack(side=tk.LEFT, padx=5)
entry_code = tk.Entry(input_frame, width=15, bd=2, relief=tk.GROOVE)
entry_code.pack(side=tk.LEFT, padx=5)

btn_frame = tk.Frame(root, bg=BG_PRIMARY)
btn_frame.pack(pady=10)

#These are just the button designs for the functions.
button_specs = [
    ("View ALL Student Records", handle_view_all),
    ("Look Up Individual Record", handle_view_individual),
    ("Who Scored the Highest?", lambda: handle_extrema('highest')),
    ("Who Scored the Lowest?", lambda: handle_extrema('lowest')),
    ("Quit Program", root.quit)
]

#And this code is the actual coding design for it.
for text, command in button_specs:
    btn = tk.Button(btn_frame, 
                    text=text, 
                    command=command,
                    bg=BG_BUTTON, 
                    fg=FG_BUTTON,
                    activebackground=BG_ACCENT, 
                    activeforeground=FG_BUTTON,
                    width=30,
                    height=1,
                    bd=3,
                    relief=tk.RAISED, 
                    font=(FONT_FAMILY, 10, 'bold')
    )
    btn.pack(pady=4)

root.after(100, handle_view_all) 

root.mainloop()
