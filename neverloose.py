import tkinter as tk
from tkinter import ttk, font
import webbrowser

class ConfigWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("NEWERLOSE")
        self.root.geometry("900x650")
        self.root.configure(bg="#0a0a0a")
        self.root.minsize(800, 600)
        
        self.base_font = ("Segoe UI", 10)
        self.title_font = ("Segoe UI", 12, "bold")
        
        self.all_sections = []
        self.all_checkboxes = []
        
        self.create_warning_modal()
        
        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TFrame', background="#111111")
        self.style.configure('TButton', background="#000000", foreground="#e1e1e1", 
                           font=self.base_font, borderwidth=1)
        self.style.map('TButton',
                      background=[('active', '#00a8ff'), ('disabled', '#2a2a2a')],
                      foreground=[('active', 'white')])
        
        self.style.configure('TCheckbutton', font=self.base_font, 
                           foreground="#e1e1e1", background="#111111")
        
        self.style.configure('Search.TEntry', foreground="#888", 
                           fieldbackground="#1a1a1a", borderwidth=1, 
                           relief="solid", padding=5)

    def create_warning_modal(self):
        self.warning_window = tk.Toplevel(self.root)
        self.warning_window.title("Important Notice")
        self.warning_window.configure(bg="#111111")
        self.warning_window.geometry("400x200")
        self.warning_window.resizable(False, False)
        
        self.warning_window.grab_set()
        self.center_window(self.warning_window)
        
        content = tk.Frame(self.warning_window, bg="#111111")
        content.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        warning_icon = tk.Label(content, text="⚠️", font=("Arial", 24), bg="#111111", fg="#ffcc00")
        warning_icon.pack(pady=(0, 10))
        
        message = tk.Label(content, text="This is a free tool\nPlease join our Telegram channel", 
                         font=self.title_font, bg="#111111", fg="#e1e1e1")
        message.pack(pady=5)
        
        telegram_link = tk.Label(content, text="https://t.me/ESCRIPTHITTER", 
                               font=self.base_font, fg="#00a8ff", cursor="hand2", bg="#111111")
        telegram_link.pack(pady=5)
        telegram_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/ESCRIPTHITTER"))
        
        close_btn = ttk.Button(content, text="I Understand", 
                             command=self.warning_window.destroy)
        close_btn.pack(pady=10)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.create_header()
        
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        sidebar = self.create_sidebar(main_container)
        
        self.create_main_content(main_container)
        
        self.create_footer()

    def create_header(self):
        header = ttk.Frame(self.root, height=60)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        title = tk.Label(header, text="NEWERLOSE", font=("Segoe UI", 18, "bold"), 
                       fg="#00a8ff", bg="#0a0a0a")
        title.pack(side=tk.LEFT)
        
        version = tk.Label(header, text="v1.2.0", font=self.base_font, 
                         fg="#666", bg="#0a0a0a")
        version.pack(side=tk.RIGHT)

    def create_sidebar(self, parent):
        sidebar = ttk.Frame(parent, width=240)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        search_frame = ttk.Frame(sidebar)
        search_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                               style='Search.TEntry', font=self.base_font)
        search_entry.pack(fill=tk.X)
        search_entry.bind('<KeyRelease>', self.filter_options)
        
        search_entry.insert(0, "Search options...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) 
                        if search_entry.get() == "Search options..." else None)
        search_entry.bind('<FocusOut>', lambda e: search_entry.insert(0, "Search options...") 
                        if not search_entry.get() else None)
        
        sections = [
            ("Visuals", [
                ("Ambient", True),
                ("Glass Stop", False),
                ("Blush List", True),
                ("Water Vessels", False)
            ]),
            ("Movement", [
                ("Auto Jump", True),
                ("Auto Stride", False),
                ("Edge Jump", True)
            ])
        ]
        
        for title, options in sections:
            section = self.create_section(sidebar, title, options)
            self.all_sections.append(section)

        return sidebar

    def create_main_content(self, parent):
        main_content = ttk.Frame(parent)
        main_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        sections = [
            ("Combat", [
                ("Fast Weapon Switch", False),
                ("Stride Assist", True),
                ("Anti Untreated", False)
            ]),
            ("Players", [
                ("Filter Server Slot", True),
                ("Auto Pack", False)
            ]),
            ("World", [
                ("Blacklock", False),
                ("Fast Reward", True)
            ])
        ]
        
        for title, options in sections:
            section = self.create_section(main_content, title, options)
            self.all_sections.append(section)

    def create_footer(self):
        footer = ttk.Frame(self.root, height=50)
        footer.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        
        buttons = [
            ("Scripts", self.on_scripts_click),
            ("Configs", self.on_configs_click),
            ("Inventory", self.on_inventory_click)
        ]
        
        for btn_text, command in buttons:
            btn = ttk.Button(footer, text=btn_text, command=command)
            btn.pack(side=tk.LEFT, padx=10)

    def create_section(self, parent, title, options):
        section = ttk.Frame(parent)
        section.pack(fill=tk.X, pady=10)
        
        header = ttk.Frame(section)
        header.pack(fill=tk.X)
        
        title_label = tk.Label(header, text=title, font=self.title_font, 
                             fg="#00a8ff", bg="#111111", anchor="w")
        title_label.pack(side=tk.LEFT)
        
        options_frame = ttk.Frame(section)
        options_frame.pack(fill=tk.X, padx=10)
        
        for label, checked in options:
            chk = self.create_checkbox(options_frame, label, checked)
            self.all_checkboxes.append((chk, label, options_frame))
        
        return (section, options_frame)

    def create_checkbox(self, parent, text, checked):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        var = tk.BooleanVar(value=checked)
        chk = ttk.Checkbutton(frame, text=text, variable=var, 
                            style='TCheckbutton')
        chk.pack(anchor="w")
        return (chk, var)

    def filter_options(self, event):
        query = self.search_var.get().lower()
        
        for section, options_frame in self.all_sections:
            section_visible = False
            for chk, label, parent in self.all_checkboxes:
                if parent == options_frame:
                    text = chk.cget('text').lower()
                    if query in text:
                        chk.master.pack()
                        section_visible = True
                    else:
                        chk.master.pack_forget()
            section.pack() if section_visible else section.pack_forget()

    def on_scripts_click(self):
        print("Scripts button clicked - add your logic here")

    def on_configs_click(self):
        print("Configs button clicked - add your logic here")

    def on_inventory_click(self):
        print("Inventory button clicked - add your logic here")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigWindow(root)
    root.mainloop()
