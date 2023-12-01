# sounddevice must be imported after forking processes
import soundfile as sf
from typing import Dict, Optional, Tuple
import sounddevice as sd
import numpy as np

from cereal import car, messaging
from openpilot.common.basedir import BASEDIR

SAMPLE_RATE = 48000

AudibleAlert = car.CarControl.HUDControl.AudibleAlert

MAX_VOLUME = 1.0

sound_list: Dict[int, Tuple[str, Optional[int], float]] = {
  # AudibleAlert, file name, play count (none for infinite)
  AudibleAlert.engage: ("engage.wav", 1, MAX_VOLUME),
  AudibleAlert.disengage: ("disengage.wav", 1, MAX_VOLUME),
  AudibleAlert.refuse: ("refuse.wav", 1, MAX_VOLUME),

  AudibleAlert.prompt: ("prompt.wav", 1, MAX_VOLUME),
  AudibleAlert.promptRepeat: ("prompt.wav", None, MAX_VOLUME),
  AudibleAlert.promptDistracted: ("prompt_distracted.wav", None, MAX_VOLUME),

  AudibleAlert.warningSoft: ("warning_soft.wav", None, MAX_VOLUME),
  AudibleAlert.warningImmediate: ("warning_immediate.wav", None, MAX_VOLUME),
}

loaded_sounds: Dict[int, np.ndarray] = {}

# Load all sounds
for sound in sound_list:
  filename, play_count, volume = sound_list[sound]

  with sf.SoundFile(BASEDIR + "/selfdrive/assets/sounds/" + filename) as f:
    assert f.channels == 1
    # TODO: these should all be the same sample rate
    #assert f.samplerate == SAMPLE_RATE
    loaded_sounds[sound] = f.read(dtype='float32')


def soundd():
  sm = messaging.SubMaster(['controlsState', 'microphone'])

  current_alert = AudibleAlert.none

  with sd.OutputStream(channels=1, samplerate=SAMPLE_RATE) as stream:
    while True:
      sm.update()

      new_alert = sm['controlsState'].alertSound

      if current_alert != new_alert.raw:
        current_alert = new_alert.raw
        stream.write(loaded_sounds[current_alert])


if __name__ == "__main__":
  soundd()