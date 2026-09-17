from utils.audio_player import AudioPlayer

PISTOL_SOUND = AudioPlayer('pistol.ogg').init()
PISTOL_SOUND.set_volume(0.4)

SHOTGUN_SOUND = AudioPlayer('shotgun.ogg').init()
SHOTGUN_SOUND.set_volume(0.5)

MACHINEGUN_SOUND = AudioPlayer('machinegun.ogg').init()
MACHINEGUN_SOUND.set_volume(0.75)

RIFLE_SOUND = AudioPlayer('rifle.ogg').init()
RIFLE_SOUND.set_volume(0.5)

STAB_SOUND = AudioPlayer('stab.ogg').init()
STAB_SOUND.set_volume(0.75)

FLAMEGUN_SOUND = AudioPlayer('flamegun.ogg').init()
# FLAMEGUN_SOUND.set_volume(1)

LASER_SOUND = AudioPlayer('laser.ogg').init()
# LASER_SOUND.set_volume(1)

IMPACT_SOUND = AudioPlayer('impact.ogg').init()
IMPACT_SOUND.set_volume(0.4)

EXPLOSION_SOUND = AudioPlayer('explosion.ogg').init()
EXPLOSION_SOUND.set_volume(0.5)

BONES_SOUND = AudioPlayer('bones.ogg').init()
BONES_SOUND.set_volume(0.3)

""" 
AUDIO to add:
- burning flame ?
- collecting powerup ?

- boss death 
- boss orb creation
- ultimate move
"""