import google.adk.runners
import os

path = google.adk.runners.__file__
print(f"Path: {path}")
with open("runners_path.txt", "w") as f:
    f.write(path)
