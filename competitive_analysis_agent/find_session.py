import google.adk
import pkgutil

def find_class(package, specific_class):
    if hasattr(package, specific_class):
        print(f"Found {specific_class} in {package.__name__}")
        return
    
    if hasattr(package, '__path__'):
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_name = package.__name__ + '.' + name
            try:
                module = __import__(full_name, fromlist=[specific_class])
                if hasattr(module, specific_class):
                    print(f"Found {specific_class} in {full_name}")
            except Exception:
                pass

find_class(google.adk, 'InMemorySessionService')
find_class(google.adk, 'SessionService')
