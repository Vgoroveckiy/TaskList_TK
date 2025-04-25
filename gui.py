import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from datetime import datetime
from services import save_data, load_data, add_task, move_right, move_left, delete_task, get_task_info, edit_task, get_users_list

class KanbanApp:
    def __init__(self, user_role, username):
        self.user_role = user_role
        self.username = username
        self.root = tk.Tk()
        self.root.geometry("1200x600")  # Увеличиваем размер окна
        self.root.title(f"Canban - {user_role} ({username})")
        self.root.configure(background="grey81")

        # Получаем список пользователей
        self.users_list = get_users_list()

        # Настраиваем сетку
        self.setup_grid()
        
        # Создаем элементы интерфейса
        self.create_widgets()
        
        # Загружаем данные
        self.load_initial_data()
        
        # Настраиваем обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_grid(self):
        """Настраивает веса столбцов и строк для равномерного распределения"""
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_columnconfigure(4, weight=2)  # Увеличиваем вес для колонки с деталями
        self.root.grid_rowconfigure(3, weight=1)

    def create_widgets(self):
        """Создает все элементы интерфейса"""
        # Поле ввода и кнопка добавления (только для админов)
        if self.user_role == "admin":
            self.create_input_section()
        
        # Заголовки списков
        self.create_list_headers()
        
        # Списки задач
        self.create_listboxes()
        
        # Кнопки перемещения
        self.create_move_buttons()
        
        # Окно свойств задачи
        self.create_task_properties()

    def create_input_section(self):
        """Создает секцию ввода новой задачи"""
        self.text1 = tk.Label(self.root, text="Создать новую задачу:", background="grey81")
        self.text1.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.add_task_button = tk.Button(
            self.root, 
            text="Добавить задачу", 
            command=self.show_create_window
        )
        self.add_task_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def create_list_headers(self):
        """Создает заголовки для списков"""
        self.label1 = tk.Label(self.root, text="Беклог", background="grey81")
        self.label1.grid(row=2, column=1, padx=5, pady=5)

        self.label2 = tk.Label(self.root, text="В работе", background="grey81")
        self.label2.grid(row=2, column=2, padx=5, pady=5)

        self.label3 = tk.Label(self.root, text="Выполнено", background="grey81")
        self.label3.grid(row=2, column=3, padx=5, pady=5)

        self.label4 = tk.Label(self.root, text="Свойства задачи", background="grey81")
        self.label4.grid(row=2, column=4, padx=5, pady=5)

    def create_listboxes(self):
        """Создает списки задач"""
        self.task_listbox1 = tk.Listbox(self.root, width=35, height=15, background="grey90")
        self.task_listbox1.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        self.task_listbox1.bind("<<ListboxSelect>>", self.update_task_properties)
        self.task_listbox1.task_data = []  # Инициализируем пустой список для метаданных

        self.task_listbox2 = tk.Listbox(self.root, width=35, height=15, background="grey90")
        self.task_listbox2.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")
        self.task_listbox2.bind("<<ListboxSelect>>", self.update_task_properties)
        self.task_listbox2.task_data = []  # Инициализируем пустой список для метаданных

        self.task_listbox3 = tk.Listbox(self.root, width=35, height=15, background="grey90")
        self.task_listbox3.grid(row=3, column=3, padx=5, pady=5, sticky="nsew")
        self.task_listbox3.bind("<<ListboxSelect>>", self.update_task_properties)
        self.task_listbox3.task_data = []  # Инициализируем пустой список для метаданных

    def create_move_buttons(self):
        """Создает кнопки перемещения между списками"""
        # Между первым и вторым списком
        self.btn1_2_right = tk.Button(
            self.root, 
            text="→", 
            command=lambda: move_right(self.task_listbox1, self.task_listbox2, self.save_current_state, self.username)
        )
        self.btn1_2_right.grid(row=3, column=1, padx=(160, 0), pady=(0, 30), sticky="e")

        self.btn2_1_left = tk.Button(
            self.root, 
            text="←", 
            command=lambda: move_left(self.task_listbox2, self.task_listbox1, self.save_current_state, self.username)
        )
        self.btn2_1_left.grid(row=3, column=1, padx=(160, 0), pady=(30, 0), sticky="e")

        # Между вторым и третьим списком
        self.btn2_3_right = tk.Button(
            self.root, 
            text="→", 
            command=lambda: move_right(self.task_listbox2, self.task_listbox3, self.save_current_state, self.username)
        )
        self.btn2_3_right.grid(row=3, column=2, padx=(160, 0), pady=(0, 30), sticky="e")

        self.btn3_2_left = tk.Button(
            self.root, 
            text="←", 
            command=lambda: move_left(self.task_listbox3, self.task_listbox2, self.save_current_state, self.username)
        )
        self.btn3_2_left.grid(row=3, column=2, padx=(160, 0), pady=(30, 0), sticky="e")

        # Кнопки для админов
        if self.user_role == "admin":
            self.btn_edit_task = tk.Button(
                self.root,
                text="Редактировать задачу",
                command=self.show_edit_window
            )
            self.btn_edit_task.grid(row=1, column=3, padx=5, pady=5, sticky="e")

            self.btn_delete_task = tk.Button(
                self.root, 
                text="Удалить задачу", 
                command=self.confirm_delete
            )
            self.btn_delete_task.grid(row=1, column=4, padx=5, pady=5, sticky="e")

    def create_task_properties(self):
        """Создает окно для отображения свойств задачи"""
        self.task_properties = tk.Text(self.root, width=35, height=15, background="grey90", state="disabled")
        self.task_properties.grid(row=3, column=4, padx=5, pady=5, sticky="nsew")

    def show_create_window(self):
        """Показывает окно создания новой задачи"""
        create_window = tk.Toplevel(self.root)
        create_window.title("Создание задачи")
        create_window.geometry("400x500")
        create_window.configure(background="grey81")
        
        # Создаем и размещаем поля ввода
        fields = [
            ("Название задачи:", "title"),
            ("Описание:", "description"),
            ("Приоритет:", "priority"),
            ("Ответственный:", "assignee"),
            ("Срок выполнения:", "deadline")
        ]
        
        entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            label = tk.Label(create_window, text=label_text, background="grey81")
            label.grid(row=i*2, column=0, padx=5, pady=5, sticky="w")
            
            if field_name == "priority":
                entry = ttk.Combobox(create_window, values=["Низкий", "Средний", "Высокий"])
                entry.grid(row=i*2+1, column=0, padx=5, pady=5, sticky="ew")
            elif field_name == "assignee":
                entry = ttk.Combobox(create_window, values=self.users_list)
                entry.grid(row=i*2+1, column=0, padx=5, pady=5, sticky="ew")
            elif field_name == "deadline":
                frame = tk.Frame(create_window, background="grey81")
                frame.grid(row=i*2+1, column=0, padx=5, pady=5, sticky="ew")
                
                entry = tk.Entry(frame)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                btn_calendar = ttk.Button(
                    frame,
                    text="📅",
                    command=lambda e=entry: self.show_date_picker(e)
                )
                btn_calendar.pack(side=tk.LEFT, padx=(5, 0))
            else:
                entry = tk.Entry(create_window)
                entry.grid(row=i*2+1, column=0, padx=5, pady=5, sticky="ew")
            
            entries[field_name] = entry
        
        create_window.grid_columnconfigure(0, weight=1)
        
        # Кнопка сохранения
        save_button = ttk.Button(
            create_window,
            text="Создать задачу",
            command=lambda: self.save_new_task(entries, create_window)
        )
        save_button.grid(row=len(fields)*2+1, column=0, padx=5, pady=20)

    def save_new_task(self, entries, window):
        """Сохраняет новую задачу"""
        task_data = {
            "title": entries["title"].get(),
            "description": entries["description"].get(),
            "priority": entries["priority"].get(),
            "assignee": entries["assignee"].get(),
            "deadline": entries["deadline"].get()
        }
        
        if task_data["title"]:
            add_task(None, self.task_listbox1, self.save_current_state, self.username, task_data)
            window.destroy()
        else:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым")

    def show_edit_window(self):
        """Показывает окно редактирования задачи"""
        listbox = self.root.focus_get()
        if not isinstance(listbox, tk.Listbox):
            return
            
        selection = listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        task_data = listbox.task_data[index]
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование задачи")
        edit_window.geometry("400x420")  # Уменьшаем высоту окна
        edit_window.configure(background="grey81")
        edit_window.resizable(False, False)  # Запрещаем изменение размера окна
        
        # Создаем и размещаем поля ввода
        fields = [
            ("Название задачи:", "title"),
            ("Описание:", "description"),
            ("Приоритет:", "priority"),
            ("Ответственный:", "assignee"),
            ("Срок выполнения:", "deadline")
        ]
        
        entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            label = tk.Label(edit_window, text=label_text, background="grey81")
            label.grid(row=i*2, column=0, padx=5, pady=(5,0), sticky="w")
            
            if field_name == "priority":
                entry = ttk.Combobox(edit_window, values=["Низкий", "Средний", "Высокий"])
                entry.grid(row=i*2+1, column=0, padx=5, pady=(0,5), sticky="ew")
            elif field_name == "assignee":
                entry = ttk.Combobox(edit_window, values=self.users_list)
                entry.grid(row=i*2+1, column=0, padx=5, pady=(0,5), sticky="ew")
            elif field_name == "deadline":
                frame = tk.Frame(edit_window, background="grey81")
                frame.grid(row=i*2+1, column=0, padx=5, pady=(0,5), sticky="ew")
                
                entry = tk.Entry(frame)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                btn_calendar = ttk.Button(
                    frame,
                    text="📅",
                    command=lambda e=entry: self.show_date_picker(e)
                )
                btn_calendar.pack(side=tk.LEFT, padx=(5, 0))
            else:
                entry = tk.Entry(edit_window)
                if field_name == "description":
                    entry = tk.Text(edit_window, height=4)  # Увеличиваем поле описания
                entry.grid(row=i*2+1, column=0, padx=5, pady=(0,5), sticky="ew")
            
            if isinstance(entry, tk.Text):
                entry.insert("1.0", task_data.get(field_name, ""))
            else:
                entry.insert(0, task_data.get(field_name, ""))
            entries[field_name] = entry
        
        edit_window.grid_columnconfigure(0, weight=1)
        
        # Кнопка сохранения
        save_button = ttk.Button(
            edit_window,
            text="Сохранить изменения",
            command=lambda: self.save_edit(listbox, index, entries, edit_window)
        )
        save_button.grid(row=len(fields)*2+1, column=0, padx=5, pady=10)  # Уменьшаем отступ снизу

    def save_edit(self, listbox, index, entries, window):
        """Сохраняет отредактированную задачу"""
        new_data = {
            "title": entries["title"].get(),
            "description": entries["description"].get("1.0", tk.END).strip() if isinstance(entries["description"], tk.Text) else entries["description"].get(),
            "priority": entries["priority"].get(),
            "assignee": entries["assignee"].get(),
            "deadline": entries["deadline"].get()
        }
        
        if new_data["title"]:
            edit_task(listbox, index, new_data, self.save_current_state, self.username)
            window.destroy()
            # Создаем событие с правильным виджетом
            event = type('Event', (), {'widget': listbox})()
            self.update_task_properties(event)
        else:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым")

    def update_task_properties(self, event):
        """Обновляет информацию о выбранной задаче"""
        listbox = event.widget
        task_info = get_task_info(listbox)
        
        self.task_properties.config(state="normal")
        self.task_properties.delete(1.0, tk.END)
        
        if task_info:
            self.task_properties.insert(tk.END, f"Название: {task_info.get('title', '')}\n\n")
            self.task_properties.insert(tk.END, f"Описание:\n{task_info.get('description', '')}\n\n")
            self.task_properties.insert(tk.END, f"Приоритет: {task_info.get('priority', '')}\n\n")
            self.task_properties.insert(tk.END, f"Ответственный: {task_info.get('assignee', '')}\n\n")
            self.task_properties.insert(tk.END, f"Срок выполнения: {task_info.get('deadline', '')}\n\n")
            self.task_properties.insert(tk.END, f"Изменено: {task_info.get('modified', '')}\n\n")
            self.task_properties.insert(tk.END, f"Изменено пользователем: {task_info.get('modified_by', '')}")
        
        self.task_properties.config(state="disabled")

    def save_current_state(self):
        """Сохраняет текущее состояние списков"""
        save_data(self.task_listbox1, self.task_listbox2, self.task_listbox3)

    def load_initial_data(self):
        """Загружает начальные данные из файла"""
        load_data(self.task_listbox1, self.task_listbox2, self.task_listbox3)

    def on_closing(self):
        """Обработчик закрытия окна"""
        self.save_current_state()
        self.root.destroy()

    def confirm_delete(self):
        """Показывает диалог подтверждения перед удалением задачи"""
        listbox = self.root.focus_get()
        if not isinstance(listbox, tk.Listbox):
            return
            
        selection = listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        task_text = listbox.get(index)
        
        if messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить задачу:\n\n'{task_text}'?"
        ):
            delete_task(listbox, self.save_current_state)

    def show_date_picker(self, entry):
        """Показывает календарь для выбора даты"""
        top = tk.Toplevel(self.root)
        top.title("Выберите дату")
        
        # Если есть существующая дата, используем её
        try:
            if entry.get():
                date_obj = datetime.strptime(entry.get(), '%d.%m.%Y')
                initial_date = date_obj
            else:
                initial_date = datetime.now()
        except ValueError:
            initial_date = datetime.now()
        
        # Создаем календарь
        cal = Calendar(top, 
                      selectmode='day',
                      year=initial_date.year,
                      month=initial_date.month,
                      day=initial_date.day,
                      locale='ru_RU',
                      background="grey81",
                      foreground="black",
                      selectbackground="royal blue",
                      selectforeground="white",
                      normalbackground="white",
                      normalforeground="black",
                      weekendbackground="white",
                      weekendforeground="black",
                      date_pattern='dd.mm.yyyy')  # Устанавливаем нужный формат даты
        cal.pack(padx=10, pady=10)
        
        def set_date():
            date = cal.get_date()  # Теперь возвращается в формате dd.mm.yyyy
            entry.delete(0, tk.END)
            entry.insert(0, date)
            top.destroy()
        
        # Кнопка подтверждения
        ttk.Button(top, text="OK", command=set_date).pack(pady=10)

    def run(self):
        """Запускает приложение"""
        self.root.mainloop()

if __name__ == "__main__":
    app = KanbanApp("admin", "admin")
    app.run() 