filename = None

def audio_download_hook(d):
    if d["status"] == "finished":
        global filename
        filename = d["filename"]
