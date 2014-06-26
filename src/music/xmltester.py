import mp3play


os.chdir("/Users/omrigildor/sampletest")

song = mp3play.load('01.Intro.mp3')
song.play()

import subprocess
audio_file = "/full/path/to/audio.wav"

return_code = subprocess.call(["afplay", audio_file])