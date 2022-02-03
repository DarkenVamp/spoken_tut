import pyttsx3


def text_to_audio_file(src_text: str, dst_file: str, gender: int) -> None:
    engine = pyttsx3.init()

    # change voice and rate
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[gender].id)
    engine.setProperty('rate', 110)

    # TODO: take in iobytes directly
    with open(src_text, 'r') as f:
        text = f.read()

    # TODO: use iobytes instead of file
    # save to file
    engine.save_to_file(text, dst_file)
    engine.runAndWait()
    engine.stop()
