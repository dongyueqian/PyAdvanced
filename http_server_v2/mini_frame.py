def register():
    return "======index======"

def login():
    return "======login======"

def logout():
    return "======center======"

def application(filename):
    if filename == "/index.py":
        return "index success"
    elif filename == "/login.py":
        return "login success"
    elif filename == "/center.py":
        return "center success"
    else:
        return "error,not found"