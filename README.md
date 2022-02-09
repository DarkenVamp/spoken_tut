# Spoken Tutorial
Why? See [Here](https://spoken-tutorial.org/stinternship2022/autogeneration/).

## Instructions

#### Pre-requisites
>```ffmpeg``` should be in your path, more information [here](https://ffmpeg.org/).

Install requirements
>```pip install -r requirements.txt```

Run migrate command
>```python manage.py migrate```

#### Running
Run using
>```python manage.py runserver```

#### Open in browser
Visit [localhost](http://localhost:8000)

## How to use?
- Default page is the merge portal, upload valid video and audio files.
- It should give a Preview button after clicking merge, if something went wrong either ffmpeg is not in path or uploaded files are invalid.
- The TTS page accepts text file with readable text.
> Example contents: "The quick brown fox jumped over a branch"
- If the text file is valid a download button would be visible.