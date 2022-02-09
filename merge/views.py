from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from utils.merge_files import merge_aud_vid
from utils.text_audio import text_to_audio_file


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

    v_name = fs.save(vid.name, vid)
    a_name = fs.save(aud.name, aud)
    # rsplit('.', maxsplit=1) gives ['filename', 'extension']
    op_path = 'media/' + v_name.rsplit('.', maxsplit=1)[0] + '-merged.mp4'

    # [1:] removes leading '/' character so relative path can be used
    v_url = fs.url(v_name)[1:].replace('%20', ' ')
    a_url = fs.url(a_name)[1:].replace('%20', ' ')
    try:
        merge_aud_vid(v_url, a_url, op_path)
    except:
        return render(request, 'merge/merge_page.html', {'error': 'Incompatible media files'})

    # delete processed files to save space
    fs.delete(vid.name)
    fs.delete(aud.name)
    return render(request, 'merge/merge_page.html', {'result': op_path})


def tts_home(request):
    if request.method != 'POST':
        return render(request, 'merge/tts_page.html')

    fs = FileSystemStorage()

    try:
        txt_file = request.FILES['transcript']
        gender = int(request.POST['gender'])
    except KeyError:
        return render(request, 'merge/tts_page.html', {'error': 'Missing fields'})

    local_txt_name = fs.save(txt_file.name, txt_file)
    audio_path = 'media/' + local_txt_name.rsplit('.', maxsplit=1)[0] + '.wav'

    try:
        text_to_audio_file(fs.url(local_txt_name)[1:], audio_path, gender)
    except:
        return render(request, 'merge/tts_page.html', {'error': 'Invalid text format'})

    fs.delete(txt_file.name)
    return render(request, 'merge/tts_page.html', {'result': audio_path})
