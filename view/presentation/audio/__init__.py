from . import audio_resources


def play_animation_audio(src):
    audio = get_audio(src)
    print(audio)


def get_audio(src):
    audio = audio_resources.RESOURCES[src]
    return audio
