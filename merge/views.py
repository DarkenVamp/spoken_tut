from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from utils.merge_files import merge_aud_vid


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
