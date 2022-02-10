from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from utils.merge_files import merge_aud_vid
from utils.text_audio import text_to_audio_file
from spoken_tut.settings import MEDIA_ROOT, MEDIA_URL
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

    # rsplit('.', maxsplit=1) gives ['filename', 'extension']
    op_url = MEDIA_URL + vid.name.rsplit('.', maxsplit=1)[0] + '-merged.mp4'

    # save files to access them later via ffmpeg
    fs.save(vid.name, vid)
    fs.save(aud.name, aud)

    # generate paths to pass to ffmpeg
    v_path = os.path.join(MEDIA_ROOT, vid.name)
    a_path = os.path.join(MEDIA_ROOT, aud.name)
    try:
        merge_aud_vid(v_path, a_path, op_url)
    except:
        return render(request, 'merge/merge_page.html', {'error': 'Incompatible media files'})

    # delete processed files to save space
    fs.delete(vid.name)
    fs.delete(aud.name)
    return render(request, 'merge/merge_page.html', {'result': op_url})


def tts_home(request):
    # for handling GET and other requests
    if request.method != 'POST':
        return render(request, 'merge/tts_page.html')

    fs = FileSystemStorage()

    try:
        txt_file = request.FILES['transcript']  # from file input
        gender = int(request.POST['gender'])  # from radio input, gives 0 or 1
    except KeyError:
        return render(request, 'merge/tts_page.html', {'error': 'Missing fields'})

    # save() also creates media directory so avoids FileNotFound
    fs.save(txt_file.name, txt_file)
    txt_path = os.path.join(MEDIA_ROOT, txt_file.name)
    audio_url = MEDIA_URL + txt_file.name.rsplit('.', maxsplit=1)[0] + '.wav'

    try:
        text_to_audio_file(txt_path, audio_url, gender)
    except:
        return render(request, 'merge/tts_page.html', {'error': 'Invalid text format'})

    # nuke file after processing
    fs.delete(txt_file.name)
    return render(request, 'merge/tts_page.html', {'result': audio_url})
