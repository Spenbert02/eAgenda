import tkinter
import datetime
import calendar
from tkinter import messagebox

#design:
root = tkinter.Tk()
root.title("eAgenda")
root.geometry("1430x710")
root.resizable(False,False)
padx = 0
pady = 0
#top canvas:
top_canvas = tkinter.Canvas(root, width=1425, height=75, bg="whitesmoke")
top_canvas.grid(row=0, column=0, columnspan=3, padx=padx, pady=pady)
#create assignment canvas:
middle_left_canvas = tkinter.Canvas(root, width=300, height=260, bg="lightsteelblue")
middle_left_canvas.grid(row=1, column=0, padx=padx, pady=pady, sticky="n"+"s"+"e"+"w")
#create exam canvas:
bottom_left_canvas = tkinter.Canvas(root, width=300, height=260, bg="lightsteelblue")
bottom_left_canvas.grid(row=2, column=0, padx=padx, pady=pady, sticky="n"+"s"+"e"+"w")
#agenda list canvas:
bottom_right_canvas = tkinter.Canvas(root, width=620, height=525, bg="whitesmoke", bd=0)
bottom_right_canvas.grid(row=1, column=1, rowspan=2, padx=padx, pady=pady, sticky="n"+"s"+"e"+"w")
#Schedule:
#schedule_image = tkinter.PhotoImage(file="<filepath>")
# label = tkinter.Label(root, image=schedule_image)
# label.grid(row=1, column=2, rowspan=2, sticky="w"+"e",pady=pady,padx=padx)

#constant top_canvas text:
num_sections = 6
class_codes = ["Class Code", "Class Code", "Class Code", "Class Code", "Class Code", "Class Code"]
classes = ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6"]
class_colors = ["skyblue", "palegoldenrod", "orange", "darkolivegreen1", "lightgoldenrod3", "gray18"]
top_canvas.create_text(75,37.5, font="Fantasy 20", fill="black", text="Classes:")
for x in range(0, num_sections):
    top_canvas.create_rectangle((190+((1275/num_sections)*x)),32.5, (200+((1275/num_sections)*x)),42.5, outline=class_colors[x], fill=class_colors[x])
    top_canvas.create_text((205+((1275/num_sections)*x)),42, anchor="sw", font="fantasy 12", fill="black", text=classes[x]) # Classes
    top_canvas.create_text((205+((1275/num_sections)*x)),41, anchor="nw", font="fantasy 12", fill="black", text=class_codes[x]) # Class codes







# generates list of next seven dates:
today = str(datetime.date.today()).split("-") #today is a list with ["year", "month", "day"]
for x in range(0,3):
    today[x] = int(today[x])

days_in_agenda = 28 #can be adjusted, set to show next 4 weeks. only works for int <= rest of current month and next month

month_lengths = [[1,31],[2,28],[3,31],[4,30],[5,31],[6,30],[7,31],[8,31],[9,30],[10,31],[11,30],[12,31]]
int_dates_lst = [] #after conditional below, int_dates_lst contains a list of 28 dates which are lists in the same format as "today"
days_left_in_month = month_lengths[today[1]-1][1] - today[2] + 1
if days_left_in_month >= days_in_agenda:
    for x in range(0,days_in_agenda):
        int_dates_lst.append([today[0], today[1], today[2]+x])
else:
    for x in range(0,days_left_in_month):
        int_dates_lst.append([today[0], today[1], today[2]+x])
    for x in range(0,(days_in_agenda-days_left_in_month)):
        int_dates_lst.append([today[0], today[1]+1, x+1])

str_dates_lst = []
for x in range (0, days_in_agenda):
    str_dates_lst.append(str(int_dates_lst[x][0]) + "-"+ str(int_dates_lst[x][1]) + "-" + str(int_dates_lst[x][2]))

display_dates = []
for date in int_dates_lst:
    display_dates.append(calendar.weekday(date[0], date[1], date[2]))
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for x in range(0, len(display_dates)):
    display_dates[x] = str(weekdays[display_dates[x]]) + ", " + str(int_dates_lst[x][1]) + "/" + str(int_dates_lst[x][2])
#display_dates now contains list of dates in display format in same order as int and str dates lists



#displaying latest date to enter assignment:
latest_day = str_dates_lst[-1]
top_canvas.create_text(10,5, anchor="nw", font="fantasy 12", text=("*Latest day to enter assignment/exam: " + latest_day))

#function that adds a single assignment/exam to listbox in bottom_right_canvas
list_box = tkinter.Listbox(bottom_right_canvas, bg="whitesmoke", width=49, height=22, font="Fantasy 16")
list_box.pack(pady=20)
    #establishing list box ^^^^^
def add_single_object_listbox(assign_or_exam, name, _class):    #each var is str
    list_box.insert("end", "          " + _class + " | " + name + "                    " + "(" + assign_or_exam + ")")
    list_box.itemconfig("end", bg=class_colors[class_codes.index(_class)])
    if _class == "MISC":
        list_box.itemconfig("end", fg = "white")

#function that adds date to listbox
def add_date_listbox(_date):    # _date is list with int values in same format as "today"
    global str_dates_lst
    global display_dates
    list_box.insert("end", display_dates[str_dates_lst.index(_date)]) #can be adjusted to show year

def add_empty():
    list_box.insert("end", "          Nothing Due")
    list_box.itemconfig("end", bg="white")


#function which displays current assignments and exams | needs to be called by add_assignment and add_exam | needs to clear listbox before adding everything
def display_all():
    list_box.delete(0,"end")
    global current_agenda_dict
    global str_dates_lst
    for date in str_dates_lst:
        add_date_listbox(date)
        if date in current_agenda_dict:
            for object in current_agenda_dict[date]:
                add_single_object_listbox(object[0], object[1], object[2])
        else:
            add_empty()



# general function to read all current assignmets/exams and format into assignments list
def get_assignments_exams():
    with open("eAgenda_data.txt", "r") as md:
        assignments = md.readlines()
    #Removing empty lines:    (below)
    lines_removed_counter = 0
    for x in range(0, len(assignments)):
        if len(assignments[x-lines_removed_counter]) == 1 or assignments[x-lines_removed_counter][0] == "#":
            del assignments[x-lines_removed_counter]
            lines_removed_counter += 1


    for x in range(0, len(assignments)):
        assignments[x] = assignments[x][:-1]
    for x in range(0, len(assignments)):
        if ";" in assignments[x]:
            assignments[x] = assignments[x].split(";")
        elif assignments[x][0] != "2":
            assignments[x] = [assignments[x]]
    for x in range(0, len(assignments)):
        if (x%2) == 1:
            for y in range(0, len(assignments[x])):
                assignments[x][y] = assignments[x][y].split(",")
    assignments_dict = {}
    for x in range(0, len(assignments)):
        if (x%2) == 0:
            assignments_dict[assignments[x]] = assignments[x+1]
    return assignments_dict



#function to rewrite updated file
def update_file():
    global current_agenda_dict
    with open("eAgenda_data.txt", "w") as updated_file:
        for date in current_agenda_dict:
            updated_file.write(date + "\n")
            assignments_for_date = []
            for object in current_agenda_dict[date]:
                assignment_line = object[0] + "," + object[1] + "," + object[2] + "," + object[3]
                assignments_for_date.append(assignment_line)
            assignments_for_date_str = ""
            for x in range(0, len(assignments_for_date)):
                assignments_for_date_str = assignments_for_date_str + assignments_for_date[x] + ";"
            assignments_for_date_str = assignments_for_date_str[:-1]
            updated_file.write(assignments_for_date_str + "\n")




#function to add assignment
def add_assignment(name, _class, due_date): #could add safe guards to different capitalization entries
    global current_agenda_dict
    if due_date in current_agenda_dict:
        current_agenda_dict[due_date].append(["Assignment", name, _class, due_date])
    else:
        current_agenda_dict[due_date] = [["Assignment", name, _class, due_date]]
    update_file()
    display_all()

def add_assignment_button_command():
    assignment_name = assignment_name_tkStringVar.get()
    assignment_class = assignment_class_tkStringVar.get()
    assignment_due_date = str_dates_lst[display_dates.index(assignment_due_date_tkStringVar.get())]
    add_assignment(assignment_name, assignment_class, assignment_due_date)






#function to add exam
def add_exam(name, _class, due_date): #could add safe guards to different capitalization entries
    global current_agenda_dict
    if due_date in current_agenda_dict:
        current_agenda_dict[due_date].append(["Exam", name, _class, due_date])
    else:
        current_agenda_dict[due_date] = [["Exam", name, _class, due_date]]
    update_file()
    display_all()

def add_exam_button_command():
    exam_name = exam_name_tkStringVar.get()
    exam_class = exam_class_tkStringVar.get()
    exam_due_date = str_dates_lst[display_dates.index(exam_due_date_tkStringVar.get())]
    add_exam(exam_name, exam_class, exam_due_date)





#function to complete (remove) exam/assignment
def delete_assign_exam(list_box_index):
    global current_agenda_dict
    list_box_string = list_box.get(list_box_index)
    assign_char_lst = []
    for char in list_box_string:
        if char == "|":
            current_index = list_box_string.index("|") + 2
            while list_box_string[current_index] != "(":
                assign_char_lst.append(list_box_string[current_index])
                current_index += 1

            assignment_class_str = list_box_string[(list_box_string.index("|")-13) : list_box_string.index("|")-1]
            while assignment_class_str[0] == " ":
                assignment_class_str = assignment_class_str[1:] #assignment_class_str is now a string of the class code

    assignment_name_str = ""
    for char in assign_char_lst:
        assignment_name_str += char #assignment_name_str now is a string of the assignment name, regardless of length or contents
    while assignment_name_str[-1] == " ":
        assignment_name_str = assignment_name_str[:-1]

    dates_in_agenda_rev_order = []
    for x in range(0, list_box_index+1):
        if list_box.get(list_box_index-x)[0] != " ":
            dates_in_agenda_rev_order.append(str_dates_lst[display_dates.index(list_box.get(list_box_index-x))])
    assignment_date_str = dates_in_agenda_rev_order[0] #assignment_date_str is now  string of the assignments date "yyyy-(m)m-(d)d"

    for key in current_agenda_dict:
        if assignment_date_str == key:
            for assignment in current_agenda_dict[key]:
                    if assignment[1] == assignment_name_str and assignment[2] == assignment_class_str:
                        date = key
                        assignment_index = current_agenda_dict[key].index(assignment)
    if len(current_agenda_dict[date]) == 1:
        del current_agenda_dict[date]
    elif len(current_agenda_dict[date]) > 1:
        del current_agenda_dict[date][assignment_index]

    update_file()
    display_all()

def delete_assign_exam_button_command():
    _list_box_index_tup = list_box.curselection()
    _list_box_str = list_box.get(_list_box_index_tup[0])
    if _list_box_str[0] != " ":
        tkinter.messagebox.showerror(title="Error", message="Cannot delete dates.", icon="error")

    elif _list_box_str[10:] == "Nothing Due":
        tkinter.messagebox.showerror(title="Error", message="Cannot delete assignment placeholders.", icon="error")
    else:
        delete_assign_exam(_list_box_index_tup[0])

#First program read through:
current_agenda_dict = get_assignments_exams()   #current_agenda_dict now contains dict where dict["yyyy-(m)m-(d)d"] : [["assign/exam", "name", "class", date in str format, *repeated for every assignment]
display_all()




#buttons and dropdown menus (and text display for "add" widgets):
middle_left_canvas.create_text(200, 15, anchor="n", font="fantasy 18 bold", text="Add Assignment*")
#
assignment_name_tkStringVar = tkinter.StringVar(root)
assignment_name_entry = tkinter.Entry(middle_left_canvas, width=30, textvariable=assignment_name_tkStringVar)
assignment_name_entry.pack(pady=(45,5))
assignment_name_entry.insert(0, "assignment name")
#
assignment_class_tkStringVar = tkinter.StringVar(root)
assignment_class_tkStringVar.set(class_codes[0])
assignment_class_dropdown = tkinter.OptionMenu(middle_left_canvas, assignment_class_tkStringVar, *class_codes)
assignment_class_dropdown.pack(pady=5)

#
assignment_due_date_tkStringVar = tkinter.StringVar(root)
assignment_due_date_tkStringVar.set(display_dates[0])
assignment_due_date_dropdown = tkinter.OptionMenu(middle_left_canvas, assignment_due_date_tkStringVar, *display_dates)
assignment_due_date_dropdown.pack(pady=5)
#
assignment_creation_button = tkinter.Button(middle_left_canvas, text="Add Assignment", command=add_assignment_button_command)
assignment_creation_button.pack(pady=25)

#----------------------

bottom_left_canvas.create_text(200, 15, anchor="n", font="fantasy 18 bold", text="Add Exam*")
#
exam_name_tkStringVar = tkinter.StringVar(root)
exam_name_entry = tkinter.Entry(bottom_left_canvas, width=30, textvariable=exam_name_tkStringVar)
exam_name_entry.pack(pady=(45,5))
exam_name_entry.insert(0, "exam name")
#
exam_class_tkStringVar = tkinter.StringVar(root)
exam_class_tkStringVar.set(class_codes[0])
exam_class_dropdown = tkinter.OptionMenu(bottom_left_canvas, exam_class_tkStringVar, *class_codes)
exam_class_dropdown.pack(pady=5)
#
exam_due_date_tkStringVar = tkinter.StringVar(root)
exam_due_date_tkStringVar.set(display_dates[0])
exam_due_date_dropdown = tkinter.OptionMenu(bottom_left_canvas, exam_due_date_tkStringVar, *display_dates)
exam_due_date_dropdown.pack(pady=5)
#
exam_creation_button = tkinter.Button(bottom_left_canvas, text="Add Exam", command=add_exam_button_command)
exam_creation_button.pack(pady=25)

#--------------------------

#button to delete assignment
assign_exam_delete_button = tkinter.Button(bottom_right_canvas, text="Remove Assignment/Exam", command=delete_assign_exam_button_command)
assign_exam_delete_button.pack(pady=5)



root.mainloop()
