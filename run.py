#!/usr/bin/env python3
import os
import subprocess
import sys

# Get port from environment or use default
port = os.environ.get('PORT', '8501')

# Ensure port is valid
try:
    port_int = int(port)
except ValueError:
    port = '8501'

print(f"Starting Streamlit on port {port}")

# Run streamlit
cmd = [
    sys.executable, '-m', 'streamlit', 'run', 'app.py',
    '--server.port', port,
    '--server.address', '0.0.0.0',
    '--server.headless', 'true'
]

subprocess.run(cmd)