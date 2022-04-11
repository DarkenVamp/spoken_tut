from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from utils.merge_files import merge_aud_vid
from utils.text_audio import generate_audio
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
        csv_file = request.FILES['transcript']  # from file input
        gender = int(request.POST['gender'])  # from radio input, gives 0 or 1
        # from text input, default is 200, default value is '' so set it to 200
        rate = int(request.POST['rate'] or 200)
    except KeyError:
        return render(request, 'merge/merge_page.html', {'error': 'Missing fields'})

    # rsplit('.', maxsplit=1) gives ['filename', 'extension']
    op_url = MEDIA_URL + vid.name.rsplit('.', maxsplit=1)[0] + '-merged.mp4'

    # save files to access them later via ffmpeg
    fs.save(vid.name, vid)
    fs.save(csv_file.name, csv_file)

    # generate paths to pass to ffmpeg
    csv_path = os.path.join(MEDIA_ROOT, csv_file.name)
    audio_url = MEDIA_URL + csv_file.name.rsplit('.', maxsplit=1)[0]
    v_path = os.path.join(MEDIA_ROOT, vid.name)
    a_path = audio_url + '.wav'

    try:
        # generate audio
        generate_audio(csv_path, audio_url, gender, rate)
        # merge video with generated audio
        merge_aud_vid(v_path, a_path, op_url)
        # delete generated audio after processing
        os.remove(a_path)
        context = {'result': op_url}
    except Exception as e:
        context = {'error': e}
    finally:
        # delete files to save space
        fs.delete(vid.name)
        fs.delete(csv_file.name)

    return render(request, 'merge/merge_page.html', context=context)
