import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os


def TTS(tts):
    pitch = "+25.00%"  
    rate = "-10.00%"
    audio_output = speechsdk.audio.AudioOutputConfig(filename="output_audio.wav")

    ssml_template = """
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
        <voice name="en-US-RyanMultilingualNeural">    
            <prosody rate="{rate}" volume="soft" pitch="{pitch}" contour="(0%,-30Hz) (50%,-10Hz) (100%,+20Hz)" >
                {text}
            </prosody>
        </voice>
    </speak>
    """

    ssml = ssml_template.format(pitch=pitch, rate=rate, text=tts)

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = os.getenv('AZURE_TOKEN')
    service_region = "eastus"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "en-US-RyanMultilingualNeural"



    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    result = speech_synthesizer.speak_ssml_async(ssml).get()

