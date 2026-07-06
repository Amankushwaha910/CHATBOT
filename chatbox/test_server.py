#!/usr/bin/env python3
import sys
import traceback

try:
    print("📋 Importing server module...")
    from server import ChatServer
    print("✅ Import successful")
    
    print("🚀 Creating ChatServer instance...")
    server = ChatServer()
    print("✅ ChatServer created")
    
    print("🎨 Starting GUI...")
    server.start_gui()
    print("✅ GUI started")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print("\n📋 Full traceback:")
    traceback.print_exc()
    sys.exit(1)
