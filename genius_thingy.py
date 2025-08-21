import syncedlyrics
import re
import sys
import time
import pygame
from os import system
pygame.init()
lyrics = syncedlyrics.search("Ode to a conversation stuck in your throat Del water Gap")

def convert_to_ms(timestamp: str) -> int:
    timestamp = timestamp.replace('[', '')
    timestamp = timestamp.replace(']', '')
    timestamp = timestamp.split(":")
    ms_counter = 0
    ms_counter += float(timestamp[0]) * 60000 + float(timestamp[1]) * 1000

    return int(ms_counter)

def char_delay(list):
    print(list)
    for i, line in enumerate(list):
        verse = line['verse']
        timestamp = line['timestamp']
        if i+1 == len(list) or i + 1 > len(list):
            delay = 0
        else:
            delay = list[i + 1]["timestamp"] - timestamp
        if len(verse) != 0:
            char_delay = round(delay / len(verse))
        else:
            char_delay = 0

        print(f"{delay} / {len(verse)} = {char_delay}")
        list[i]['char_delay'] = char_delay

    return list

def parse_text(lines):
    pattern = r'\[(\d{2}:\d{2}\.\d{2})\](.+)'
    new_lines = []

    for i, line in enumerate(lines):
        match = re.match(pattern, line)
        timestamp = convert_to_ms(match.group(1))
        verse = match.group(2).strip()


        new_lines.append({"verse": verse,
                          "char_delay": None,
                          "timestamp": timestamp})
    print(new_lines)
    new_lines = char_delay(new_lines)

    return new_lines




lines = parse_text(lyrics.split('\n'))

print(lines)
time.sleep(3)
print("GO")

sound = pygame.mixer.Sound('.\Song\Del Water Gap - Ode to a Conversation Stuck in Your Throat (Official Video) - Del Water Gap.mp3')
sound.play()

system('cls')

time.sleep(0.20)
time.sleep(lines[0]['timestamp'] / 1000)
for line in lines:
    for char in line['verse']:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(line['char_delay'] / 1000)
    #time.sleep(delays[i])
    print('')

