import os
import openai
from dotenv import load_dotenv
from langchain.chains import TransformChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from config import CHAT_MODEL, PINECONE_ENVIRONMENT, PINECONE_INDEX, EMBEDDING_MODEL
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.tools import BaseTool
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from few_shot_exampls import few_shot_examples
from memory_manager import timestamp_to_string, gpt_embeddings
from uuid import uuid4
from time import time
from langchain.vectorstores import Pinecone
from telegram_handler import telegram_handler
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.tools.zapier.tool import ZapierNLARunAction
from functools import wraps
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.callbacks import get_openai_callback
import tiktoken
import torch
import requests
import urllib.parse

import streamlit as st
import logging,sys,os
import openai
from dotenv import load_dotenv
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
from llama_hub.tools.zapier.base import ZapierToolSpec
from openai import OpenAI
import requests, json
import io
import wave
import pyaudio
import time



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Voicevox:
    def __init__(self,host="0.0.0.0",port=50021):
        self.host = host
        self.port = port

    def speak(self,text=None,speaker=3): # VOICEVOX:ナースロボ＿タイプＴ

        params = (
            ("text", text),
            ("speaker", speaker)  # 音声の種類をInt型で指定
        )

        init_q = requests.post(
            f"http://{self.host}:{self.port}/audio_query",
            params=params
        )

        res = requests.post(
            f"http://{self.host}:{self.port}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(init_q.json())
        )

        # メモリ上で展開
        audio = io.BytesIO(res.content)

        with wave.open(audio,'rb') as f:
            # 以下再生用処理
            p = pyaudio.PyAudio()

            def _callback(in_data, frame_count, time_info, status):
                data = f.readframes(frame_count)
                return (data, pyaudio.paContinue)

            stream = p.open(format=p.get_format_from_width(width=f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True,
                            stream_callback=_callback)

            # Voice再生
            stream.start_stream()
            while stream.is_active():
                time.sleep(0.1)

            stream.stop_stream()
            stream.close()
            p.terminate()


def main():
    vv = Voicevox()
    vv.speak(text="""How are you doing today?""")


if __name__ == "__main__":
    main()