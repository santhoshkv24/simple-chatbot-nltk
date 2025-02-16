import nltk
from nltk.chat.util import Chat, reflections

# Download NLTK data (only needed once)
nltk.download("punkt")

# Pre-defined patterns and responses
pairs = [
    [
        r"hi|hello|hey",
        ["Hello! How can I help you?", "Hi there! What can I do for you?"]
    ],
    [
        r"how are you?",
        ["I'm just a bot, but I'm doing great! How about you?",]
    ],
    [
        r"what is your name?",
        ["I'm a chatbot. You can call me ChatGPT!",]
    ],
    [
        r"bye|goodbye",
        ["Goodbye! Have a great day!", "Bye! See you soon!"]
    ],
    [
        r"what can you do?",
        ["I can chat with you, answer simple questions, and help you learn about chatbots!",]
    ],
    [
        r"tell me a joke",
        ["Why don't scientists trust atoms? Because they make up everything!",]
    ],
    [
        r"thank you|thanks",
        ["You're welcome!", "No problem!", "Happy to help!"]
    ],
    [
        r"default",
        ["I'm not sure I understand. Can you rephrase that?",]
    ]
]

# Create a chatbot
chatbot = Chat(pairs, reflections)

# Function to start the chat
def start_chat():
    print("Hello! I'm your chatbot. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "goodbye"]:
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = chatbot.respond(user_input)
        print(f"Chatbot: {response}")

# Run the chatbot
if __name__ == "__main__":
    start_chat()
