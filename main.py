import pygame
import sys
import time
from os import system, walk
import os
from pytube import YouTube
from moviepy.editor import *
from settings import *
from Song_Handler import Song_Handler

pygame.init()


new_file_path = join('.', 'Notion.mp3')
sound = pygame.mixer.Sound(new_file_path)
sound.play()
system('cls')


def print_lyrics():
    lines = [
        ("Sure, it's a calming notion, perpetual in motion", 0.12),
        ("But I don't need the comfort of any lies", 0.1),
        ("For I have seen the ending and there is no ascending", 0.1),
        ("Riiiiiiiiiiiiiiise", 0.3),
        ("Oh, back when I was younger, was told by other youngsters", 0.1),
        ("That my end will be torture beneath the earth", 0.1),
        ("'Cause I don't see what they see when death is staring at me", 0.1),
        ("I see a window, a limit, to live it, or not at all", 0.08)
    ]
    delays = [0.3, 2, 1.5, 0, 0, 1.5, 0, 0]

    for i, (line, char_delay) in enumerate(lines):
        for char in line:
            print(char, end='')
            sys.stdout.flush()
            time.sleep(char_delay)
        time.sleep(delays[i])
        print('')

    system('curl parrot.live')

print_lyrics()

class App:
    def __init__(self):
        self.clear_folder(SONG_FOLDER)
        self.link = input("Song link; ")
        self.song_handler = Song_Handler()

        self.download(mp3=True)


    def clear_folder(self, folder):
        for full_path, sub_folders, file_names in walk(folder):
            for file in file_names:
                os.remove(join(full_path, file))

    def download(self, mp3=False):
        file_path = self.song_handler.download(self.link)
        if mp3: file_path = self.song_handler.convert_to_mp3(file_path)

        self.song_path = file_path
        system('cls')
        self.play()

    def play(self):
        self.sound = pygame.mixer.Sound(self.song_path)
        self.sound.play()

    def run(self):
        while True:
            pass


if __name__ == '__main__':
    # app = App()
    # app.run()
    pass

