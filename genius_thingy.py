import syncedlyrics
import re
import sys
import time
import pygame
from os import system
from settings import *

def convert_to_ms(timestamp: str) -> int:
    """Converts the received timestamps to milliseconds passed since start of the song"""

    timestamp = timestamp.replace('[', '')
    timestamp = timestamp.replace(']', '')
    timestamp = timestamp.replace('<', '')
    timestamp = timestamp.replace('>', '')
    timestamp = timestamp.split(":")

    ms_counter = float(timestamp[0]) * 60000 + float(timestamp[1]) * 1000
    if DEBUG: print(f"Converted timestamp: {timestamp} to {ms_counter} milliseconds")
    return int(ms_counter)

def add_char_delay(lines: list) -> list:
    """Adds the delay before each character is displayed using the difference between two timestamps"""

    if DEBUG: print(f"Started adding char delay")

    for i, line in enumerate(lines):
        verse = line['verse']
        timestamp = line['timestamp']

        # Just checks if it's not the final verse
        if i+1 == len(lines) or i + 1 > len(lines):
            delay = 0
        else:
            delay = lines[i + 1]["timestamp"] - timestamp

        # Checks if the verse isn't empty, so we don't divide by zero by accident.
        if len(verse) != 0:
            char_delay = round(delay / len(verse))
        else:
            char_delay = delay
        if DEBUG: print(f"Added a delay of {char_delay} to {i+1}st line")
        # Adds the character delay
        lines[i]['char_delay'] = char_delay

    if DEBUG: print(f"Added char delays to table: {lines}")

    return lines

def parse_text(lines: list) -> list:
    """Parses the text into the right format"""

    if DEBUG: print("Started parsing the text")

    # Pattern used to match (genuinely no clue how this works just copied it :) )
    verse_timestamp_pattern = r'\[(\d{2}:\d{2}\.\d{2})\](.+)'
    new_lines = []

    for i, line in enumerate(lines):
        # Splits the string and converts the timestamp to milliseconds
        match = re.match(verse_timestamp_pattern, line)
        if not match:
            print('failure') #Makes sure i don't forget that i'm a failure
            continue
        # Adds the timestamp of the verse
        timestamp = convert_to_ms(match.group(1))

        verse = match.group(2).strip()
        if not verse:
            verse = ' '
        #Checks if there are word specific timestamps available
        if verse[0] == '<':
            print(verse)
            word_timestamp_pattern = '''(<\d\d:\d\d\.\d\d>) ([A-Za-z,"'()]+)(?: (<\d\d:\d\d\.\d\d>))?'''
            split_verse = []
            char_delays = []
            #Searches the verse for the pattern and groups the timestamps and words together like ('timestamp1', 'verse', 'timestamp2')
            search = re.findall(word_timestamp_pattern, verse)
            #Makes a list out of all the words, so it's easier to display them one by one
            for i, word in enumerate(search):
                if word[2] == '':
                    print(word)
                    split_verse.append(word[1] + ' ')
                    char_delays.append(67)
                    continue
                split_verse.append(word[1] + ' ')
                char_delays.append(convert_to_ms(word[2]) - convert_to_ms(word[0]))

            new_lines.append({
                "verse": split_verse,
                "char_delay": char_delays,
                "timestamp": timestamp
            })

        else:
            new_lines.append({"verse": verse,
                            "char_delay": None,
                            "timestamp": timestamp})
            new_lines = add_char_delay(new_lines)
    if DEBUG: print(f"Parsed table without char_delay: {new_lines}")



    return new_lines

def init() -> list:

    search = "The Rare Occasions - Notion"

    if DEBUG: print(f"Started initiating")
    pygame.init()

    if DEBUG: print(f"SyncedLyrics is searching for '{search}'")
    lyrics = syncedlyrics.search(search)
    if DEBUG: print(f"Song found: {lyrics}")

    lines = parse_text(lyrics.split('\n'))
    return lines

def start(lines: list, channel, sound) -> None:
    system('cls')

    channel.play(sound)

    while not channel.get_busy():
        pass
    time.sleep(lines[0]['timestamp'] / 1000)

    for line in lines:
        #This if-statement makes sure that the loop won't skip an empty verse (prob an instrumental part or a bridge or smth)
        # if not line['verse']:
        #     time.sleep(line['char_delay'] / 1000)
        #     print('')
        #     continue
        for char in line['verse']:
            print(char, end='')
            sys.stdout.flush()
            time.sleep(line['char_delay'] / 1000)
        print('')

if __name__ == '__main__':
    # lines = init()
    #
    # pygame.mixer.set_num_channels(1)
    # channel = pygame.mixer.Channel(0)
    # sound = pygame.mixer.Sound(
    #     r'.\Song\The Rare Occasions ｜ ＂Notion＂ Official Music Video (online-audio-converter.com).mp3')
    #
    # if not DEBUG:
    #     start(lines, channel, sound)
    # else:
    #     print("\n Press Enter to Start")
    #     input()
    #     start(lines, channel, sound)
    # while True:
    #     if not channel.get_busy():
    #         break
    #     time.sleep(0.1)
    # print('end')
    lyrics = syncedlyrics.search('Notion - The Rare Occacions').split('\n')
    lyrics = parse_text(lyrics)
    print(lyrics)
