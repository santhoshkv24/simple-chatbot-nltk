import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import random

# Initialize NLTK
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# User memory system
user_profile = {
    'name': None,
    'favorites': {
        'food': None,
        'music': None,
        'movie': None,
        'book': None,
        'hobby': None
    },
    'last_topic': None
}

# Enhanced response database
RESPONSES = {
    'greetings': [
        "Hello! How can I help you today?",
        "Hi there! What would you like to talk about?",
        "Greetings! Tell me something about yourself."
    ],
    'name': [
        "Nice to meet you, {name}!",
        "Hello, {name}! What's on your mind today?",
        "Got it, {name}! Ask me anything."
    ],
    'favorites': {
        'food': [
            "I remember you like {food}! That's one of my favorites too.",
            "Ah yes, you mentioned you enjoy {food}. Great taste!",
            "{food}? Excellent choice!"
        ],
        'music': [
            "Your music taste ({music}) is awesome!",
            "I won't forget you're into {music} music.",
            "{music} really gets you going, doesn't it?"
        ],
        'movie': [
            "I remember you like {movie} movies!",
            "Ah yes, you mentioned {movie} films.",
            "{movie} movies are great choices!"
        ],
        'hobby': [
            "I recall you enjoy {hobby}!",
            "Yes, you told me about your interest in {hobby}.",
            "Your hobby of {hobby} sounds fascinating!"
        ]
    },
    'topics': {
        'food': [
            "I love talking about food! What's your favorite cuisine?",
            "Food is life! Do you prefer cooking or eating out?",
            "Tell me about the best meal you've ever had."
        ],
        'music': [
            "Music is magical! What artists do you listen to most?",
            "Do you play any instruments or just enjoy listening?",
            "What's your go-to song when you need energy?"
        ],
        'movie': [
            "Movies are awesome! What genre do you prefer?",
            "Who's your favorite director or actor?",
            "Tell me about a movie that changed your perspective."
        ],
        'hobby': [
            "Hobbies make life interesting! How did you get into {hobby}?",
            "What do you enjoy most about {hobby}?",
            "How often do you get to practice {hobby}?"
        ],
        'default': [
            "That's interesting! Tell me more.",
            "I'd love to hear more about that.",
            "What else would you like to share about this?"
        ]
    },
    'fallbacks': [
        "I'm not quite sure I understand. Could you rephrase that?",
        "That's an interesting point. Let's talk about something else?",
        "I'm still learning. Could you explain that differently?"
    ]
}

def preprocess(text):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(word) for word in tokens 
            if word.isalnum() and word not in stop_words]

def remember_details(original_text):
    text_lower = original_text.lower()
    
    # Improved name detection
    if not user_profile['name']:
        if "my name is" in text_lower:
            name = original_text.split("is")[-1].strip()
            user_profile['name'] = name.capitalize()
            return random.choice(RESPONSES['name']).format(name=user_profile['name'])
        elif "i am" in text_lower:
            name = original_text.split("am")[-1].strip()
            user_profile['name'] = name.capitalize()
            return random.choice(RESPONSES['name']).format(name=user_profile['name'])
        elif len(original_text.split()) == 1 and original_text[0].isupper():
            user_profile['name'] = original_text.strip()
            return random.choice(RESPONSES['name']).format(name=user_profile['name'])
    
    # Favorite detection
    tokens = preprocess(original_text)
    if "favorite" in tokens or "like" in tokens or "love" in tokens:
        for category in user_profile['favorites']:
            if category in tokens:
                # Extract the value after the category word
                words = original_text.lower().split(category)
                if len(words) > 1:
                    value = words[1].strip()
                    if value.startswith('is '):
                        value = value[3:].strip()
                    if value.startswith('are '):
                        value = value[4:].strip()
                    user_profile['favorites'][category] = value.capitalize()
                    user_profile['last_topic'] = category
                    return f"I'll remember you love {user_profile['favorites'][category]} when it comes to {category}!"
    
    return None

def generate_response(user_input):
    original_text = user_input.strip()
    
    # First check for remembered details
    memory_response = remember_details(original_text)
    if memory_response:
        return memory_response
    
    tokens = preprocess(original_text)
    
    # Check for greetings
    if any(word in tokens for word in ["hi", "hello", "hey", "greetings"]):
        if user_profile['name']:
            return f"Hi {user_profile['name']}! {random.choice(RESPONSES['greetings'])}"
        return random.choice(RESPONSES['greetings'])
    
    # Check queries about remembered info
    if "my name" in original_text.lower():
        if user_profile['name']:
            return f"Your name is {user_profile['name']}, right?"
        return "You haven't told me your name yet. What should I call you?"
    
    # Handle favorite topics
    for category in user_profile['favorites']:
        if category in tokens:
            if user_profile['favorites'][category]:
                return random.choice(RESPONSES['favorites'][category]).format(**{category: user_profile['favorites'][category]})
            return random.choice(RESPONSES['topics'][category])
    
    # Continue last topic
    if user_profile['last_topic']:
        if user_profile['favorites'][user_profile['last_topic']]:
            return random.choice(RESPONSES['topics'][user_profile['last_topic']])
    
    # Fallback
    return random.choice(RESPONSES['fallbacks'])

def chat():
    print("ChatBot: Hi! I'm your personal chatbot with memory. What's your name?")
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["bye", "goodbye", "exit", "quit"]:
                closing = f"Goodbye{', ' + user_profile['name'] if user_profile['name'] else ''}! It was wonderful talking to you!"
                print(f"ChatBot: {closing}")
                break
            response = generate_response(user_input)
            print(f"ChatBot: {response}")
        except KeyboardInterrupt:
            print("\nChatBot: Goodbye!")
            break

if __name__ == "__main__":
    chat()