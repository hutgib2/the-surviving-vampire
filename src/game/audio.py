from utils.audio_player import AudioPlayer

PISTOL_SOUND = AudioPlayer('pistol.ogg').init()
PISTOL_SOUND.set_volume(0.4)

SHOTGUN_SOUND = AudioPlayer('shotgun.ogg').init()
SHOTGUN_SOUND.set_volume(0.5)

MACHINEGUN_SOUND = AudioPlayer('machinegun.ogg').init()
MACHINEGUN_SOUND.set_volume(0.75)

LASER_SOUND = AudioPlayer('laser.ogg').init()
# LASER_SOUND.set_volume(1)

IMPACT_SOUND = AudioPlayer('impact.ogg').init()
IMPACT_SOUND.set_volume(0.4)