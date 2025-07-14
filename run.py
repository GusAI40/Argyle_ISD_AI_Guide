#!/usr/bin/env python3
"""
Simple runner script for the Argyle ISD AI Guide
Loads environment variables and starts the Streamlit app
"""

import os
import sys
import subprocess

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("💡 Install python-dotenv to load .env files automatically")

# Check if required environment variables are set
required_vars = ["FIRECRAWL_API_KEY", "OPENAI_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print("❌ Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\nPlease set these variables or create a .env file")
    sys.exit(1)

print("🚀 Starting Argyle ISD AI Guide...")
print("   Visit: http://localhost:8501")
print("   Press Ctrl+C to stop")
print()

# Run the Streamlit app
try:
    subprocess.run(["streamlit", "run", "app.py"], check=True)
except KeyboardInterrupt:
    print("\n👋 Goodbye!")
except subprocess.CalledProcessError as e:
    print(f"❌ Error running app: {e}")
    sys.exit(1) 