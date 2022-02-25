import pyttsx3


def text_to_audio_file(src_text: str, dst_file: str) -> None:
    engine = pyttsx3.init()

    # change voice and rate
    voices = engine.getProperty('voices')
    # linux doesn't have gender so choose default english accent
    engine.setProperty('voice', voices[11].id)
    # default speed is 200 which is too fast so slow it down
    engine.setProperty('rate', 110)

    # read file contents
    with open(src_text, 'r') as f:
        text = f.read()

    # save to file
    engine.save_to_file(text, dst_file)
    engine.runAndWait()
    engine.stop()
