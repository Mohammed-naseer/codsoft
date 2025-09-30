import os
import sys
from datetime import datetime

# Add the project root to Python path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display a fancy banner"""
    banner = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚀 ADVANCED TO-DO LIST MANAGER v2.0                      ║
║                                                              ║
║    "Organize Your Life, One Task at a Time"                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if required packages are installed"""
    try:
        import tkinter
        import json
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        return False

def get_app_statistics():
    """Display application statistics"""
    try:
        from core import storage
        tasks = storage.load_tasks()
        total_tasks = len(tasks)
        completed = len([t for t in tasks if t["done"]])
        
        print("\n📊 Application Statistics:")
        print(f"   • Total tasks in database: {total_tasks}")
        print(f"   • Completed tasks: {completed}")
        print(f"   • Pending tasks: {total_tasks - completed}")
        
        if total_tasks > 0:
            completion_rate = (completed / total_tasks) * 100
            print(f"   • Completion rate: {completion_rate:.1f}%")
        
        # Check data directory
        data_dir = "data"
        if os.path.exists(data_dir):
            todo_file = os.path.join(data_dir, "todo.json")
            if os.path.exists(todo_file):
                file_size = os.path.getsize(todo_file)
                print(f"   • Data file size: {file_size} bytes")
        
        return True
    except Exception as e:
        print(f"   • Could not load statistics: {e}")
        return False

def display_feature_list():
    """Display the features of each version"""
    print("\n🎯 FEATURES COMPARISON:")
    
    print("\n📟 CLI Version:")
    print("   ✓ Full keyboard navigation")
    print("   ✓ Advanced filtering and search")
    print("   ✓ Task statistics and analytics")
    print("   ✓ Import/export functionality")
    print("   ✓ Priority levels and due dates")
    print("   ✓ Categories and tags")
    print("   ✓ Undo/redo operations")
    
    print("\n🖥️  GUI Version:")
    print("   ✓ Modern graphical interface")
    print("   ✓ Drag-and-drop functionality")
    print("   ✓ Visual task management")
    print("   ✓ Real-time search and filters")
    print("   ✓ Interactive calendar")
    print("   ✓ Color-coded priorities")
    print("   ✓ Treeview with multiple columns")

def check_data_health():
    """Check the health of the data file"""
    try:
        from core import storage
        tasks = storage.load_tasks()
        
        if not tasks:
            print("💡 Tip: No tasks found. Start by adding some tasks!")
            return True
            
        # Check for tasks without titles
        invalid_tasks = [t for t in tasks if not t.get("title") or not t["title"].strip()]
        if invalid_tasks:
            print("⚠️  Warning: Found tasks with empty titles")
            
        # Check for overdue tasks
        from datetime import datetime
        overdue = 0
        for task in tasks:
            if task.get("due_date") and not task["done"]:
                try:
                    due = datetime.strptime(task["due_date"], "%Y-%m-%d")
                    if due < datetime.now():
                        overdue += 1
                except:
                    pass
        
        if overdue > 0:
            print(f"⏰ You have {overdue} overdue task(s)!")
            
        return True
    except Exception as e:
        print(f"❌ Data health check failed: {e}")
        return False

def backup_data():
    """Create a backup of the data file"""
    try:
        from core import storage
        import shutil
        import time
        
        data_file = "data/todo.json"
        if os.path.exists(data_file):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_file = f"data/backup/todo_backup_{timestamp}.json"
            
            # Create backup directory if it doesn't exist
            os.makedirs("data/backup", exist_ok=True)
            
            shutil.copy2(data_file, backup_file)
            print(f"✅ Backup created: {backup_file}")
            return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def main():
    """Main application launcher"""
    clear_screen()
    display_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please install required packages before running the application.")
        sys.exit(1)
    
    # Display current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🕒 Current time: {current_time}")
    
    # Show statistics
    get_app_statistics()
    
    # Check data health
    check_data_health()
    
    # Display feature list
    display_feature_list()
    
    while True:
        print("\n" + "="*60)
        print("🎮 MAIN MENU - Choose your preferred interface:")
        print("="*60)
        print("1. 📟 CLI Version (Keyboard-focused, fast)")
        print("2. 🖥️  GUI Version (Visual, mouse-friendly)")
        print("3. 📊 Show Detailed Statistics")
        print("4. 💾 Create Data Backup")
        print("5. 🛠️  Data Health Check")
        print("6. ❓ Help & About")
        print("7. 🚪 Exit Application")
        print("="*60)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\n🚀 Launching CLI Version...")
            print("💡 Tip: Use numbers for navigation, 'q' to quit sections")
            try:
                from ui import cli
                cli.run_cli()
            except ImportError as e:
                print(f"❌ Error launching CLI: {e}")
                print("💡 Make sure the CLI module is properly installed")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
            
        elif choice == "2":
            print("\n🚀 Launching GUI Version...")
            print("💡 Tip: Double-click tasks to edit, use filters for organization")
            try:
                from ui import gui
                gui.run_gui()
            except ImportError as e:
                print(f"❌ Error launching GUI: {e}")
                print("💡 Make sure tkinter is installed on your system")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
            
        elif choice == "3":
            clear_screen()
            display_banner()
            get_app_statistics()
            check_data_health()
            
        elif choice == "4":
            if backup_data():
                print("✅ Backup completed successfully!")
            else:
                print("❌ Backup failed!")
            input("\nPress Enter to continue...")
            clear_screen()
            display_banner()
            
        elif choice == "5":
            clear_screen()
            display_banner()
            print("\n🔍 Running comprehensive data health check...")
            check_data_health()
            input("\nPress Enter to continue...")
            clear_screen()
            display_banner()
            
        elif choice == "6":
            clear_screen()
            display_banner()
            print("\n📖 ABOUT ADVANCED TO-DO MANAGER v2.0")
            print("="*50)
            print("""
🌟 Features:
• Cross-platform compatibility (Windows, macOS, Linux)
• Dual interface (CLI + GUI)
• Advanced task management with priorities
• Due dates and reminders
• Categories and tags for organization
• Data import/export functionality
• Statistics and progress tracking
• Data backup and recovery

🛠️  Technical Details:
• Built with Python 3.6+
• CLI: Pure Python with rich text interface
• GUI: Tkinter with modern widgets
• Data: JSON-based storage with validation
• Modular architecture for easy extension

📋 System Requirements:
• Python 3.6 or higher
• Tkinter (usually included with Python)
• 50MB free disk space

👨‍💻 Developed with ❤️ for productivity enthusiasts

Press Enter to return to main menu...""")
            input()
            clear_screen()
            display_banner()
            
        elif choice == "7":
            print("\n👋 Thank you for using Advanced To-Do Manager!")
            print("🎯 Stay productive and organized!")
            print("\nGoodbye! 👋")
            break
            
        else:
            print("❌ Invalid choice! Please enter a number between 1-7.")
            input("Press Enter to continue...")
            clear_screen()
            display_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Application interrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please check your installation and try again.")
