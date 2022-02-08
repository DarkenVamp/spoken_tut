from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from utils.merge_files import merge_aud_vid
from utils.text_audio import text_to_audio_file


def merge_home(request):
    if request.method != 'POST':
        return render(request, 'merge/merge_page.html')

    fs = FileSystemStorage()

    try:
        vid = request.FILES['video']
        aud = request.FILES['audio']
    except KeyError:
        return render(request, 'merge/merge_page.html', {'error': 'Upload both files'})

    v_name = fs.save(vid.name, vid)
    a_name = fs.save(aud.name, aud)
    op_path = 'media/' + v_name[:-4] + '-merged.mp4'

    try:
        merge_aud_vid(fs.url(v_name)[1:], fs.url(a_name)[1:], op_path)
    except:
        return render(request, 'merge/merge_page.html', {'error': 'Incompatible media files'})

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
    audio_path = 'media/' + txt_file.name[:-4] + '.wav'

    try:
        text_to_audio_file(fs.url(local_txt_name)[1:], audio_path, gender)
    except:
        return render(request, 'merge/tts_page.html', {'error': 'Invalid text format'})

    return render(request, 'merge/tts_page.html', {'result': audio_path})
