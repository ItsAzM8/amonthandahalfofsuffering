import tkinter as tk
from tkinter import ttk

import os

from vosk import Model, KaldiRecognizer
import json
import pyaudio

import threading

RATE = 16000

p = pyaudio.PyAudio()
model = Model("modelBig")
rec = KaldiRecognizer(model, RATE)

class App:

    def __init__(self):

        self.stream = p.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=RATE, 
                        input=True, 
                        frames_per_buffer=1024)

        self.recording = False

        self.root = tk.Tk()
        self.root.title("Be heard")

        self.photo = tk.PhotoImage(file='./Record.png')
        self.button = tk.Button(image=self.photo, command=self.record)
        self.button.pack()

        self.currentText = tk.Text(self.root, height=2, width=50)
        
        self.currentText.pack()
        self.currentText.insert(tk.END, "Just a text Widget\nin two lines\n")

        self.resultText = tk.Text(self.root, height=10, width=50)
        self.resultText.pack()
        self.resultText.insert(tk.END, "")

        self.root.mainloop()
        

    def record(self):
        t1 = threading.Thread(target=self.listen)

        if self.recording:
            self.recording = False
            
            self.stream.close()
            print("recording stopped")
        else:
            self.recording = True
            self.stream = p.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=RATE, 
                        input=True, 
                        frames_per_buffer=1024)
            self.stream.start_stream()
            print("recording")
            t1.start()
            
            
            
        
    def updateResult(self, arg):
        self.resultText.insert(tk.END, "\n" + arg)
        print("Results: " + arg)

    def updatePartial(self, arg):
        self.currentText.delete("1.0", tk.END)
        self.currentText.insert("1.0", arg)
        print("Partial: " + arg)

    def listen(self):
        while True:
            if self.recording == False:
                break
        
            data = self.stream.read(1024)
            
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result())
                # print(text["text"])
                self.updateResult(text["text"])
                
            else:
                partial = json.loads(rec.PartialResult())
                # print(partial["partial"])
                self.updatePartial(partial["partial"])