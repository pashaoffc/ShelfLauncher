# if u see this this is version from github idk just know it

import customtkinter
import customtkinter as ctk
import minecraft_launcher_lib
from shelf.libs.shelf_nick import shelf_nick
import os
import subprocess
import threading
#trying do ts manualy pls no hate

#ShelfLauncher

# ctk settings
customtkinter.set_appearance_mode("dark") #makes dark mode NOT CHANGABLE
customtkinter.set_default_color_theme("shelf/themes/dark_red.json")
# Settings
with open(".versions", "r", encoding="utf-8") as file: # versions file
    versions_list = [line.strip() for line in file if line.strip()] # cur no forge / fabric sorry

gennick = shelf_nick()

# Ui

app = customtkinter.CTk()
app.geometry("400x300")
app.title("Shelf Launcher")

class Tabs(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        #i would make something on cli if i was lazy and wont read documentation

        self.add('Menu')
        self.add('Settings')
        self.add('Credits')
        ## MENU MENU MENU MENU
        self.informname = customtkinter.CTkLabel(
        self.tab('Menu'),
        text="Shelf Launcher",
        fg_color="transparent"
        )

        self.informname.pack(pady=5, padx=10)
        self.nameinput = customtkinter.CTkTextbox(
        self.tab('Menu'),
        height=10,

        )

        self.nameinput.bind("<KeyRelease>", lambda e: open(os.path.join(os.path.dirname(__file__), "shelf", "nick.txt"), "w", encoding="utf-8").write(self.nameinput.get('1.0', 'end-1c').strip()))
        if os.path.exists(os.path.join(os.path.dirname(__file__), "shelf", "nick.txt")): self.nameinput.insert("1.0", open(os.path.join(os.path.dirname(__file__), "shelf", "nick.txt"), "r", encoding="utf-8").read().strip())
        
        #self.nameinput.delete("1.0", "end")
        #self.nameinput.insert("1.0", gennick)
        # REMOVED cuz i made save nick
        self.nameinput.pack(pady=5, padx=10)
        # found that u can put it like list idk how to call gnna go for a walk 26-07-2026 21-25
        self.version_dropdown = ctk.CTkComboBox(
        self.tab("Menu"), 
        values=versions_list, 
        width=200
        )
        
        
        self.version_dropdown.pack(pady=20)

        if versions_list:
            self.version_dropdown.set(versions_list[0])

        self.play_btn = customtkinter.CTkButton(
        self.tab('Menu'),
        text="Play",
        command=lambda: run_game(self),
        )

        self.play_btn.pack(pady=10)

        self.ram_slider = customtkinter.CTkSlider(self.tab('Settings'), from_=1, to=8, number_of_steps=7, command=lambda v: open(os.path.join(os.path.dirname(__file__), "shelf", "ram.txt"), "w").write(str(int(v)))); self.ram_slider.pack(pady=20); self.ram_slider.set(int(open(os.path.join(os.path.dirname(__file__), "shelf", "ram.txt"), "r").read().strip()) if os.path.exists(os.path.join(os.path.dirname(__file__), "shelf", "ram.txt")) else 2)
        


def run_game(app_window):
    username = app_window.nameinput.get('1.0', 'end-1c').strip()
    if not username:
        username = 'ShelfLauncher'

    
    try:
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        nick_file_path = os.path.join(current_dir, "shelf", "nick.txt")
        
        with open(nick_file_path, "w", encoding="utf-8") as f:
            f.write(username)
    except Exception as e:
        print(f"Не удалось сохранить ник: {e}")

    version = app_window.version_dropdown.get().strip()
    minecraft_dir = os.path.join(os.getenv('APPDATA'), ".minecraft")
    ram = open(os.path.join(os.path.dirname(__file__), "shelf", "ram.txt"), "r").read().strip() if os.path.exists(os.path.join(os.path.dirname(__file__), "shelf", "ram.txt")) else "2"
    options = {"username": username, "uuid": "00000000000000000000000000000000", "token": "00000000000000000000000000000000", "user_type": "legacy", "user_properties": "{}", "meta": {"type": "mojang", "demo": False}, "jvmArguments": [f"-Xmx{ram}G", f"-Xms{ram}G"]}
    try:
       
        print(f"Checking/Downloading version {version}...")
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_dir)
        
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_dir, options)
        subprocess.Popen(minecraft_command)
    except Exception as e:
        print(f"Error: {e}")

my_tabs = Tabs(master=app)
my_tabs.pack(fill="both", expand=True, padx=10, pady=10)

app.iconbitmap("shelf/icon.ico")
app.mainloop()
