from os.path import join
from pytube import YouTube
from moviepy.editor import *
from settings import *

class Song_Handler:
    def download(self, link):
        video = YouTube(link, on_complete_callback=self.succeed)
        stream = video.streams.get_lowest_resolution()
        stream.download(SONG_FOLDER)

        return stream.default_filename

    def convert_to_mp3(self, file_name):
        old_file_path = join(SONG_FOLDER, file_name)
        new_file_name = f"{file_name.split('.')[0]}.mp3"
        new_file_path = join(SONG_FOLDER, new_file_name)
        print(new_file_path)

        video_file = VideoFileClip(old_file_path)
        video_file.audio.write_audiofile(new_file_path)
        video_file.close()
        os.remove(old_file_path)

        return new_file_path


    def succeed(self, *args, **kwargs):
        print("Download was succesful")
        print(*args, *kwargs)
