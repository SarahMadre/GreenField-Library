# db.py

# USERS DATABASE
users = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "email": "admin@greenfield.edu"
    },
    "staff1": {
        "password": "staff123",
        "role": "staff",
        "email": "staff@greenfield.edu"
    }
}

# BOOKS DATABASE
books = {
    1: {
        "id": 1,
        "title": "Discrete Mathematics",
        "subject": "Mathematics",
        "available": True
    },
    2: {
        "id": 2,
        "title": "English Grammar Essentials",
        "subject": "English",
        "available": False
    }
}

# BOOK REQUESTS
requests = []

book_counter = 3
request_counter = 1
