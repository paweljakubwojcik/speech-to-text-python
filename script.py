import os
import shutil
from pydub.silence import split_on_silence
from pydub import AudioSegment
import speech_recognition as sr
import ffmpeg


command2mp3 = "ffmpeg -i speech.mp4 speech.mp3"
command2wav = "ffmpeg -i speech.mp3 speech.wav"

""" 
TODO: 
1.konwersja z mp4 na wav 
2.large file splitting
3. writting to .txt file
 """


r = sr.Recognizer()

os.mkdir('./tmp')

# converting mp4 file into wav file
filename = "./video_test/test-1.mp4"
output = "./tmp/temp.wav"

stream = ffmpeg.input('./video_test/test-1.mp4')
stream = ffmpeg.output(stream, output)
ffmpeg.run(stream)


def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=1000,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS-14,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language="PL")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text


text = get_large_audio_transcription(output)
print(text)

file = open('output.txt', 'w+', encoding='utf-8')
file.write(text)

shutil.rmtree('./audio-chunks')
shutil.rmtree('./tmp')


# a function that splits the audio file into chunks
# and applies speech recognition
