import sys
import os

# Ensure the current directory is in the path
sys.path.append(os.getcwd())

from api.app import app

if __name__ == "__main__":
    app.run()
