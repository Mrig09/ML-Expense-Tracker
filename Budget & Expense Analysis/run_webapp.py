#!/usr/bin/env python3
"""
Launcher script for the Budget & Expense Analysis Web App
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit web app"""
    print("🚀 Launching Budget & Expense Analysis Web App...")
    print("📱 Opening in your default web browser...")
    print("🔄 The app will automatically reload when you make changes")
    print("⏹️  Press Ctrl+C to stop the app")
    print("\n" + "="*50)
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Web app stopped. Thanks for using Budget & Expense Analysis!")
    except Exception as e:
        print(f"\n❌ Error launching web app: {e}")
        print("💡 Make sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()
