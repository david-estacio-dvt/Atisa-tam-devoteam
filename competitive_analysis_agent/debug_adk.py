import google.adk
import inspect
import pkgutil

print(f"ADK Path: {google.adk.__path__}")

def find_runner(package):
    if hasattr(package, 'Runner'):
        print(f"Found Runner in {package.__name__}")
        return
    
    if hasattr(package, '__path__'):
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_name = package.__name__ + '.' + name
            try:
                module = __import__(full_name, fromlist=['Runner'])
                if hasattr(module, 'Runner'):
                    print(f"Found Runner in {full_name}")
            except Exception as e:
                pass

find_runner(google.adk)
