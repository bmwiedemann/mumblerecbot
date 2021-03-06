#!/usr/bin/python
# -*- coding: utf-8 -*-

import wave
import time
import sys

import pymumble

from pymumble import pyopus

DEBUG = False

HOST = "mumble.nue.suse.com"
PORT = 64738
USER = "playerbot"
PASSWORD = "playerbotpw"

# input: 48kHZ mono wav - e.g. from sox INPUT -c 1 -r 48k -t wav -
AUDIO_FILE = sys.argv[1]

audio=wave.open(AUDIO_FILE)

CHANNEL = "Breakout1"
if sys.argv.__len__() > 2:
    CHANNEL = sys.argv[2]


# create the mumble instance
mumble = pymumble.Mumble(HOST, PORT, USER, PASSWORD, debug=DEBUG)

mumble.start()  # start the mumble thread
mumble.is_ready()  # wait for the connection
mumble.users.myself.unmute()  # by sure the user is not muted
mumble.channels.find_by_name(CHANNEL).move_in()

start = time.time()

frames = audio.readframes(480)
while frames:
    while mumble.sound_output.get_buffer_size() > 0.5:
        time.sleep(0.01)  # if mumble outgoing buffer is full enough, wait a bit
        
    mumble.sound_output.add_sound(frames)  # send a piece of audio to mumble
    
    frames = audio.readframes(480)

while mumble.sound_output.get_buffer_size() > 0:  # wait for the output buffer to empty
    time.sleep(0.01)  # wait for the mumble buffer's exhaustion before exiting

time.sleep(1.2)  # some extra time for transmission

audio.close()
