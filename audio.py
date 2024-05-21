
import speech_recognition as sr
import soundfile as sf
import keyboard

from pvrecorder import PvRecorder
import pyaudio
import wave
import time
 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 6
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)


def record():

    '''This Function is for recording the input audio file and saves it as a wave file'''

    filename = input('Enter the Output Filename: ')
    filename = filename + ".wav"
    # print(filename)

    print("Press r key to start Recording\nPress q to Stop Recording")
    keyboard.wait('r')  # Wait for any key press to start recording

    print("Recording...")

    frames = []
    
    while not keyboard.is_pressed('q'):
        data = stream.read(CHUNK)
        frames.append(data)
      
    # stop Recording
    print("Recording Stopped...")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return filename


def audio_to_text(file):

    """This Function converts the audio file in wav format to text and return the text as string"""
    # print(type(file))
    r = sr.Recognizer()
    audiofile = sr.AudioFile(file)
    with audiofile as source:
        audio = r.record(source)

    string = r.recognize_whisper(audio)

    # print(string)
    return string



if __name__ == "__main__":

    # audio = record()
    result = audio_to_text("AUDIO_FILE_LOCATION")
    print(result)