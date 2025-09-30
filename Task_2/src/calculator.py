# advanced_calculator.py
# Advanced Command-line Calculator with Multiple Features

import math
import sys
from datetime import datetime

class AdvancedCalculator:
    def __init__(self):
        self.history = []
        self.memory = 0
        
    def display_menu(self):
        print("\n" + "="*50)
        print("           ADVANCED CALCULATOR")
        print("="*50)
        print("1. Basic Arithmetic")
        print("2. Scientific Functions")
        print("3. Financial Calculations")
        print("4. Statistics")
        print("5. Number Conversion")
        print("6. View History")
        print("7. Memory Functions")
        print("8. Clear History")
        print("9. Exit")
        print("="*50)
        
    def add_to_history(self, operation, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{timestamp} | {operation} = {result}")
        # Keep only last 20 entries
        if len(self.history) > 20:
            self.history.pop(0)
            
    def basic_arithmetic(self):
        print("\n--- Basic Arithmetic ---")
        try:
            expression = input("Enter expression (e.g., 2 + 3 * 4): ")
            # Basic safety check - only allow numbers and operators
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                print("Error: Only numbers and basic operators allowed!")
                return
                
            result = eval(expression)
            operation = f"{expression}"
            print(f"Result: {result}")
            self.add_to_history(operation, result)
            
        except ZeroDivisionError:
            print("Error: Division by zero!")
        except Exception as e:
            print(f"Error: Invalid expression! {e}")
            
    def scientific_functions(self):
        print("\n--- Scientific Functions ---")
        print("1. Power (x^y)")
        print("2. Square Root")
        print("3. Logarithm (base 10)")
        print("4. Natural Logarithm")
        print("5. Sine")
        print("6. Cosine")
        print("7. Tangent")
        print("8. Factorial")
        
        choice = input("Choose operation (1-8): ")
        
        try:
            if choice == '1':
                base = float(input("Enter base: "))
                exponent = float(input("Enter exponent: "))
                result = math.pow(base, exponent)
                operation = f"{base} ^ {exponent}"
                
            elif choice == '2':
                num = float(input("Enter number: "))
                if num < 0:
                    print("Error: Cannot calculate square root of negative number!")
                    return
                result = math.sqrt(num)
                operation = f"√{num}"
                
            elif choice == '3':
                num = float(input("Enter number: "))
                if num <= 0:
                    print("Error: Logarithm undefined for non-positive numbers!")
                    return
                result = math.log10(num)
                operation = f"log10({num})"
                
            elif choice == '4':
                num = float(input("Enter number: "))
                if num <= 0:
                    print("Error: Natural log undefined for non-positive numbers!")
                    return
                result = math.log(num)
                operation = f"ln({num})"
                
            elif choice == '5':
                angle = float(input("Enter angle in degrees: "))
                result = math.sin(math.radians(angle))
                operation = f"sin({angle}°)"
                
            elif choice == '6':
                angle = float(input("Enter angle in degrees: "))
                result = math.cos(math.radians(angle))
                operation = f"cos({angle}°)"
                
            elif choice == '7':
                angle = float(input("Enter angle in degrees: "))
                result = math.tan(math.radians(angle))
                operation = f"tan({angle}°)"
                
            elif choice == '8':
                num = int(input("Enter positive integer: "))
                if num < 0:
                    print("Error: Factorial undefined for negative numbers!")
                    return
                result = math.factorial(num)
                operation = f"{num}!"
                
            else:
                print("Invalid choice!")
                return
                
            print(f"Result: {result}")
            self.add_to_history(operation, result)
            
        except ValueError:
            print("Error: Invalid input! Please enter valid numbers.")
        except Exception as e:
            print(f"Error: {e}")
            
    def financial_calculations(self):
        print("\n--- Financial Calculations ---")
        print("1. Simple Interest")
        print("2. Compound Interest")
        print("3. Loan EMI Calculation")
        
        choice = input("Choose operation (1-3): ")
        
        try:
            if choice == '1':
                principal = float(input("Enter principal amount: "))
                rate = float(input("Enter annual interest rate (%): "))
                time = float(input("Enter time in years: "))
                interest = (principal * rate * time) / 100
                total = principal + interest
                result = total
                operation = f"Simple Interest: P={principal}, R={rate}%, T={time}yr"
                print(f"Total amount: {total}")
                print(f"Interest earned: {interest}")
                
            elif choice == '2':
                principal = float(input("Enter principal amount: "))
                rate = float(input("Enter annual interest rate (%): "))
                time = float(input("Enter time in years: "))
                n = int(input("Enter compounding frequency per year: "))
                amount = principal * math.pow(1 + (rate/100)/n, n * time)
                interest = amount - principal
                result = amount
                operation = f"Compound Interest: P={principal}, R={rate}%, T={time}yr, n={n}"
                print(f"Total amount: {amount:.2f}")
                print(f"Interest earned: {interest:.2f}")
                
            elif choice == '3':
                principal = float(input("Enter loan amount: "))
                rate = float(input("Enter annual interest rate (%): "))
                time = int(input("Enter loan term in years: "))
                monthly_rate = rate / 12 / 100
                months = time * 12
                emi = (principal * monthly_rate * math.pow(1 + monthly_rate, months)) / (math.pow(1 + monthly_rate, months) - 1)
                result = emi
                operation = f"EMI: Loan={principal}, Rate={rate}%, Term={time}yr"
                print(f"Monthly EMI: {emi:.2f}")
                total_payment = emi * months
                print(f"Total payment: {total_payment:.2f}")
                print(f"Total interest: {total_payment - principal:.2f}")
                
            else:
                print("Invalid choice!")
                return
                
            self.add_to_history(operation, result)
            
        except ValueError:
            print("Error: Invalid input! Please enter valid numbers.")
            
    def statistics(self):
        print("\n--- Statistics ---")
        try:
            numbers = input("Enter numbers separated by spaces: ")
            num_list = [float(x) for x in numbers.split()]
            
            if not num_list:
                print("Error: No numbers entered!")
                return
                
            mean = sum(num_list) / len(num_list)
            sorted_list = sorted(num_list)
            n = len(sorted_list)
            
            # Median
            if n % 2 == 0:
                median = (sorted_list[n//2 - 1] + sorted_list[n//2]) / 2
            else:
                median = sorted_list[n//2]
                
            # Mode
            from collections import Counter
            freq = Counter(num_list)
            mode = freq.most_common(1)[0][0]
            
            # Standard Deviation
            variance = sum((x - mean) ** 2 for x in num_list) / len(num_list)
            std_dev = math.sqrt(variance)
            
            print(f"Count: {len(num_list)}")
            print(f"Mean: {mean:.2f}")
            print(f"Median: {median:.2f}")
            print(f"Mode: {mode:.2f}")
            print(f"Min: {min(num_list):.2f}")
            print(f"Max: {max(num_list):.2f}")
            print(f"Standard Deviation: {std_dev:.2f}")
            
            operation = f"Stats for {len(num_list)} numbers"
            self.add_to_history(operation, f"mean={mean:.2f}")
            
        except ValueError:
            print("Error: Please enter valid numbers!")
            
    def number_conversion(self):
        print("\n--- Number Conversion ---")
        print("1. Decimal to Binary")
        print("2. Binary to Decimal")
        print("3. Decimal to Hexadecimal")
        print("4. Hexadecimal to Decimal")
        
        choice = input("Choose conversion (1-4): ")
        
        try:
            if choice == '1':
                num = int(input("Enter decimal number: "))
                result = bin(num)[2:]
                operation = f"Decimal {num} to Binary"
                
            elif choice == '2':
                binary = input("Enter binary number: ")
                result = int(binary, 2)
                operation = f"Binary {binary} to Decimal"
                
            elif choice == '3':
                num = int(input("Enter decimal number: "))
                result = hex(num)[2:].upper()
                operation = f"Decimal {num} to Hexadecimal"
                
            elif choice == '4':
                hex_num = input("Enter hexadecimal number: ")
                result = int(hex_num, 16)
                operation = f"Hexadecimal {hex_num} to Decimal"
                
            else:
                print("Invalid choice!")
                return
                
            print(f"Result: {result}")
            self.add_to_history(operation, result)
            
        except ValueError:
            print("Error: Invalid number format!")
            
    def view_history(self):
        print("\n--- Calculation History ---")
        if not self.history:
            print("No history available.")
            return
            
        for i, entry in enumerate(self.history, 1):
            print(f"{i}. {entry}")
            
    def memory_functions(self):
        print("\n--- Memory Functions ---")
        print(f"Current Memory: {self.memory}")
        print("1. Store to Memory (MS)")
        print("2. Recall from Memory (MR)")
        print("3. Add to Memory (M+)")
        print("4. Subtract from Memory (M-)")
        print("5. Clear Memory (MC)")
        
        choice = input("Choose operation (1-5): ")
        
        try:
            if choice == '1':
                self.memory = float(input("Enter value to store: "))
                print(f"Value {self.memory} stored in memory.")
                
            elif choice == '2':
                print(f"Memory value: {self.memory}")
                
            elif choice == '3':
                value = float(input("Enter value to add: "))
                self.memory += value
                print(f"Added {value}. New memory: {self.memory}")
                
            elif choice == '4':
                value = float(input("Enter value to subtract: "))
                self.memory -= value
                print(f"Subtracted {value}. New memory: {self.memory}")
                
            elif choice == '5':
                self.memory = 0
                print("Memory cleared.")
                
            else:
                print("Invalid choice!")
                
        except ValueError:
            print("Error: Please enter a valid number!")
            
    def clear_history(self):
        self.history.clear()
        print("History cleared!")
        
    def run(self):
        print("Welcome to Advanced Calculator!")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-9): ")
            
            if choice == '1':
                self.basic_arithmetic()
            elif choice == '2':
                self.scientific_functions()
            elif choice == '3':
                self.financial_calculations()
            elif choice == '4':
                self.statistics()
            elif choice == '5':
                self.number_conversion()
            elif choice == '6':
                self.view_history()
            elif choice == '7':
                self.memory_functions()
            elif choice == '8':
                self.clear_history()
            elif choice == '9':
                print("Thank you for using Advanced Calculator!")
                sys.exit()
            else:
                print("Invalid choice! Please try again.")
                
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    calculator = AdvancedCalculator()
    calculator.run()