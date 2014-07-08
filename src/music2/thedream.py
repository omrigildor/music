import pyaudio
import wave

p = pyaudio.PyAudio()
fw = wave.open("/Users/omrigildor/sampletest/01.All Is Fair In Love And Brostep (Feat. The Ragga Twins).wav")

stream = p.open(format=p.get_format_from_width(fw.getsampwidth()), channels=fw.getnchannels(), rate=fw.getframerate(), output=True)

d = fw.readframes(1024)
while d:
    stream.write(d)
    d = fw.readframes(1024)

