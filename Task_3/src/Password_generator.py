import random
import string
import secrets
import json
import os
from datetime import datetime
import hashlib
import re

# Check for pyperclip availability
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

class AdvancedPasswordGenerator:
    def __init__(self):
        self.history_file = "password_history.json"
        self.strength_rules = {
            'weak': 8,
            'medium': 12,
            'strong': 16,
            'very_strong': 20
        }
        self.load_history()
        
    def load_history(self):
        """Load password generation history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []
        else:
            self.history = []
            
    def save_history(self, password, strength, purpose=""):
        """Save generated password to history (hashed for security)"""
        timestamp = datetime.now().isoformat()
        # Store only the hash of the password for security
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        entry = {
            'timestamp': timestamp,
            'password_hash': password_hash,
            'length': len(password),
            'strength': strength,
            'purpose': purpose
        }
        
        self.history.append(entry)
        
        # Keep only last 50 entries
        if len(self.history) > 50:
            self.history = self.history[-50:]
            
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError:
            print("Warning: Could not save password history")
            
    def generate_password(self, length=16, use_uppercase=True, use_lowercase=True, 
                         use_digits=True, use_symbols=True, exclude_similar=True, 
                         exclude_ambiguous=True, custom_chars="", must_include=""):
        """Generate a secure password with specified criteria"""
        
        # Character sets
        chars = ""
        
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += string.punctuation
            
        # Add custom characters
        if custom_chars:
            chars += custom_chars
            
        # Remove similar characters (e.g., l, 1, I, O, 0)
        if exclude_similar:
            similar_chars = "l1IoO0"
            chars = ''.join(c for c in chars if c not in similar_chars)
            
        # Remove ambiguous symbols
        ambiguous_symbols = "{}[]()/\\'\"`~,;:.<>"
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in ambiguous_symbols)
            
        if not chars:
            raise ValueError("No character sets selected!")
            
        # Ensure minimum length
        if length < 4:
            length = 4
            
        # Generate password using cryptographically secure random generator
        password = []
        
        # First, ensure we have at least one character from each required set
        if use_lowercase and string.ascii_lowercase:
            password.append(secrets.choice(string.ascii_lowercase))
        if use_uppercase and string.ascii_uppercase:
            password.append(secrets.choice(string.ascii_uppercase))
        if use_digits and string.digits:
            password.append(secrets.choice(string.digits))
        if use_symbols and string.punctuation:
            # Filter symbols based on exclusion rules
            symbols = string.punctuation
            if exclude_ambiguous:
                symbols = ''.join(c for c in symbols if c not in ambiguous_symbols)
            if symbols:
                password.append(secrets.choice(symbols))
                
        # Add must_include characters
        if must_include:
            for char in must_include:
                if char in chars:
                    password.append(char)
                    
        # Fill the rest with random characters
        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend(secrets.choice(chars) for _ in range(remaining_length))
            
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def generate_memorable_password(self, word_count=4, separator="-", capitalize=True, add_number=True):
        """Generate a memorable password using dictionary words"""
        # Common word list (in a real application, use a larger dictionary)
        words = [
            "apple", "brave", "cloud", "dragon", "eagle", "flame", "globe", "happy",
            "ice", "jump", "kite", "light", "mountain", "night", "ocean", "peace",
            "quiet", "river", "sun", "tree", "unity", "victory", "water", "xray",
            "yellow", "zenith", "alpha", "beta", "gamma", "delta"
        ]
        
        selected_words = [secrets.choice(words) for _ in range(word_count)]
        
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]
            
        password = separator.join(selected_words)
        
        if add_number:
            password += str(secrets.randbelow(90) + 10)  # Add 2-digit number
            
        return password
    
    def generate_pin(self, length=6):
        """Generate a numeric PIN"""
        if length < 4:
            length = 4
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def check_password_strength(self, password):
        """Check and rate password strength"""
        score = 0
        feedback = []
        
        length = len(password)
        
        # Length scoring
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 2
            
        # Character variety scoring
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[0-9]', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 2
            
        # Deductions for common patterns
        common_patterns = [
            r'123456', r'password', r'qwerty', r'admin', r'welcome',
            r'111111', r'abc123', r'letmein', r'monkey'
        ]
        
        for pattern in common_patterns:
            if pattern in password.lower():
                score -= 2
                feedback.append(f"Contains common pattern: {pattern}")
                
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            score -= 1
            feedback.append("Too many repeated characters")
            
        # Determine strength level
        if score >= 8:
            strength = "Very Strong"
        elif score >= 6:
            strength = "Strong"
        elif score >= 4:
            strength = "Medium"
        elif score >= 2:
            strength = "Weak"
        else:
            strength = "Very Weak"
            
        # Additional feedback
        if length < 8:
            feedback.append("Password should be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            feedback.append("Add uppercase letters")
        if not re.search(r'[0-9]', password):
            feedback.append("Add numbers")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            feedback.append("Add special characters")
            
        return {
            'strength': strength,
            'score': score,
            'length': length,
            'feedback': feedback
        }
    
    def copy_to_clipboard(self, password):
        """Copy password to clipboard"""
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(password)
                return True
            except:
                return False
        return False
    
    def display_strength_meter(self, strength_result):
        """Display a visual strength meter"""
        strength = strength_result['strength']
        score = strength_result['score']
        
        print(f"\nPassword Strength: {strength} ({score}/10)")
        
        # Visual meter
        meter_length = 20
        filled = min(score, 10) * 2  # Convert to percentage
        
        colors = {
            "Very Weak": "🔴",
            "Weak": "🟠", 
            "Medium": "🟡",
            "Strong": "🟢",
            "Very Strong": "🔵"
        }
        
        color = colors.get(strength, "⚫")
        bar = "█" * filled + "░" * (meter_length - filled)
        print(f"{color} [{bar}]")
        
        # Show feedback
        if strength_result['feedback']:
            print("\nSuggestions for improvement:")
            for suggestion in strength_result['feedback']:
                print(f"  • {suggestion}")
    
    def show_history(self):
        """Display password generation history"""
        if not self.history:
            print("\nNo password history found.")
            return
            
        print(f"\n{'Date':<20} {'Length':<8} {'Strength':<12} {'Purpose':<15}")
        print("-" * 60)
        
        for entry in self.history[-10:]:  # Show last 10 entries
            date = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
            print(f"{date:<20} {entry['length']:<8} {entry['strength']:<12} {entry['purpose']:<15}")
    
    def bulk_generate(self, count=5, length=12, strength="medium", purpose="Bulk Generation"):
        """Generate multiple passwords at once"""
        passwords = []
        target_length = self.strength_rules.get(strength, 12)
        actual_length = max(length, target_length)
        
        for i in range(count):
            password = self.generate_password(
                length=actual_length,
                use_uppercase=True,
                use_lowercase=True,
                use_digits=True,
                use_symbols=True
            )
            passwords.append(password)
            # Save each password to history
            self.save_history(password, strength, purpose)
            
        return passwords

def main():
    generator = AdvancedPasswordGenerator()
    
    while True:
        print("\n" + "="*60)
        print("              ADVANCED PASSWORD GENERATOR")
        print("="*60)
        print("1. Generate Custom Password")
        print("2. Generate Strong Password")
        print("3. Generate Memorable Password")
        print("4. Generate PIN")
        print("5. Check Password Strength")
        print("6. Bulk Generate Passwords")
        print("7. View History")
        print("8. Exit")
        print("="*60)
        
        choice = input("Choose an option (1-8): ").strip()
        
        if choice == '1':
            # Custom password generation
            print("\n--- Custom Password Generator ---")
            try:
                length = int(input("Password length (default 16): ") or 16)
                use_upper = input("Include uppercase letters? (y/n, default y): ").lower() != 'n'
                use_lower = input("Include lowercase letters? (y/n, default y): ").lower() != 'n'
                use_digits = input("Include digits? (y/n, default y): ").lower() != 'n'
                use_symbols = input("Include symbols? (y/n, default y): ").lower() != 'n'
                exclude_similar = input("Exclude similar characters (l,1,I,0,O)? (y/n, default y): ").lower() != 'n'
                purpose = input("Purpose (optional): ").strip()
                
                password = generator.generate_password(
                    length=length,
                    use_uppercase=use_upper,
                    use_lowercase=use_lower,
                    use_digits=use_digits,
                    use_symbols=use_symbols,
                    exclude_similar=exclude_similar
                )
                
                print(f"\nGenerated Password: {password}")
                
                # Check strength
                strength_result = generator.check_password_strength(password)
                generator.display_strength_meter(strength_result)
                
                # Save to history
                generator.save_history(password, strength_result['strength'], purpose)
                
                # Copy to clipboard
                if generator.copy_to_clipboard(password):
                    print("✓ Password copied to clipboard!")
                elif not CLIPBOARD_AVAILABLE:
                    print("Clipboard functionality not available. Install pyperclip: pip install pyperclip")
                    
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == '2':
            # Strong password
            print("\n--- Strong Password Generator ---")
            strength_level = input("Strength level (weak/medium/strong/very_strong, default strong): ").strip().lower()
            if strength_level not in generator.strength_rules:
                strength_level = "strong"
                
            length = generator.strength_rules[strength_level]
            purpose = input("Purpose (optional): ").strip()
            
            password = generator.generate_password(
                length=length,
                use_uppercase=True,
                use_lowercase=True,
                use_digits=True,
                use_symbols=True,
                exclude_similar=True
            )
            
            print(f"\nGenerated Password: {password}")
            strength_result = generator.check_password_strength(password)
            generator.display_strength_meter(strength_result)
            generator.save_history(password, strength_result['strength'], purpose)
            
            if generator.copy_to_clipboard(password):
                print("✓ Password copied to clipboard!")
            elif not CLIPBOARD_AVAILABLE:
                print("Clipboard functionality not available. Install pyperclip: pip install pyperclip")
                
        elif choice == '3':
            # Memorable password
            print("\n--- Memorable Password Generator ---")
            word_count = int(input("Number of words (default 4): ") or 4)
            separator = input("Separator (default -): ") or "-"
            capitalize = input("Capitalize words? (y/n, default y): ").lower() != 'n'
            add_number = input("Add number? (y/n, default y): ").lower() != 'n'
            purpose = input("Purpose (optional): ").strip()
            
            password = generator.generate_memorable_password(
                word_count=word_count,
                separator=separator,
                capitalize=capitalize,
                add_number=add_number
            )
            
            print(f"\nGenerated Password: {password}")
            strength_result = generator.check_password_strength(password)
            generator.display_strength_meter(strength_result)
            generator.save_history(password, strength_result['strength'], purpose)
            
            if generator.copy_to_clipboard(password):
                print("✓ Password copied to clipboard!")
            elif not CLIPBOARD_AVAILABLE:
                print("Clipboard functionality not available. Install pyperclip: pip install pyperclip")
                
        elif choice == '4':
            # PIN generation
            print("\n--- PIN Generator ---")
            length = int(input("PIN length (4-12, default 6): ") or 6)
            purpose = input("Purpose (optional): ").strip()
            
            pin = generator.generate_pin(length)
            print(f"\nGenerated PIN: {pin}")
            generator.save_history(pin, "PIN", purpose)
            
            if generator.copy_to_clipboard(pin):
                print("✓ PIN copied to clipboard!")
            elif not CLIPBOARD_AVAILABLE:
                print("Clipboard functionality not available. Install pyperclip: pip install pyperclip")
                
        elif choice == '5':
            # Strength checker
            print("\n--- Password Strength Checker ---")
            password = input("Enter password to check: ").strip()
            strength_result = generator.check_password_strength(password)
            generator.display_strength_meter(strength_result)
            
        elif choice == '6':
            # Bulk generation
            print("\n--- Bulk Password Generator ---")
            count = int(input("Number of passwords to generate (default 5): ") or 5)
            length = int(input("Password length (default 12): ") or 12)
            purpose = input("Purpose (optional, default 'Bulk Generation'): ").strip() or "Bulk Generation"
            
            passwords = generator.bulk_generate(count=count, length=length, purpose=purpose)
            
            print(f"\nGenerated {count} passwords:")
            for i, pwd in enumerate(passwords, 1):
                print(f"{i:2d}. {pwd}")
                
            print(f"\nAll passwords saved to history with purpose '{purpose}'")
                
        elif choice == '7':
            # View history
            generator.show_history()
            
        elif choice == '8':
            print("Thank you for using Advanced Password Generator!")
            break
            
        else:
            print("Invalid choice! Please try again.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()