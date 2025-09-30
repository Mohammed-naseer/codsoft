# advanced_gui_calculator.py
# Advanced GUI Calculator using Tkinter

import tkinter as tk
from tkinter import ttk, messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Variables
        self.current_input = tk.StringVar(value="0")
        self.previous_input = ""
        self.operator = ""
        self.new_input = True
        
        # Styling
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
        # Bind keyboard events
        self.bind_events()
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("Number.TButton", background="#f0f0f0")
        style.configure("Operator.TButton", background="#ff9500", foreground="white")
        style.configure("Special.TButton", background="#a6a6a6")
        style.configure("Display.TLabel", font=("Arial", 20), background="black", foreground="white")
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.display = ttk.Label(
            display_frame, 
            textvariable=self.current_input, 
            style="Display.TLabel",
            anchor="e"
        )
        self.display.pack(fill=tk.X, ipady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button layout
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '=']
        ]
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == '':
                    continue
                    
                if text == '0':
                    btn = ttk.Button(
                        buttons_frame, 
                        text=text, 
                        style="Number.TButton",
                        command=lambda t=text: self.button_click(t)
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky="ew", padx=1, pady=1)
                else:
                    # Determine button style
                    if text in ['÷', '×', '-', '+', '=']:
                        style = "Operator.TButton"
                    elif text in ['C', '±', '%']:
                        style = "Special.TButton"
                    else:
                        style = "Number.TButton"
                    
                    btn = ttk.Button(
                        buttons_frame, 
                        text=text, 
                        style=style,
                        command=lambda t=text: self.button_click(t)
                    )
                    btn.grid(row=i, column=j, sticky="ew", padx=1, pady=1)
        
        # Configure grid weights for responsive layout
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)
    
    def bind_events(self):
        # Bind keyboard events
        self.root.bind('<Key>', self.key_press)
        self.root.focus_set()
    
    def key_press(self, event):
        key = event.char
        
        if key in '0123456789':
            self.button_click(key)
        elif key == '.':
            self.button_click('.')
        elif key == '+':
            self.button_click('+')
        elif key == '-':
            self.button_click('-')
        elif key in ['*', 'x', 'X']:
            self.button_click('×')
        elif key in ['/', '÷']:
            self.button_click('÷')
        elif key in ['\r', '=']:  # Enter or = key
            self.button_click('=')
        elif event.keysym == 'Escape':
            self.button_click('C')
        elif event.keysym == 'BackSpace':
            self.backspace()
    
    def button_click(self, value):
        if value in '0123456789':
            self.input_number(value)
        elif value == '.':
            self.input_decimal()
        elif value in ['+', '-', '×', '÷']:
            self.input_operator(value)
        elif value == '=':
            self.calculate()
        elif value == 'C':
            self.clear()
        elif value == '±':
            self.negate()
        elif value == '%':
            self.percentage()
    
    def input_number(self, num):
        if self.new_input or self.current_input.get() == "0":
            self.current_input.set(num)
            self.new_input = False
        else:
            current = self.current_input.get()
            self.current_input.set(current + num)
    
    def input_decimal(self):
        if self.new_input:
            self.current_input.set("0.")
            self.new_input = False
        elif "." not in self.current_input.get():
            self.current_input.set(self.current_input.get() + ".")
    
    def input_operator(self, op):
        if self.operator and not self.new_input:
            self.calculate()
        
        self.previous_input = self.current_input.get()
        self.operator = op
        self.new_input = True
    
    def calculate(self):
        if not self.operator or self.new_input:
            return
        
        try:
            current = float(self.current_input.get())
            previous = float(self.previous_input)
            
            if self.operator == '+':
                result = previous + current
            elif self.operator == '-':
                result = previous - current
            elif self.operator == '×':
                result = previous * current
            elif self.operator == '÷':
                if current == 0:
                    messagebox.showerror("Error", "Division by zero is not allowed!")
                    return
                result = previous / current
            
            # Format result
            if result.is_integer():
                self.current_input.set(str(int(result)))
            else:
                self.current_input.set(str(result))
            
            self.operator = ""
            self.new_input = True
            
        except ValueError:
            messagebox.showerror("Error", "Invalid calculation!")
            self.clear()
    
    def clear(self):
        self.current_input.set("0")
        self.previous_input = ""
        self.operator = ""
        self.new_input = True
    
    def negate(self):
        try:
            current = float(self.current_input.get())
            self.current_input.set(str(-current))
        except ValueError:
            pass
    
    def percentage(self):
        try:
            current = float(self.current_input.get())
            self.current_input.set(str(current / 100))
            self.new_input = True
        except ValueError:
            pass
    
    def backspace(self):
        if not self.new_input:
            current = self.current_input.get()
            if len(current) > 1:
                self.current_input.set(current[:-1])
            else:
                self.current_input.set("0")
                self.new_input = True

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()