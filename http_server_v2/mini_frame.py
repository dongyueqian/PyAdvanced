def register():
    return "======register======"

def login():
    return "======login======"

def logout():
    return "======logout======"

def application(filename):
    if filename == "/register.py":
        return "register success"
    elif filename == "/login.py":
        return "login success"
    elif filename == "/logout.py":
        return "logout success"
    else:
        return "error,not found"