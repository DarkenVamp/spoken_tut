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
        video_stream,  # first stream
        audio_stream,  # second stream
        subs_stream,  # third steam
        filename=output_name,  # output name
        crf=output_crf,  # for compression
        vcodec=video_codec,  # for compatibility
        scodec='mov_text',  # mp4 supports only mov_text subtitle codec
    ).run(overwrite_output=True)
