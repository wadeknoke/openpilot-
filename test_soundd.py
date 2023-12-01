from cereal import messaging
from openpilot.system.soundd import sound_list

pm = messaging.PubMaster(['controlsState'])


while True:
  msg = messaging.new_message('controlsState')

  for key in sound_list:
    msg.controlsState.alertSound = key
    pm.send('controlsState', msg)