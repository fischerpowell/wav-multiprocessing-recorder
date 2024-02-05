import pyaudio
import wave
import datetime
import multiprocessing

class Recording:
    def __init__(self, filename, samples=1024, format = pyaudio.paInt16, rate = 44100):
        
        self.interface = pyaudio.PyAudio()
        channels = self.interface.get_default_input_device_info()['maxInputChannels']

        self.samples = samples
        self.format = format
        self.rate = rate

        #Timestamp based file name by default
        self.filename = filename

        #Init wave file for recording
        self.wav_file = wave.open(f'audio_recordings/{self.filename}.wav', 'wb')
        self.wav_file.setnchannels(channels)

        #Init stream
       

        self.stream = self.interface.open(format= format,
                                          channels = self.wav_file.getnchannels(),
                                          rate = rate,
                                          input = True,
                                          frames_per_buffer = samples)
        
        self.frames = []


    def record(self):
        data = self.stream.read(self.samples)
        self.frames.append(data)

    def stop(self):
        sample_width = self.interface.get_sample_size(self.format)
        self.wav_file.setsampwidth(sample_width)
        self.wav_file.setframerate(self.rate)
        self.wav_file.writeframes(b''.join(self.frames))
        self.wav_file.close()
        self.interface.terminate()



class RecordController:
    def __init__(self):
        self.is_recording = multiprocessing.Value('i', 1)
        self.recording_process = multiprocessing.Process(target=self.run, args=(str(datetime.datetime.now()).replace(".", "-").replace(":", "-"),))
        self.recording_process.start()
        

    def run(self, filename):
        self.new_recording = Recording(filename)
        while self.is_recording.value == 1:
            self.new_recording.record()
        print("Stopping")
        self.new_recording.stop()


if __name__ == '__main__':
    recorder = RecordController()

    while True:
        if input("Gimme input pls") == "a":
            recorder.is_recording.value = 0
            break
            