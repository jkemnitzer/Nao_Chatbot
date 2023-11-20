__version__ = "0.1.0"

__author__ = "Jonas Kemnitzer"
__email__ = "jonas.kemnitzer.2@hof-university.de"

import qi
import os


class Activity:
    APP_ID = "mini_python3_nao_app"

    def __init__(self, qiapp):
        self.qiapp = qiapp
        self.session = qiapp.session

    def on_start(self):
        import openai

        prompt_recording = self.get_recording()

        client = openai.OpenAI(
            api_key="KEY HERE"
        )

        # Transcribe the recorded file
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=prompt_recording, response_format="text"
        )
        self.session.service("ALTextToSpeech").say(
            "The open ai API detected" + str(transcript)
        )
        
        self.session.service("ALTextToSpeech").say(
            "Processing the information, give me a moment"
        )

        # Generate response from the transcribed tts.wav file here
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Robot of the type Nao, also called Gustav."},
                {"role": "system", "content": "You are short and precise, try also to be funny."},
                {"role": "user", "content": transcript},
            ],
        )
        answer = response.choices[0].message.content

        self.say(answer)
        self.stop()


    def stop(self):
        self.qiapp.stop()

    def say(self, answer):
        self.session.service("ALTextToSpeech").say(str(answer))

    def get_recording(self):
        path = os.path.expanduser("~") + "/recordings/microphones/tts.wav"
        return open(path, "rb")


if __name__ == "__main__":
    qiapp = qi.Application()
    qiapp.start()
    activity = Activity(qiapp)   
    qi.runAsync(activity.on_start)
    qiapp.run()