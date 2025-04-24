import tkinter as tk

def add_task():
    task = task_entry.get()
    if task:  # Проверяем, что поле не пустое
        task_listbox1.insert(tk.END, task)
        task_entry.delete(0, tk.END)  # Очищаем поле ввода после добавления

def move_right(listbox_from, listbox_to):
    selected = listbox_from.curselection()
    if selected:
        item = listbox_from.get(selected[0])
        listbox_to.insert(tk.END, item)
        listbox_from.delete(selected[0])

def move_left(listbox_from, listbox_to):
    selected = listbox_from.curselection()
    if selected:
        item = listbox_from.get(selected[0])
        listbox_to.insert(tk.END, item)
        listbox_from.delete(selected[0])

root = tk.Tk()
root.geometry("800x400")  # Уменьшаем размер окна
root.title("Canban")
root.configure(background="grey81")

# Настраиваем веса столбцов для равномерного распределения
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
# Настраиваем вес строки с листбоксами
root.grid_rowconfigure(3, weight=1)

text1 = tk.Label(root, text="Введите задачу:", background="grey81")
text1.grid(row=0, column=1, padx=5, pady=5, sticky="w")

task_entry = tk.Entry(root, width=35, background="grey90")
task_entry.grid(row=1, column=1, padx=5, pady=5)

add_task_button = tk.Button(root, text="Добавить задачу", command=add_task)
add_task_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

# Add labels for each listbox
label1 = tk.Label(root, text="Беклог", background="grey81")
label1.grid(row=2, column=1, padx=5, pady=5)

label2 = tk.Label(root, text="В работе", background="grey81")
label2.grid(row=2, column=2, padx=5, pady=5)

label3 = tk.Label(root, text="Выполенено", background="grey81")
label3.grid(row=2, column=3, padx=5, pady=5)

# Move listboxes down by one row
task_listbox1 = tk.Listbox(root, width=35, height=15, background="grey90")
task_listbox1.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

task_listbox2 = tk.Listbox(root, width=35, height=15, background="grey90")
task_listbox2.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")

task_listbox3 = tk.Listbox(root, width=35, height=15, background="grey90")
task_listbox3.grid(row=3, column=3, padx=5, pady=5, sticky="nsew")

# Добавляем кнопки между списками
# Между первым и вторым списком
btn1_2_right = tk.Button(root, text="→", command=lambda: move_right(task_listbox1, task_listbox2))
btn1_2_right.grid(row=3, column=1, padx=(160,0), pady=(0,30), sticky="e")

btn2_1_left = tk.Button(root, text="←", command=lambda: move_left(task_listbox2, task_listbox1))
btn2_1_left.grid(row=3, column=1, padx=(160,0), pady=(30,0), sticky="e")

# Между вторым и третьим списком
btn2_3_right = tk.Button(root, text="→", command=lambda: move_right(task_listbox2, task_listbox3))
btn2_3_right.grid(row=3, column=2, padx=(160,0), pady=(0,30), sticky="e")

btn3_2_left = tk.Button(root, text="←", command=lambda: move_left(task_listbox3, task_listbox2))
btn3_2_left.grid(row=3, column=2, padx=(160,0), pady=(30,0), sticky="e")

root.mainloop()
