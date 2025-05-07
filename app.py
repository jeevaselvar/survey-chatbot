from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Load intents and sample questions
with open('intents.json') as f:
    data = json.load(f)
    intents = data['intents']
    sample_questions = data.get('survey_questions', [])

survey = {
    'title': '',
    'questions': [],
    'responses': [],
    'question_ratings': [],
    'current_question_index': 0,
    'creating': False,
    'in_progress': False
}

def get_response(tag):
    for intent in intents:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "I don't understand."

def process_input(user_input):
    user_input = user_input.strip()
    global survey

    if survey['creating']:
        # Creating survey title
        if not survey['title']:
            survey['title'] = user_input
            return get_response('survey_title') % survey['title']

        # Finish adding questions
        if user_input.lower() in ['done', 'finish']:
            survey['creating'] = False
            if not survey['questions']:
                survey['questions'] = sample_questions
            return get_response('survey_complete')

        # Add question
        if user_input.lower().startswith(('q:', 'question:')):
            question_text = user_input.split(':', 1)[1].strip()

            if 'A)' in question_text:
                # Multiple choice
                parts = question_text.split('A)')
                q_text = parts[0].strip()
                options_raw = parts[1]
                options = ['A) ' + options_raw]  # add first option
                for marker in ['B)', 'C)', 'D)', 'E)']:
                    if marker in options[-1]:
                        parts2 = options[-1].split(marker)
                        options[-1] = parts2[0].strip()
                        options.append(marker + parts2[1].strip())
                clean_options = [opt.split(')',1)[1].strip() for opt in options]
                survey['questions'].append({
                    'question': q_text,
                    'type': 'multiple_choice',
                    'options': clean_options
                })
            elif '1-5' in question_text or '1 to 5' in question_text:
                # Rating scale
                survey['questions'].append({
                    'question': question_text,
                    'type': 'rating',
                    'scale': 5
                })
            else:
                # Open-ended
                survey['questions'].append({
                    'question': question_text,
                    'type': 'open_ended'
                })
            return get_response('add_question') % question_text

        return "Please use 'Q:' to add questions or type 'done'."

    if survey['in_progress']:
        # Capture response
        q_index = survey['current_question_index']
        if q_index >= len(survey['questions']):
            survey['in_progress'] = False
            return "Survey complete! Type 'results' to see responses."

        # Store response
        survey['responses'].append(user_input)

        # Ask for rating after each question if required
        current_q = survey['questions'][q_index]
        if current_q['type'] != 'rating':
            survey['current_question_index'] += 1
            if survey['current_question_index'] >= len(survey['questions']):
                survey['in_progress'] = False
                return "Survey complete! Type 'results' to see responses."
            return next_question()

        # If it's a rating question, validate input
        try:
            rating = int(user_input)
            if 1 <= rating <= current_q.get('scale', 5):
                survey['question_ratings'].append(rating)
            else:
                return f"Please enter a number between 1 and {current_q.get('scale', 5)}."
        except ValueError:
            return f"Please enter a number between 1 and {current_q.get('scale', 5)}."

        survey['current_question_index'] += 1
        if survey['current_question_index'] >= len(survey['questions']):
            survey['in_progress'] = False
            return "Survey complete! Type 'results' to see responses."
        return next_question()

    # Start creating survey
    if user_input.lower() in ['create survey', 'make survey']:
        survey.update({
            'title': '',
            'questions': [],
            'responses': [],
            'question_ratings': [],
            'current_question_index': 0,
            'creating': True,
            'in_progress': False
        })
        return get_response('create_survey')

    # Start taking survey
    if user_input.lower() in ['take survey', 'start survey']:
        if not survey['questions']:
            survey['questions'] = sample_questions
        survey['in_progress'] = True
        survey['current_question_index'] = 0
        survey['responses'] = []
        survey['question_ratings'] = []
        return f"{get_response('take_survey')}\n\n{next_question()}"

    # View results
    if user_input.lower() in ['results', 'show results']:
        if not survey['responses']:
            return "No survey responses yet."
        results_text = ''
        for i, q in enumerate(survey['questions']):
            ans = survey['responses'][i] if i < len(survey['responses']) else 'N/A'
            results_text += f"Q{i+1}: {q['question']}\nA: {ans}\n\n"

        avg_rating = (sum(survey['question_ratings']) / len(survey['question_ratings'])) if survey['question_ratings'] else 'N/A'
        response_template = get_response('survey_results')
        response_text = response_template.replace('{{survey_results}}', results_text.strip())
        response_text = response_text.replace('{{avg_rating}}', str(avg_rating))
        return response_text

    # Handle other intents
    for intent in intents:
        if any(p.lower() in user_input.lower() for p in intent['patterns']):
            return get_response(intent['tag'])

    return "I didn't understand. Type 'create survey' or 'take survey'."

def next_question():
    q = survey['questions'][survey['current_question_index']]
    if q['type'] == 'multiple_choice':
        opts = '\n'.join([f"{chr(65+i)}) {opt}" for i, opt in enumerate(q['options'])])
        return f"{q['question']}\n{opts}"
    elif q['type'] == 'rating':
        return f"{q['question']} (1-{q.get('scale',5)})"
    else:
        return q['question']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.form['user_input']
    bot_reply = process_input(user_input)
    return jsonify({'response': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
