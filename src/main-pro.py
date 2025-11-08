import tkinter as tk
from tkinter import ttk
import os
import random
import pygame
import time
from PIL import Image, ImageTk, ImageOps, ImageGrab
import threading
import warnings
import pyautogui
import keyboard

warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

class PhonkPrank:
    def __init__(self, root):
        self.root = root
        self.root.title("py-phonk")
        self.root.geometry("200x100")
        
        pygame.mixer.init()
        
        self.is_active = False
        self.toggle_var = tk.BooleanVar()
        self.toggle_switch = ttk.Checkbutton(
            root, 
            text="Prank Mode",
            variable=self.toggle_var,
            command=self.toggle_prank,
            style="Switch.TCheckbutton"
        )
        self.toggle_switch.pack(pady=20)
        
        style = ttk.Style()
        style.configure("Switch.TCheckbutton", padding=10)
        
        self.check_folders()
        self.user_actions = []
        self.setup_user_monitoring()
    
    def check_folders(self):
        if not os.path.exists("sounds"):
            os.makedirs("sounds")
            
        if not os.path.exists("textures"):
            os.makedirs("textures")
    
    def setup_user_monitoring(self):
        self.monitor_thread = threading.Thread(target=self.monitor_user_actions)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def monitor_user_actions(self):
        while True:
            time.sleep(0.1)
            if not self.is_active:
                continue
                
            if random.random() < 0.3:
                self.trigger_random_prank()
    
    def trigger_random_prank(self):
        prank_type = random.choice(["keyboard", "mouse", "screen", "audio"])
        
        if prank_type == "keyboard":
            self.keyboard_prank()
        elif prank_type == "mouse":
            self.mouse_prank()
        elif prank_type == "screen":
            self.screen_prank()
        elif prank_type == "audio":
            self.audio_prank()
    
    def toggle_prank(self):
        if self.toggle_var.get():
            self.start_prank()
        else:
            self.stop_prank()
    
    def start_prank(self):
        self.is_active = True
        
        prank_thread = threading.Thread(target=self.run_prank)
        prank_thread.daemon = True
        prank_thread.start()
    
    def stop_prank(self):
        self.is_active = False
        pygame.mixer.music.stop()
        if hasattr(self, 'effect_window'):
            self.root.after(0, self.close_effect_window)
    
    def run_prank(self):
        try:
            sound_files = [f for f in os.listdir("sounds") if f.endswith('.ogg')]
            if not sound_files:
                self.root.after(0, self.reset_toggle)
                return
                
            texture_files = [f for f in os.listdir("textures") if f.endswith('.png')]
            if not texture_files:
                self.root.after(0, self.reset_toggle)
                return
            
            selected_sound = random.choice(sound_files)
            selected_texture = random.choice(texture_files)
            
            sound_path = os.path.join("sounds", selected_sound)
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            
            sound = pygame.mixer.Sound(sound_path)
            duration = sound.get_length()
            
            self.root.after(0, self.create_effect_window, selected_texture)
            
            time.sleep(duration)
            
            if self.is_active:
                self.root.after(0, self.close_effect_window)
                self.root.after(0, self.reset_toggle)
                
        except Exception as e:
            print(f"Error: {e}")
            self.root.after(0, self.reset_toggle)
    
    def keyboard_prank(self):
        actions = [
            lambda: keyboard.write(''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 10)))),
            lambda: pyautogui.hotkey('ctrl', 'c'),
            lambda: pyautogui.hotkey('ctrl', 'v'),
            lambda: pyautogui.press(random.choice(['enter', 'tab', 'esc', 'backspace'])),
            lambda: pyautogui.press('f11'),
            lambda: pyautogui.hotkey('alt', 'tab'),
            lambda: pyautogui.hotkey('win', 'd'),
            lambda: pyautogui.typewrite(' '.join(['lol', 'haha', 'wtf', 'omg'][random.randint(0, 3)])),
            lambda: pyautogui.hotkey('ctrl', 'a'),
            lambda: pyautogui.hotkey('ctrl', 'z')
        ]
        
        random.choice(actions)()
    
    def mouse_prank(self):
        screen_width, screen_height = pyautogui.size()
        
        actions = [
            lambda: pyautogui.moveTo(random.randint(0, screen_width), random.randint(0, screen_height), duration=0.5),
            lambda: pyautogui.click(),
            lambda: pyautogui.scroll(random.randint(-5, 5)),
            lambda: pyautogui.dragTo(random.randint(0, screen_width), random.randint(0, screen_height), duration=0.5),
            lambda: pyautogui.rightClick(),
            lambda: pyautogui.doubleClick(),
            lambda: pyautogui.moveRel(random.randint(-100, 100), random.randint(-100, 100), duration=0.5),
            lambda: pyautogui.mouseDown(),
            lambda: pyautogui.mouseUp()
        ]
        
        random.choice(actions)()
    
    def screen_prank(self):
        actions = [
            lambda: self.invert_colors(),
            lambda: self.rotate_screen(),
            lambda: self.flash_screen()
        ]
        
        random.choice(actions)()
    
    def audio_prank(self):
        try:
            sound_files = [f for f in os.listdir("sounds") if f.endswith('.ogg')]
            if sound_files:
                sound_path = os.path.join("sounds", random.choice(sound_files))
                sound = pygame.mixer.Sound(sound_path)
                sound.play()
        except:
            pass
    
    def invert_colors(self):
        try:
            screenshot = ImageGrab.grab()
            inverted = ImageOps.invert(screenshot)
            
            self.invert_window = tk.Toplevel(self.root)
            self.invert_window.attributes('-fullscreen', True)
            self.invert_window.attributes('-topmost', True)
            
            photo = ImageTk.PhotoImage(inverted)
            
            label = tk.Label(self.invert_window, image=photo)
            label.image = photo
            label.place(x=0, y=0, relwidth=1, relheight=1)
            
            self.root.after(1000, lambda: self.invert_window.destroy() if hasattr(self, 'invert_window') else None)
        except:
            pass
    
    def rotate_screen(self):
        try:
            screenshot = ImageGrab.grab()
            rotated = screenshot.rotate(180)
            
            self.rotate_window = tk.Toplevel(self.root)
            self.rotate_window.attributes('-fullscreen', True)
            self.rotate_window.attributes('-topmost', True)
            
            photo = ImageTk.PhotoImage(rotated)
            
            label = tk.Label(self.rotate_window, image=photo)
            label.image = photo
            label.place(x=0, y=0, relwidth=1, relheight=1)
            
            self.root.after(1500, lambda: self.rotate_window.destroy() if hasattr(self, 'rotate_window') else None)
        except:
            pass
    
    def flash_screen(self):
        try:
            self.flash_window = tk.Toplevel(self.root)
            self.flash_window.attributes('-fullscreen', True)
            self.flash_window.attributes('-topmost', True)
            self.flash_window.configure(bg='white')
            
            self.root.after(200, lambda: self.flash_window.destroy() if hasattr(self, 'flash_window') else None)
        except:
            pass
    
    def reset_toggle(self):
        self.is_active = False
        self.toggle_var.set(False)
    
    def create_effect_window(self, texture_file):
        try:
            screenshot = ImageGrab.grab()
            screenshot_bw = ImageOps.grayscale(screenshot)
            
            self.effect_window = tk.Toplevel(self.root)
            self.effect_window.attributes('-fullscreen', True)
            self.effect_window.attributes('-topmost', True)
            self.effect_window.configure(bg='black')
            
            photo = ImageTk.PhotoImage(screenshot_bw)
            
            bg_label = tk.Label(
                self.effect_window, 
                image=photo, 
                bg='black'
            )
            bg_label.image = photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            texture_path = os.path.join("textures", texture_file)
            image = Image.open(texture_path)
            
            screen_width = self.effect_window.winfo_screenwidth()
            screen_height = self.effect_window.winfo_screenheight()
            max_size = min(screen_width, screen_height) // 3
            
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            image_bw = ImageOps.grayscale(image)
            texture_photo = ImageTk.PhotoImage(image_bw)
            
            image_label = tk.Label(
                self.effect_window, 
                image=texture_photo, 
                bg='black',
                borderwidth=0
            )
            image_label.image = texture_photo
            
            image_label.place(
                relx=0.5, 
                rely=0.6, 
                anchor='center'
            )
            
        except Exception as e:
            print(f"Effect window error: {e}")
    
    def close_effect_window(self):
        if hasattr(self, 'effect_window'):
            self.effect_window.destroy()

def main():
    root = tk.Tk()
    app = PhonkPrank(root)
    root.mainloop()

if __name__ == "__main__":
    main()