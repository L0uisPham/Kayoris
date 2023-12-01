 # Kayoris 

Kayoris is a Telegram bot that is designed to assist with Japanese language studies and enhance productivity through various integrated features. It's a multifunctional bot that integrates language learning tools, long-term memory aids, event management through Google Calendar, weather updates, and more.

![Description](assets/Untitled_5_P1.jpg){width=50%}

## Known bugs
- requirements.txt is not up to date
- Some changes have yet to be pushed

## Features

- **Langchain Custom Tool**: A specialized tool integrated into Kayoris along with promp engineering to assist users in their Japanese language studies.

- **Long Term Memory with Pinecone Vector Database**: Utilizes Pinecone's vector database to implement a long-term memory feature, enhancing the learning and retention process

- **Telegram Handler**: A robust telegram handling feature that manages interactions and ensures smooth communication with users. The user can either text Kayoris or send voice messages and they will receive a response in both text and voice form

- **Google Calendar Integration**: Allows users to access their Google Calendar directly through the Kayoris. Users can view and create events.

- **Weather API Integration**: Provides real-time weather updates using OpenWeatherMap API. Users can get current weather conditions and forecasts.

- **Wake Up Text**: Sends users a wake-up text combined with a weather report to start the day informed and prepared.

- **Random Messages from Kayoris**: Kayoris can send messages at random intervals initiating a conversation with the user

- **Whisper Feature with Trigger Word**: Includes whisper to convert a voice file from telegram to text and pass it to GPT query

- **Text-to-Speech (TTS)**: Implements TTS capabilities, making the bot more interactive and accessible throught the use of Microsoft Azure Speech Studio

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


5. Sample images:
![Description](assets/Screenshot%20from%202023-12-01%2016-42-53.png)
![Description](assets/Screenshot%20from%202023-12-01%2016-43-37.png)
![Description](assets/Screenshot%20from%202023-12-01%2016-45-22.png)
![Description](assets/Screenshot%20from%202023-12-01%2016-45-54.png)
![Description](assets/Screenshot%20from%202023-12-01%2016-47-08.png)
![Description](assets/Screenshot%20from%202023-12-01%2016-48-16-12.png)
![Description](assets/Screenshot%20from%202023-12-01%2016-51-00.png)
![Description](assets/wp9376389.jpg)




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
 
