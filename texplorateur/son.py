import winsound


def play_sound(sound_type):
    try:
        if sound_type == "start":
            winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
        elif sound_type == "success":
            winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)
        elif sound_type == "open":
            winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
    except Exception:
        pass  # Silencieux si les sons ne fonctionnent pas
