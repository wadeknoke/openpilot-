# sounddevice must be imported after forking processes
import sounddevice as sd
import soundfile as sf
from openpilot.common.basedir import BASEDIR

SAMPLE_RATE = 48000

engage = sf.SoundFile(BASEDIR + '/selfdrive/assets/sounds/engage.wav')

def assert_sound_format(sound):
   assert sound.channels == 1
   assert sound.samplerate == SAMPLE_RATE

sounds = [engage]

for sound in sounds:
  assert_sound_format(sound)

sounds = [sound.read(dtype='float32') for sound in sounds]

sd.play(sounds[0], SAMPLE_RATE)
sd.wait()