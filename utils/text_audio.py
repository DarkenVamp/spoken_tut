# import pyttsx3
import ffmpeg
from mutagen.wave import WAVE
import os
import pandas as pd
import subprocess

DF_HEADINGS = ['Text', 'Narration']


def get_narrations(src_filename: str) -> tuple:
    # open csv and extract times and texts
    df = pd.read_csv(src_filename)
    times = df.get('Times')
    text = None

    for heading in DF_HEADINGS:
        if heading in df:
            text = df[heading]

    if not text:
        raise Exception("No valid column heading found for narrations")

    if times is None:
        return (None, text)

    # convert "M:SS" to integer seconds
    for i, time in enumerate(times):
        mins, secs = time.split(':')
        times[i] = int(mins)*60 + int(secs)

    # rather than timestamps, keep adjacent differences for easier processing
    for i in range(len(times)-1, 0, -1):
        times[i] -= times[i-1]

    return (times, text)


def text_to_audio_file(src_text: list, dst_file: str, gender: int, rate: int) -> None:
    # save to file
    for i, txt in enumerate(src_text):
        subprocess.call(['espeak-ng', txt, '-s', str(rate), '-v', f'mb-us{gender}',
                         '-w', f'{dst_file}-{str(i).zfill(3)}.wav'])


def add_silence(file_path: str, duration: int) -> None:
    # apad filter adds silence at end of stream of given duration
    inp_stream = ffmpeg.input(file_path)

    # add padding
    filtered_stream = inp_stream.filter_("apad", pad_dur=duration)

    # use separate output name as ffmpeg can't edit file in-place
    output_file = f'{file_path[:-4]}-padded.wav'
    filtered_stream.output(output_file).run(overwrite_output=True)

    # replaced original with padded file
    os.replace(output_file, file_path)


def get_audio_length(file_path: str) -> int:
    return WAVE(file_path).info.length


def concat_all(prefix: str, n: int) -> None:
    # generate array of filenames
    f_names = [f'{prefix}-{str(i).zfill(3)}.wav' for i in range(n)]

    # inp array contains list of ffmpeg audio streams
    inp = list(map(lambda x: ffmpeg.input(x).audio, f_names))

    # concat using star unpacking
    # v=0 -> no video; a=1 -> single audio output stream
    concat_stream = ffmpeg.concat(*inp, v=0, a=1)
    concat_stream.output(prefix + '.wav').run(overwrite_output=True)

    # remove individual parts for clean up
    for file in f_names:
        os.remove(file)


def generate_audio(csv_file: str, dst_name: str, gender: int, rate: int) -> None:
    # separate out times and texts
    times, text = get_narrations(csv_file)

    text_to_audio_file(text, dst_name, gender, rate)

    # to calculate padding length, next_start and current audio length are needed
    if times is not None:
        for i, next_start in enumerate(times[1:]):
            f_path = f'{dst_name}-{str(i).zfill(3)}.wav'
            len_seconds = get_audio_length(f_path)
            add_silence(f_path, max(next_start - len_seconds, 0))

    concat_all(dst_name, len(text))
