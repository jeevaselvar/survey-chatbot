# Interactive Survey Chatbot

An intelligent chatbot designed to collect survey data through conversational interactions. This solution achieves much higher engagement rates compared to traditional form-based surveys.

## Features

- **Conversational Interface**: Engages users in natural dialogue to collect survey responses
- **Customizable Survey Flow**: Define your own survey questions and flow
- **Beautiful UI**: Modern, responsive interface works on all devices
- **Real-time Response Tracking**: Monitor completion rates and response statistics
- **Data Export**: Save survey results for further analysis
- **Custom Question Support**: Add, edit, and remove questions as needed
- **Theming Options**: Customize the look and feel to match your brand

## Project Structure

```
survey-bot/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   └── index.html
├── intents.json
├── app.py
└── README.md
```

## Installation

1. Clone this repository
2. Install required dependencies:

```bash
pip install flask
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## How It Works

The survey bot uses a conversational flow to guide users through a series of questions. Unlike traditional surveys where users see all questions at once, this approach presents one question at a time in a chat-like interface, making the experience more engaging.

### Components:

1. **Intent Recognition**: The system uses `intents.json` to understand user inputs and generate appropriate responses
2. **Flask Backend**: Handles the conversation flow and stores responses
3. **Interactive UI**: Provides a chat interface where users can interact with the bot
4. **Survey Configuration**: Allows customization of survey questions and flow

## Customizing the Survey

### Editing intents.json

The `intents.json` file defines the conversation flow. Each intent has:

- **tag**: Unique identifier for the intent
- **patterns**: Example phrases that trigger this intent
- **responses**: Possible bot responses

To add a new question to your survey:

1. Create a new intent in `intents.json`
2. Define patterns that will match user responses to the previous question
3. Set responses that will ask your new question
4. Update the `survey_flow` list in `app.py` to include your new intent tag

### Example:

```json
{
  "tag": "product_feedback",
  "patterns": ["yes", "no", "maybe", "sometimes"],
  "responses": ["What improvements would you suggest for our product?"]
}
```

## Deployment

For production deployment, consider:

1. Using a production WSGI server like Gunicorn
2. Setting up a database for response storage (SQLite, PostgreSQL, etc.)
3. Implementing user authentication if needed
4. Setting up proper error handling and logging

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.