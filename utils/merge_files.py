import ffmpeg


def merge_aud_vid(video_name, audio_name, output_name):
    # get file streams
    video_stream = ffmpeg.input(video_name)
    audio_stream = ffmpeg.input(audio_name)

    # strip audio
    video_stream, subs_stream = video_stream['v:0'], video_stream['s?']
    audio_stream = audio_stream['a:0']

    # highly compatible with most devices
    video_codec = 'libx264'
    # mp4 container only supports mov_text
    subs_codec = 'mov_text'
    # crf > 24 is enough compression as its a spoken tutorial
    output_crf = 25

    # create output
    ffmpeg.output(
        video_stream,  # first stream
        audio_stream,  # second stream
        subs_stream,  # third steam
        filename=output_name,  # output name
        crf=output_crf,  # for compression
        vcodec=video_codec,  # for compatibility
        scodec=subs_codec,  # needed for mp4
    ).run(overwrite_output=True)
