from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

responses = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "hii"],
        "responses": ["Hello!", "Hi there!", "Hey!"]
    },
    "how_are_you": {
        "patterns": ["how are you", "how are you doing"],
        "responses": ["I'm good, thank you for asking!", "I'm doing well, thanks!"]
    },
    "activity": {
        "patterns": ["what are you up to", "what's up", "what are you doing"],
        "responses": ["I'm just chatting with you!", "I'm here to chat with you!"]
    },
    "fun_fact": {
        "patterns": ["fun fact", "tell me something interesting"],
        "responses": ["Sure! Did you know that a group of flamingos is called a flamboyance?"]
    },
    "age": {
        "patterns": ["how old are you", "what's your age"],
        "responses": ["I'm ageless! I exist in the digital realm."]
    },
    "favorite_color": {
        "patterns": ["what's your favorite color", "do you have a favorite color"],
        "responses": ["I don't have a favorite color, but I like all colors!"]
    },
    "music": {
        "patterns": ["do you like music", "what music do you like"],
        "responses": ["I enjoy listening to digital tunes!"]
    },
    "time": {
        "patterns": ["what's the time", "current time"],
        "responses": ["The current time is [current time]."]
    },
    "capital": {
        "patterns": ["what's the capital of France", "capital of France"],
        "responses": ["The capital of France is Paris!"]
    }
}

def message_probability(user_message, recognised_phrases):
    user_message_lower = user_message.lower()
    recognised_phrases_lower = [phrase.lower() for phrase in recognised_phrases]
    for phrase in recognised_phrases_lower:
        if phrase in user_message_lower:
            return 100  # If any recognized phrase is found, return 100% certainty
    return 0  # If no recognized phrase is found, return 0% certainty

def check_all_messages(message):
    highest_prob_list = {}
    
    for intent, data in responses.items():
        prob = message_probability(message, data["patterns"])
        if prob:
            highest_prob_list[intent] = prob
    
    threshold = 50
    matching_responses = {intent: prob for intent, prob in highest_prob_list.items() if prob >= threshold}
    if matching_responses:
        best_match = random.choice(list(matching_responses.keys()))
        return best_match
    else:
        return "default"

def get_response(user_input):
    split_message = user_input.split()  # Split the input message into words
    user_message = ' '.join(split_message)  # Join the list of words into a single string
    response_intent = check_all_messages(user_message)
    
    if response_intent in responses:
        if response_intent == "default":
            return "Sorry, I didn't understand that."
        else:
            return random.choice(responses[response_intent]["responses"])
    else:
        return "Sorry, I didn't understand that."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.form['user_input']
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
