import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from config import CHAT_MODEL, PINECONE_ENVIRONMENT, PINECONE_INDEX, EMBEDDING_MODEL
from langchain.agents import initialize_agent, load_tools
from langchain.tools import BaseTool
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from few_shot_exampls import few_shot_examples
from memory_manager import timestamp_to_string
from uuid import uuid4
import time
from langchain.vectorstores import Pinecone
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from functools import wraps
from google_calendar import today_events
import aiohttp
import asyncio
from tts import TTS
import threading
import datetime
import telegram
import random

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
pinecone_key=os.getenv('PINECONE_API_KEY')
whitelist=str(os.getenv('WHITELIST'))
os.environ["OPENWEATHERMAP_API_KEY"]=os.getenv('OPENWEATHERMAP_API_KEY')

pinecone.init(api_key=pinecone_key, environment=PINECONE_ENVIRONMENT)
index = pinecone.Index(PINECONE_INDEX)

open_ai= ChatOpenAI(model_name=CHAT_MODEL, 
                    temperature=0.7)

embed = OpenAIEmbeddings(model=EMBEDDING_MODEL)

with open("Kayoris/Kayoris.txt", "r", encoding="utf-8") as f:
            background = f.read()

prompt = background

message_queue=asyncio.Queue()

class japanese_tutor(BaseTool):
        name='Teaching Japanese'
        description='Use this tool whenever Kayos is typing in Japanese. You will try to catch any grammartical error that the user made, point them out and then response to their input in Japanese'
        
        
        def _run(self, query):
            input_prompt = few_shot_examples + f"\n\nKayos: {query}\nKayoris: "
            
            return input_prompt
        
        async def _arun(self, query):
            raise NotImplementedError("Does not support async")
        
class list_schedule(BaseTool):
        name='List schedule'
        description='Use this tool whenever Kayos ask you to list today schedule.'
        def _run(self, query):
            starts, ends, events = today_events()
            prompt = f"""Using the start time, end time and event, list the events out for Kayos. You can exceed 40 words limit

            Events: {events} and this is their respective start time: {starts} and their respective end time: {ends}

        Kayoris:
"""
            
            return prompt
        
        async def _arun(self, query):
            raise NotImplementedError("Does not support async")

class create_event(BaseTool):
        name='Create event'
        description='Use this tool whenever Kayos want you to create an event on google calendar'
        def _run(self, query):
            llm = ChatOpenAI(temperature=0)
            prompt = f"""Use the following query as information to create an event. The format of the event that you will respond with is: 
            Event, Location, Description, StartTime, EndTime

            Remember that start and end time is always -05:00 and make each of the fields short
            
            For example: Pizza party, Pizza house, Eating Pizza alone sadge, 2023-11-14T09:00:00-05:00, 2023-11-14T11:00:00-05:00

            Query: {query} 
            """
            print(llm.invoke(prompt).content)
            today_events(query=llm.invoke(prompt).content)
            return_prompt = 'You just created an event for Kayoris as asked'
            return return_prompt
        async def _arun(self, query):
            raise NotImplementedError("Does not support async")




class recalling_events(BaseTool):
        name='Recalling Events'
        description='Use this tool whenever Kayos asking you whether you remember a certain events or past conversations. Add the date of the event or conversations to your response.'
        
        
        def _run(self, query):
            vectorstore = Pinecone(
                  index, embed.embed_query, 'conversation'
            )
            results = vectorstore.similarity_search(query)
            source_knowledge = "\n".join([x.page_content for x in results])
            augmented_prompt =  f"""Using the context and your personality below to answer Kayos

        Contexts:
        {source_knowledge}

        Kayos:
        {query}

        Kayoris:
"""

            return augmented_prompt 
        
        async def _arun(self, query):
            raise NotImplementedError("Does not support async")

tools = load_tools(
        ["openweathermap-api"],
        llm=open_ai
)
tools.append(japanese_tutor())
tools.append(recalling_events())
tools.append(list_schedule())
tools.append(create_event())
chat_memory = ConversationBufferMemory(llm=open_ai, memory_key='chat_history', human_prefix='Kayos', ai_prefix='Kayoris')

kayoris = initialize_agent(
        agent='conversational-react-description',
        tools=tools,
        llm=open_ai,
        verbose=True,
        max_iterations=3,
        early_stopping_method='generate',
        memory=chat_memory
)
new_prompt = kayoris.agent.create_prompt(
    prefix=prompt,
    tools=tools
)

kayoris.agent.llm_chain.prompt = new_prompt

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if str(user_id) not in whitelist:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped



@restricted
async def query(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = kayoris(update.message.text)['output'].replace("```", "")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        TTS(text)
        with open('output_audio.wav', 'rb') as audio_file:
                await context.bot.send_voice(update.message.chat_id, voice=audio_file)

@restricted
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
       await context.application.stop()

@restricted
async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
        history = kayoris.memory.buffer
        unique_id = str(uuid4())
        timestamp = time.time()
        timestring = timestamp_to_string(timestamp)
        embeds = embed.embed_documents(history)
        metadata = [
        {
                'date': timestring,
                'conversation': f"On {timestring}, {history}"
        }
        ]
        index.upsert(vectors=zip(unique_id, embeds, metadata))

@restricted
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):     
        voice_file = update.message.voice
        voice_file = update.message.voice

        # Get the file object
        new_file = await context.bot.get_file(voice_file.file_id)

        # Use aiohttp to download the file
        async with aiohttp.ClientSession() as session:
                async with session.get(new_file.file_path) as resp:
                        if resp.status == 200:
                                with open('voice_message.ogg', 'wb') as f:
                                        f.write(await resp.read())

        client = OpenAI()

        audio_file=open("voice_message.ogg", "rb")
        transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
        )
        chat_id = update.message.chat_id
        await context.bot.send_message(chat_id, text=f"Kayos: {transcript}", reply_to_message_id=update.message.message_id)

        text = kayoris(transcript)['output'].replace("```", "")
        TTS(text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        with open('output_audio.wav', 'rb') as audio_file:
                await context.bot.send_voice(chat_id, voice=audio_file)

async def send(chat, msg):
    await telegram.Bot(os.getenv('TELEGRAM_BOT_TOKEN')).sendMessage(chat_id=chat, text=msg) 


def auto_message():
        while True:
                time.sleep(1)
                current_time = datetime.datetime.now().strftime("%H:%M")
                if current_time == "04:00":
                        response = kayoris("It is currently 6:00 AM in the morning. Wake Kayos up and show him the weather in Worcester today")["output"]
                        asyncio.run(send(str(os.getenv('WHITELIST')), response))
                if int(current_time.split(':')[0]) < 21:
                        delay = random.randint(3600, 10800)
                        time.sleep(delay)
                        response = kayoris("Think of something interesting and message to Kayos. It is like you are initiating a conversation with Kayos")["output"]
                        asyncio.run(send(str(os.getenv('WHITELIST')), response))


if __name__ == "__main__":
        application = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
        application.add_handler(CommandHandler('save', save))     
        application.add_handler(MessageHandler(filters.TEXT & (~ filters.COMMAND), query))
        application.add_handler(MessageHandler(filters.VOICE, handle_voice))
        threading.Thread(target=auto_message, args=()).start()
        application.run_polling()