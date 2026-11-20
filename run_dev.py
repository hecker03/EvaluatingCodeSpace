#!/usr/bin/env python3
"""
Development server runner with enhanced auto-reload functionality.
Run this instead of app.py for better development experience.
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set environment variables for development
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    print("🚀 Starting Flask development server with auto-reload...")
    print("📁 Watching for file changes in:")
    print(f"   - {os.getcwd()}")
    print("🔄 Auto-reload enabled - changes will be picked up automatically!")
    print("🌐 Server will be available at: http://127.0.0.1:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(
            debug=True,
            use_reloader=True,
            threaded=True,
            host='127.0.0.1',
            port=5000,
            extra_files=[
                # Watch these additional files for changes
                'config.py',
                'forms.py',
                'extensions.py',
                'models/',
                'routes/',
                'templates/',
                'static/'
            ]
        )
    except KeyboardInterrupt:
        print("\n👋 Development server stopped!")
        sys.exit(0)
