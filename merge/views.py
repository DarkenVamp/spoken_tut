from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from utils.merge_files import merge_aud_vid
from utils.text_audio import text_to_audio_file
from spoken_tut.settings import MEDIA_ROOT
import os


def merge_home(request):
    # to handle GET and other requests
    if request.method != 'POST':
        return render(request, 'merge/merge_page.html')

    # for saving and delivering files
    fs = FileSystemStorage()

    # dictionary keys taken from merge_page template
    try:
        vid = request.FILES['video']
        aud = request.FILES['audio']
    except KeyError:
        return render(request, 'merge/merge_page.html', {'error': 'Upload both files'})

    # remove spaces to avoid errors
    vid.name = vid.name.replace(' ', '_')
    aud.name = aud.name.replace(' ', '_')
    # url() gives /media/<name>.<ext> so convert to media/<name>-merged.mp4
    op_url = fs.url(vid.name)[1:-4] + '-merged.mp4'

    # save files to access them later via ffmpeg
    fs.save(vid.name, vid)
    fs.save(aud.name, aud)

    # generate paths to pass to ffmpeg
    v_path = os.path.join(MEDIA_ROOT, vid.name)
    a_path = os.path.join(MEDIA_ROOT, aud.name)
    try:
        merge_aud_vid(v_path, a_path, op_url)
        context = {'result': op_url}
    except Exception as e:
        context = {'error': e}
    finally:
        # delete files to save space
        fs.delete(vid.name)
        fs.delete(aud.name)

    return render(request, 'merge/merge_page.html', context=context)


def tts_home(request):
    # for handling GET and other requests
    if request.method != 'POST':
        return render(request, 'merge/tts_page.html')

    fs = FileSystemStorage()

    try:
        txt_file = request.FILES['transcript']  # from file input
    except KeyError:
        return render(request, 'merge/tts_page.html', {'error': 'Missing fields'})

    # remove spaces to avoid errors
    txt_file.name = txt_file.name.replace(' ', '_')
    # save() also creates media directory so avoids FileNotFound
    fs.save(txt_file.name, txt_file)
    txt_path = os.path.join(MEDIA_ROOT, txt_file.name)
    audio_url = fs.url(txt_file.name)[1:-4] + '.wav'

    try:
        text_to_audio_file(txt_path, audio_url)
        context = {'result': audio_url}
    except Exception as e:
        context = {'error': e}
    finally:
        # nuke file
        fs.delete(txt_file.name)

    return render(request, 'merge/tts_page.html', context=context)
