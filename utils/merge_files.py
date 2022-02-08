import ffmpeg


def merge_aud_vid(video_name, audio_name, output_name):
    # get file streams
    video_stream = ffmpeg.input(video_name)
    audio_stream = ffmpeg.input(audio_name)

    # strip audio
    video_stream, subs_stream = video_stream['v'], video_stream['s']

    # highly compatible with most devices
    video_codec = 'libx264'
    # crf > 24 is enough compression as its a spoken tutorial
    output_crf = 25

    # create output
    ffmpeg.output(
        video_stream,
        audio_stream,
        subs_stream,
        filename=output_name,
        crf=output_crf,
        vcodec=video_codec,
        scodec='mov_text',
    ).run(overwrite_output=True)
