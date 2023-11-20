__version__ = "0.1.0"

__author__ = "Jonas Kemnitzer"
__email__ = "jonas.kemnitzer.2@hof-university.de"
__status__ = "Development"

import qi
import os


class Activity:
    """
    Represents an activity that interacts with the OpenAI API.

    Attributes:
        APP_ID (str): The ID of the mini_python3_nao_app.
        qiapp (object): The qiapp object.
        session (object): The session object.
    """

    APP_ID = "mini_python3_nao_app"

    def __init__(self, qiapp):
        """
        Initializes a new instance of the Activity class.

        Args:
            qiapp (object): The qiapp object.
        """
        self.qiapp = qiapp
        self.session = qiapp.session

    def on_start(self):
        """
        Executes the activity when it starts.
        """
        import openai

        prompt_recording = self.get_recording()

        client = openai.OpenAI(api_key="KEY HERE")

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
                {
                    "role": "system",
                    "content": "You are a Robot of the type Nao, also called Gustav.",
                },
                {
                    "role": "system",
                    "content": "You are short and precise, try also to be funny.",
                },
                {"role": "user", "content": transcript},
            ],
        )
        answer = response.choices[0].message.content

        self.say(answer)
        self.stop()

    def stop(self):
        """
        Stops the activity.
        """
        self.qiapp.stop()

    def say(self, answer):
        """
        Says the given answer using ALTextToSpeech.

        Args:
            answer (str): The answer to be spoken.
        """
        self.session.service("ALTextToSpeech").say(str(answer))

    def get_recording(self):
        """
        Retrieves the recording file.

        Returns:
            file: The recording file.
        """
        path = os.path.expanduser("~") + "/recordings/microphones/tts.wav"
        return open(path, "rb")


if __name__ == "__main__":
    qiapp = qi.Application()
    qiapp.start()
    activity = Activity(qiapp)
    qi.runAsync(activity.on_start)
    qiapp.run()
