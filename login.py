import tkinter as tk
from tkinter import messagebox
from users import UserManager
from gui import KanbanApp

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x200")
        self.root.title("Вход в систему")
        self.root.configure(background="grey81")
        
        self.user_manager = UserManager()
        
        self.create_widgets()

    def create_widgets(self):
        """Создает элементы интерфейса окна входа"""
        # Метка и поле для ввода логина
        self.label = tk.Label(self.root, text="Введите логин:", background="grey81")
        self.label.pack(pady=10)
        
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)
        
        # Кнопки входа и регистрации
        self.login_button = tk.Button(
            self.root, 
            text="Войти", 
            command=self.login
        )
        self.login_button.pack(pady=5)
        
        self.register_button = tk.Button(
            self.root, 
            text="Зарегистрироваться", 
            command=self.show_register_window
        )
        self.register_button.pack(pady=5)

    def login(self):
        """Обработка входа пользователя"""
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Ошибка", "Введите логин")
            return
            
        success, role = self.user_manager.authenticate_user(username)
        if success:
            self.root.destroy()
            app = KanbanApp(role, username)
            app.run()
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def show_register_window(self):
        """Показывает окно регистрации"""
        register_window = tk.Toplevel(self.root)
        register_window.geometry("300x200")
        register_window.title("Регистрация")
        register_window.configure(background="grey81")
        
        # Метка и поле для ввода логина
        label = tk.Label(register_window, text="Введите новый логин:", background="grey81")
        label.pack(pady=10)
        
        username_entry = tk.Entry(register_window, width=30)
        username_entry.pack(pady=5)
        
        # Чекбокс для выбора роли администратора
        is_admin_var = tk.BooleanVar()
        admin_check = tk.Checkbutton(
            register_window, 
            text="Регистрация как администратор", 
            variable=is_admin_var,
            background="grey81"
        )
        admin_check.pack(pady=5)
        
        # Кнопка регистрации
        register_button = tk.Button(
            register_window,
            text="Зарегистрироваться",
            command=lambda: self.register(username_entry.get(), is_admin_var.get(), register_window)
        )
        register_button.pack(pady=5)

    def register(self, username, is_admin, window):
        """Обработка регистрации нового пользователя"""
        if not username:
            messagebox.showerror("Ошибка", "Введите логин")
            return
            
        success, message = self.user_manager.register_user(username, is_admin)
        if success:
            messagebox.showinfo("Успех", message)
            window.destroy()
        else:
            messagebox.showerror("Ошибка", message)

    def run(self):
        """Запускает окно входа"""
        self.root.mainloop()

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.run() 