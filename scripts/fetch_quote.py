#!/usr/bin/env python3
"""Fetch daily programming/motivational quote."""

import json
import os
from datetime import datetime
import requests
import random

# Fallback quotes if API fails
FALLBACK_QUOTES = [
    {"text": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House"},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"text": "Experience is the name everyone gives to their mistakes.", "author": "Oscar Wilde"},
    {"text": "The only way to learn a new programming language is by writing programs in it.", "author": "Dennis Ritchie"},
    {"text": "Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday's code.", "author": "Dan Salomon"},
    {"text": "Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away.", "author": "Antoine de Saint-Exupery"},
    {"text": "Code never lies, comments sometimes do.", "author": "Ron Jeffries"},
    {"text": "Simplicity is the soul of efficiency.", "author": "Austin Freeman"},
    {"text": "Make it work, make it right, make it fast.", "author": "Kent Beck"},
    {"text": "Programming isn't about what you know; it's about what you can figure out.", "author": "Chris Pine"},
    {"text": "The best error message is the one that never shows up.", "author": "Thomas Fuchs"},
    {"text": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler"},
    {"text": "Programming is the art of algorithm design and the craft of debugging errant code.", "author": "Ellen Ullman"},
    {"text": "Walking on water and developing software from a specification are easy if both are frozen.", "author": "Edward V. Berard"},
    {"text": "The most disastrous thing that you can ever learn is your first programming language.", "author": "Alan Kay"},
    {"text": "Debugging is twice as hard as writing the code in the first place.", "author": "Brian Kernighan"},
    {"text": "It's not a bug – it's an undocumented feature.", "author": "Anonymous"},
    {"text": "In order to understand recursion, one must first understand recursion.", "author": "Anonymous"},
    {"text": "Talk is cheap. Show me the code.", "author": "Linus Torvalds"},
    {"text": "Programs must be written for people to read, and only incidentally for machines to execute.", "author": "Harold Abelson"},
    {"text": "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live.", "author": "John Woods"},
    {"text": "A language that doesn't affect the way you think about programming is not worth knowing.", "author": "Alan Perlis"},
    {"text": "Before software can be reusable it first has to be usable.", "author": "Ralph Johnson"},
    {"text": "The computer was born to solve problems that did not exist before.", "author": "Bill Gates"},
    {"text": "Software is a great combination between artistry and engineering.", "author": "Bill Gates"},
    {"text": "Truth can only be found in one place: the code.", "author": "Robert C. Martin"},
    {"text": "Give a man a program, frustrate him for a day. Teach a man to program, frustrate him for a lifetime.", "author": "Muhammad Waseem"},
    {"text": "When debugging, novices insert corrective code; experts remove defective code.", "author": "Richard Pattis"},
    {"text": "If debugging is the process of removing software bugs, then programming must be the process of putting them in.", "author": "Edsger Dijkstra"},
    {"text": "One of my most productive days was throwing away 1000 lines of code.", "author": "Ken Thompson"},
]

def fetch_quote():
    """Fetch a quote, with fallback to local quotes."""
    
    quote = None
    
    # Try ZenQuotes API
    try:
        resp = requests.get('https://zenquotes.io/api/random', timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data and len(data) > 0:
                quote = {
                    'text': data[0].get('q', ''),
                    'author': data[0].get('a', 'Unknown')
                }
    except:
        pass
    
    # Fallback to programming quotes
    if not quote or not quote.get('text'):
        # Use day of year as seed for consistent daily quote
        day_of_year = datetime.now().timetuple().tm_yday
        quote = FALLBACK_QUOTES[day_of_year % len(FALLBACK_QUOTES)]
    
    quote_data = {
        'updated_at': datetime.utcnow().isoformat() + 'Z',
        'quote': quote['text'],
        'author': quote['author'],
        'category': 'programming'
    }
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    with open('data/quote.json', 'w') as f:
        json.dump(quote_data, f, indent=2)
    
    print(f"✅ Quote of the day:")
    print(f'   "{quote["text"]}"')
    print(f"   — {quote['author']}")

if __name__ == '__main__':
    fetch_quote()
