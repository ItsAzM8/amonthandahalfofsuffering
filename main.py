import speech_recognition as sr

# prints all available devices in array format
# only used when setting up the mic object
# array = sr.Microphone.list_microphone_names()
# for x in array:
#     print(x)

rec = sr.Recognizer()
# device_index is the index of your microphone
# in the output of the previous array
mic = sr.Microphone(device_index=1)

with mic as source:
    audio = rec.listen(source)
print(rec.recognize_google(audio))



