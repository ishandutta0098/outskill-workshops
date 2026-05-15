"""
Sample code snippets for the workshop.
Each snippet is designed to trigger a different specialist reviewer.
"""

# --- Snippet 1: Security-relevant code (auth, user input, SQL) ---

SECURITY_SNIPPET = '''
import sqlite3

def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"token": username + ":" + password, "role": user[3]}
    return None

def reset_password(request):
    email = request.GET.get("email")
    new_pass = request.GET.get("new_password")
    conn = sqlite3.connect("users.db")
    conn.execute(f"UPDATE users SET password='{new_pass}' WHERE email='{email}'")
    conn.commit()
    conn.close()
    return "Password updated"
'''

# --- Snippet 2: Performance-relevant code (loops, complexity, memory) ---

PERFORMANCE_SNIPPET = '''
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                if items[i] not in duplicates:
                    duplicates.append(items[i])
    return duplicates

def process_large_file(filepath):
    with open(filepath) as f:
        data = f.read()
    lines = data.split("\\n")
    results = []
    for line in lines:
        for other_line in lines:
            if line.strip() == other_line.strip() and line != other_line:
                results.append(line)
    return list(set(results))

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
'''

# --- Snippet 3: Style-relevant code (naming, readability, docs) ---

STYLE_SNIPPET = '''
def f(x,y,z):
    a=x+y
    b=a*z
    if b>100:
        c=b/2
    else:
        c=b*2
    d=[]
    for i in range(int(c)):
        if i%2==0:
            d.append(i)
    return d

class mgr:
    def __init__(s,n,e):
        s.n=n
        s.e=e
        s.data=[]
    def p(s,item):
        s.data.append(item)
    def g(s,idx):
        return s.data[idx]
    def dlt(s,idx):
        del s.data[idx]
'''

# --- Snippet 4: General code for basic review ---

GENERAL_SNIPPET = '''
def calculate_statistics(numbers):
    if not numbers:
        return {}

    total = sum(numbers)
    count = len(numbers)
    mean = total / count

    sorted_nums = sorted(numbers)
    mid = count // 2
    if count % 2 == 0:
        median = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        median = sorted_nums[mid]

    variance = sum((x - mean) ** 2 for x in numbers) / count
    std_dev = variance ** 0.5

    return {
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "min": min(numbers),
        "max": max(numbers),
    }
'''
