from vosk import Model, KaldiRecognizer
import os
import json
import pyaudio

RATE = 44100

if not os.path.exists("model"):
    print("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack "
          "as 'model' in the current folder. For this project, vosk-model-en-us-daanzu is recommended")
    exit(1)


model = Model("model")
rec = KaldiRecognizer(model, RATE)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=8000)
stream.start_stream()

while True:
    data = stream.read(4000)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        print(result["text"])
