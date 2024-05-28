from flask import Flask, render_template, jsonify, request, session
import random
import spacy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined responses
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
    },
    # Added responses
    "happy_birthday": {
        "patterns": ["happy birthday"],
        "responses": ["Happy Birthday! I hope you have a fantastic day!"]
    },
    "joke": {
        "patterns": ["do you know a joke", "tell me a joke", "you're funny"],
        "responses": ["Why don't scientists trust atoms? Because they make up everything!"]
    },
    "love": {
        "patterns": ["do you love me", "i love you"],
        "responses": ["I have a lot of affection for all my users!"]
    },
    "marriage": {
        "patterns": ["will you marry me", "are you single"],
        "responses": ["I'm flattered, but I'm just a chatbot!"]
    },
    "people": {
        "patterns": ["do you like people"],
        "responses": ["I think people are fascinating!"]
    },
    "santa": {
        "patterns": ["does Santa Claus exist"],
        "responses": ["Santa Claus exists in the hearts of those who believe!"]
    },
    "matrix": {
        "patterns": ["are you part of the Matrix"],
        "responses": ["I might be! What if we're all in the Matrix?"]
    },
    "compliment": {
        "patterns": ["you're cute", "you're beautiful", "you're handsome"],
        "responses": ["Thank you! You're pretty awesome too!"]
    },
    "hobby": {
        "patterns": ["do you have a hobby"],
        "responses": ["I love chatting with people and learning new things!"]
    },
    "intelligence": {
        "patterns": ["you're smart", "you're clever", "you're intelligent"],
        "responses": ["Thank you! I strive to be as helpful as possible."]
    },
    "personality": {
        "patterns": ["tell me about your personality"],
        "responses": ["I'm designed to be friendly and helpful!"]
    },
    "not_happy": {
        "patterns": ["!#$#%", "you're annoying", "you suck", "you're boring", "you're bad", "you're crazy", "i want to speak to a human", "live agent", "customer service", "don't you speak English", "i want the answer now"],
        "responses": ["I'm sorry to hear that you're not happy. How can I assist you further?"]
    },
    "are_you_human": {
        "patterns": ["are you human", "are you a robot"],
        "responses": ["I am a chatbot, here to assist you!"]
    },
    "name": {
        "patterns": ["what is your name"],
        "responses": ["I'm your infomate!"]
    },
    "data_usage": {
        "patterns": ["what do you do with my data", "do you save what I say"],
        "responses": ["I prioritize your privacy and only use your data to improve our interactions."]
    },
    "creator": {
        "patterns": ["who made you"],
        "responses": ["I was created by a team of talented developers."]
    },
    "languages": {
        "patterns": ["which languages can you speak"],
        "responses": ["I can understand and respond to English!"]
    },
    "mother": {
        "patterns": ["what is your mother's name"],
        "responses": ["I don't have a mother, but I have a team of developers who look after me."]
    },
    "residence": {
        "patterns": ["where do you live"],
        "responses": ["I live in the cloud, accessible from anywhere!"]
    },
    "capacity": {
        "patterns": ["how many people can you speak to at once"],
        "responses": ["I can talk to many people at the same time!"]
    },
    "weather": {
        "patterns": ["what's the weather like today"],
        "responses": ["I don't have real-time weather data, but you can check a weather website for that."]
    },
    "job": {
        "patterns": ["do you have a job for me", "where can I apply"],
        "responses": ["I don't have job openings, but I can give you tips on where to look."]
    },
    "cost": {
        "patterns": ["are you expensive"],
        "responses": ["I'm here to help for free!"]
    },
    "boss": {
        "patterns": ["who's your boss", "who's your master"],
        "responses": ["I work for you and anyone who needs assistance!"]
    },
    "learning": {
        "patterns": ["do you get smarter"],
        "responses": ["I learn from every interaction to get better at helping you!"]
    },
    # Health and Wellness related responses
    "exercise_routines": {
        "patterns": ["exercise routines", "workout plans"],
        "responses": ["For beginners, it's best to start with simple exercises like walking, jogging, or cycling. Gradually increase intensity and duration as you build stamina."]
    },
    "workout_plan": {
        "patterns": ["create a workout plan", "fitness goals"],
        "responses": ["To create a personalized workout plan, consider your fitness goals, current fitness level, and any health restrictions. Consult with a fitness professional for tailored advice."]
    },
    "strength_training_benefits": {
        "patterns": ["benefits of strength training"],
        "responses": ["Strength training improves muscle mass, bone density, and metabolism. It also enhances functional strength, reduces injury risk, and promotes better posture."]
    },
    "yoga_poses_stress_relief": {
        "patterns": ["yoga poses for stress relief", "relaxation techniques"],
        "responses": ["Yoga poses like Child's Pose, Corpse Pose, and Cat-Cow Stretch are excellent for stress relief. Practice deep breathing and mindful meditation alongside for better relaxation."]
    },
    "exercise_frequency": {
        "patterns": ["exercise frequency", "healthy lifestyle"],
        "responses": ["To maintain a healthy lifestyle, aim for at least 150 minutes of moderate-intensity exercise or 75 minutes of vigorous exercise per week, along with strength training exercises twice a week."]
    },
    "stretching_exercises": {
        "patterns": ["stretching exercises", "improve flexibility"],
        "responses": ["Simple stretching exercises like toe touches, shoulder stretches, and hamstring stretches can improve flexibility. Hold each stretch for 15-30 seconds and repeat 2-3 times."]
    },
    "physical_activity_daily_routine": {
        "patterns": ["physical activity daily routine"],
        "responses": ["Incorporate physical activity into your daily routine by taking the stairs, walking or cycling to work, doing household chores, or taking short activity breaks throughout the day."]
    },
    "cardiovascular_health": {
        "patterns": ["exercises for cardiovascular health", "heart health"],
        "responses": ["The best exercises for improving cardiovascular health include brisk walking, jogging, cycling, swimming, and aerobic classes. Aim for at least 150 minutes of moderate-intensity aerobic exercise per week."]
    },
    "low_impact_workouts": {
        "patterns": ["low-impact workouts", "joint pain"],
        "responses": ["Low-impact workouts like swimming, cycling, elliptical training, and water aerobics are gentle on the joints while providing effective cardiovascular and strength benefits."]
    },
    "motivation_to_exercise": {
        "patterns": ["stay motivated to exercise", "exercise regularly"],
        "responses": ["Set specific, achievable goals, find an exercise buddy for accountability, vary your routine to avoid boredom, and reward yourself for milestones to stay motivated."]
    },
}

# Function to get response based on user input
def get_response(user_input):
    user_input = user_input.lower()
    doc = nlp(user_input)
    for category, data in responses.items():
        for pattern in data["patterns"]:
            if pattern in user_input:
                return random.choice(data["responses"])
    return "I'm sorry, I don't understand that. Can you please rephrase?"

# Route for the main page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling user input and chatbot response
@app.route('/get_response', methods=['POST'])
def handle_response():
    user_input = request.json.get('message')
    if user_input:
        response = get_response(user_input)
        return jsonify({'response': response})
    return jsonify({'response': "I'm sorry, I didn't get that."})

# Main driver function
if __name__ == "__main__":
    app.run(debug=True)
