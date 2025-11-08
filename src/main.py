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
from pynput import mouse, keyboard as kb

warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

class PhonkPrank:
    def __init__(self, root):
        self.root = root
        self.root.title("py-phonk")
        self.root.geometry("210x225")
        
        pygame.mixer.init()
        
        self.is_active = False
        self.toggle_var = tk.BooleanVar()
        
        try:
            icon_img = Image.open("icon.png")
            icon_img = icon_img.resize((128, 128), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            
            self.icon_label = tk.Label(root, image=self.icon_photo)
            self.icon_label.pack(pady=10)
        except:
            pass
        
        self.toggle_switch = ttk.Checkbutton(
            root, 
            text="Prank Mode",
            variable=self.toggle_var,
            command=self.toggle_prank,
            style="Switch.TCheckbutton"
        )
        self.toggle_switch.pack(pady=10)
        
        style = ttk.Style()
        style.configure("Switch.TCheckbutton", padding=10)
        
        self.check_folders()
        
        self.user_actions = []
        self.action_listener_active = False
        self.mouse_listener = None
        self.keyboard_listener = None
        
        self.prank_in_progress = False
    
    def check_folders(self):
        if not os.path.exists("sounds"):
            os.makedirs("sounds")
            
        if not os.path.exists("textures"):
            os.makedirs("textures")
    
    def toggle_prank(self):
        if self.toggle_var.get():
            self.start_prank()
        else:
            self.stop_prank()
    
    def start_prank(self):
        self.is_active = True
        self.start_action_listeners()
    
    def stop_prank(self):
        self.is_active = False
        self.stop_action_listeners()
        pygame.mixer.music.stop()
        if hasattr(self, 'effect_window'):
            self.root.after(0, self.close_effect_window)
    
    def start_action_listeners(self):
        self.user_actions = []
        self.action_listener_active = True
        
        def on_click(x, y, button, pressed):
            if pressed and self.action_listener_active and not self.prank_in_progress:
                self.user_actions.append(("click", x, y, button))
                self.check_for_prank_trigger()
        
        def on_key_press(key):
            if self.action_listener_active and not self.prank_in_progress:
                try:
                    self.user_actions.append(("key", key.char))
                except AttributeError:
                    self.user_actions.append(("key", key))
                self.check_for_prank_trigger()
        
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.keyboard_listener = kb.Listener(on_press=on_key_press)
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
    
    def stop_action_listeners(self):
        self.action_listener_active = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
    
    def check_for_prank_trigger(self):
        if len(self.user_actions) >= random.randint(3, 8):
            if random.random() < 0.3:
                self.trigger_prank()
    
    def trigger_prank(self):
        if not self.is_active or self.prank_in_progress:
            return
            
        self.prank_in_progress = True
        self.stop_action_listeners()
        
        prank_thread = threading.Thread(target=self.run_prank)
        prank_thread.daemon = True
        prank_thread.start()
    
    def run_prank(self):
        try:
            sound_files = [f for f in os.listdir("sounds") if f.endswith('.ogg')]
            if not sound_files:
                self.root.after(0, self.end_prank)
                return
                
            texture_files = [f for f in os.listdir("textures") if f.endswith('.png')]
            if not texture_files:
                self.root.after(0, self.end_prank)
                return
            
            selected_sound = random.choice(sound_files)
            selected_texture = random.choice(texture_files)
            
            sound_path = os.path.join("sounds", selected_sound)
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            
            sound = pygame.mixer.Sound(sound_path)
            duration = sound.get_length()
            
            self.root.after(0, self.create_effect_window, selected_texture)
            
            prank_thread = threading.Thread(target=self.run_random_prank, args=(duration,))
            prank_thread.daemon = True
            prank_thread.start()
            
            time.sleep(duration)
            
            if self.is_active:
                self.root.after(0, self.close_effect_window)
                self.root.after(0, self.end_prank)
                
        except Exception as e:
            print(f"Error: {e}")
            self.root.after(0, self.end_prank)
    
    def run_random_prank(self, duration):
        start_time = time.time()
        
        while time.time() - start_time < duration and self.is_active:
            try:
                prank_type = random.choice(["keyboard", "mouse", "both"])
                
                if prank_type == "keyboard" or prank_type == "both":
                    self.keyboard_prank()
                
                if prank_type == "mouse" or prank_type == "both":
                    self.mouse_prank()
                
                time.sleep(random.uniform(0.5, 2))
            except:
                pass
    
    def keyboard_prank(self):
        actions = [
            lambda: keyboard.write(''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3, 10)))),
            lambda: pyautogui.hotkey('ctrl', 'c'),
            lambda: pyautogui.hotkey('ctrl', 'v'),
            lambda: pyautogui.press(random.choice(['enter', 'tab', 'esc', 'backspace'])),
            lambda: pyautogui.press('f11')
        ]
        
        random.choice(actions)()
    
    def mouse_prank(self):
        screen_width, screen_height = pyautogui.size()
        
        actions = [
            lambda: pyautogui.moveTo(random.randint(0, screen_width), random.randint(0, screen_height), duration=0.5),
            lambda: pyautogui.click(),
            lambda: pyautogui.scroll(random.randint(-5, 5)),
            lambda: pyautogui.dragTo(random.randint(0, screen_width), random.randint(0, screen_height), duration=0.5)
        ]
        
        random.choice(actions)()
    
    def end_prank(self):
        self.prank_in_progress = False
        if self.is_active:
            self.start_action_listeners()
    
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
            image = Image.open(texture_path).convert("RGBA")
            
            screen_width = self.effect_window.winfo_screenwidth()
            screen_height = self.effect_window.winfo_screenheight()
            max_size = min(screen_width, screen_height) // 3
            
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            texture_photo = ImageTk.PhotoImage(image)
            
            image_label = tk.Label(
                self.effect_window, 
                image=texture_photo, 
                bg='black',
                borderwidth=0
            )
            image_label.image = texture_photo
            
            image_label.place(
                relx=0.5, 
                rely=0.75,
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
