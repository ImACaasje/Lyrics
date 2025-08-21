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
            char_delay = 0
        if DEBUG: print(f"Added a delay of {char_delay} to {i+1}st line")
        # Adds the character delay
        lines[i]['char_delay'] = char_delay

    if DEBUG: print(f"Added char delays to table: {lines}")

    return lines

def parse_text(lines: list) -> list:
    """Parses the text into the right format"""

    if DEBUG: print("Started parsing the text")

    # Pattern used to match (genuinely no clue how this works just copied it :)
    pattern = r'\[(\d{2}:\d{2}\.\d{2})\](.+)'
    new_lines = []

    for i, line in enumerate(lines):
        # Splits the string and converts the timestamp to milliseconds
        match = re.match(pattern, line)
        timestamp = convert_to_ms(match.group(1))
        verse = match.group(2).strip()


        new_lines.append({"verse": verse,
                          "char_delay": None,
                          "timestamp": timestamp})

    if DEBUG: print(f"Parsed table without char_delay: {new_lines}")

    new_lines = add_char_delay(new_lines)

    return new_lines

def init() -> list:

    search = "Ode to a conversation stuck in your throat Del water Gap"

    if DEBUG: print(f"Started initiating")
    pygame.init()

    if DEBUG: print(f"SyncedLyrics is searching for '{search}'")
    lyrics = syncedlyrics.search(search)
    if DEBUG: print(f"Song found: {lyrics}")

    lines = parse_text(lyrics.split('\n'))
    return lines

def start(lines: list) -> None:
    system('cls')

    sound = pygame.mixer.Sound('.\Song\Del Water Gap - Ode to a Conversation Stuck in Your Throat (Official Video) - Del Water Gap.mp3')
    sound.play()

    time.sleep(0.20)
    time.sleep(lines[0]['timestamp'] / 1000)

    for line in lines:
        for char in line['verse']:
            print(char, end='')
            sys.stdout.flush()
            time.sleep(line['char_delay'] / 1000)
        print('')

if __name__ == '__main__':
    lines = init()
    if not DEBUG:
        start(lines)
    else:
        print("\n Press Enter to Start")
        input()
        start(lines)
