 # Kayoris 

This Telegram bot is designed to assist with Japanese language studies and enhance productivity through various integrated features. It's a multifunctional bot that integrates language learning tools, long-term memory aids, event management through Google Calendar, weather updates, and more.

## Known bugs
- requirements.txt is not up to date
- Some changes have yet to be pushed

## Features

- **Langchain Custom Tool**: A specialized tool integrated into the bot to assist in Japanese language studies. It offers various functionalities tailored for learners at different levels.

- **Long Term Memory with Pinecone Vector Database**: Utilizes Pinecone's vector database to implement a long-term memory feature, enhancing the learning and retention process.

- **Telegram Handler**: A robust telegram handling feature that manages interactions and ensures smooth communication with users.

- **Google Calendar Integration**: Allows users to access their Google Calendar directly through the bot. Users can view, create, and manage events seamlessly.

- **Weather API Integration**: Provides real-time weather updates. Users can get current weather conditions and forecasts.

- **Wake Up Text**: Sends users a wake-up text combined with a weather report to start the day informed and prepared.

- **Random Messages from Kayoris**: The bot can send random motivational or informative messages from Kayoris, adding an element of surprise and engagement.

- **Whisper Feature with Trigger Word**: Includes a whisper functionality that gets activated by a specific trigger word, enhancing interaction dynamics.

- **Text-to-Speech (TTS)**: Implements TTS capabilities, making the bot more interactive and accessible.

## Getting Started

To get started with this Telegram bot, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourgithubprofile/your-repository-name.git

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up your environment variables:
TELEGRAM_API_KEY: Your Telegram bot API key.
PINECONE_API_KEY: Your Pinecone database API key.
WEATHER_API_KEY: Your API key for the weather service.
GOOGLE_CALENDAR_CREDENTIALS: Your credentials for Google Calendar API.

4. Run Kayoris:
 
  python kayoris.py


To do list:
- Implement langchain custom tool that helps JP studies: Done
- Implement long term memory using pinecone vector database: Done
- Implement telegram handler: Done
- Implement accessing google calendar and create events: Done
- Implement weather api: Done
- Implement wake up text(wakeup text + weather report): Done
- Implement random message from Kayoris: Done 
- Implement Whisper + trigger word: Done
- Implement TTS: Done
 
