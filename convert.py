from os import path
from pydub import AudioSegment
import os

#input_file = ""
#output_file = ""
#
#
#sound = AudioSegment.from_mp3(input_file)
#sound.export(output_file, format="wav")


def LoadAllFile():
    path = './Data/streaming'
    files = os.listdir(path)


    for index,file in enumerate(files):
        name = os.path.basename(file).split(".")[0]
        print(name)
        input_file = os.path.join(path, file)
        output_file="./Data/wavStreaming/" + name + ".wav"
        ConvertToWav(input_file, output_file)

def ConvertToWav(inFile, outFile):
    sound = AudioSegment.from_mp3(inFile)
    sound.export(outFile, format="wav")
    wavFile = AudioSegment.from_file(outFile)
    wavFile = wavFile.set_frame_rate(48000)

if __name__ == '__main__':
    LoadAllFile()
