#!/usr/bin/env python3
"""
Production deployment script for Interview Tracker
Cross-platform compatible (Windows/Linux)
"""

import os
import sys
import platform

def main():
    """Run the application on port 2699"""
    
    # Environment variables
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_APP'] = 'app.py'
    
    # Platform detection
    current_platform = platform.system()
    print(f"Platform detected: {current_platform}")
    print("Starting Interview Tracker on port 2699...")
    print("Access at: http://127.0.0.1:2699")
    print("=" * 50)
    
    try:
        # Import and run Flask app directly
        from app import app
        
        # Run on port 2699
        app.run(
            host='0.0.0.0',
            port=2699,
            debug=False
        )
        
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
