import colorsys
import random
import queue
import threading as th
from time import sleep


from openrazer.client import DeviceManager
from openrazer.client import constants as c
#from pynput.keyboard import Key, Listener
import keyboard as kb


KEY_MAPPING = { 1  : (0, 0), # Key.esc
                2  : (0, 0), # &
                3  : (0, 1), # é
                4  : (0, 1), # "
                5  : (0, 2), # '
                6  : (0, 2), # (
                7  : (0, 3), # -
                8  : (0, 3), # è
                9  : (0, 4), # _
                10 : (0, 4), # ç
                11 : (0, 4), # à
                12 : (0, 5), # )
                13 : (0, 0), # =
                14 : (0, 6), # Key.backspace
                15 : (0, 0), # Key.tab
                16 : (0, 1), # A
                17 : (0, 1), # Z
                18 : (0, 1), # E
                19 : (0, 2), # R
                20 : (0, 2), # T
                21 : (0, 3), # Y
                22 : (0, 3), # U
                23 : (0, 4), # I
                24 : (0, 4), # O
                25 : (0, 5), # P
                26 : (0, 5), # ^ 
                27 : (0, 6), # $
                28 : (0, 6), # Enter
                29 : (0, 0), # Ctrl
                30 : (0, 1), # Q
                31 : (0, 1), # S
                32 : (0, 2), # D
                33 : (0, 2), # F
                34 : (0, 2), # G
                35 : (0, 3), # H
                36 : (0, 3), # J
                37 : (0, 4), # K
                38 : (0, 4), # L
                39 : (0, 5), # M
                40 : (0, 5), # Ù 
                41 : (0, 0), # Œ 
                42 : (0, 0), # Shift 
                43 : (0, 6), # *
                44 : (0, 1), # W
                45 : (0, 1), # X
                46 : (0, 2), # C
                47 : (0, 2), # V
                48 : (0, 3), # B
                49 : (0, 3), # N
                50 : (0, 4), # ,
                51 : (0, 4), # ;
                52 : (0, 5), # :
                53 : (0, 5), # !
                54 : (0, 6), # Shift right
                56 : (0, 1), # Alt
                57 : (0, 3), # Space
                58 : (0, 0), # Key.caps_lock
                59 : (0, 1), # F1
                60 : (0, 1), # F2
                61 : (0, 2), # F3
                62 : (0, 2), # F4
                63 : (0, 3), # F5
                64 : (0, 3), # F6
                65 : (0, 4), # F7
                66 : (0, 4), # F8
                67 : (0, 5), # F9
                68 : (0, 5), # F10
                87 : (0, 6), # F11
                88 : (0, 6), # F12
                86 : (0, 1), # <
                99 : (0,7),  # Key.print_screen
                70 : (0,7), # Key.scroll_lock
                -1 : (0, 120), # "Key.media_volume_down"
                -1 : (0, 120), # "Key.media_volume_up" 
                69 : (0, 8), # Numpad Verrnum
                79 : (0, 8), # Numpad 1
                80 : (0, 8), # Numpad 2
                81 : (0, 9), # Numpad 3
                75 : (0, 8), # Numpad 4
                76 : (0, 8), # Numpad 5
                77 : (0, 9), # Numpad 6
                71 : (0, 8), # Numpad 7
                72 : (0, 8), # Numpad 8
                73 : (0, 9), # Numpad 9
                82 : (0, 8), # Numpad 0
                83 : (0, 9), # Numpad suppr
                78 : (0, 9), # Numpad +
                74 : (0, 9), # Numpad -
                96 : (0, 9), # Numpad enter
                55 : (0, 9), # Numpad *
                98 : (0, 8), # Numpad /
                97 : (0, 6), # Ctrl right
                100 : (0, 5), # Alt gr
                102 : (0, 7), # Page
                103 : (0, 7), # Up
                104 : (0, 7), # Page up
                105 : (0, 7), # Left
                106 : (0, 7), # Right
                108 : (0, 7), # Down
                107 : (0, 7), # Fin
                109 : (0, 7), # Page down
                110 : (0, 7), # Inser
                111 : (0, 7), # Suppr
                119 : (0, 7), # Key.pause
                125 : (0, 1), # Os touch
                127 : (0, 6), # Menu
}


# CONSTANTS

FADE_TIME = 20
STATIC_COLOR = (0, 15, 90)
#STATIC_COLOR = (0, 200, 255)
REACTIVE_COLOR = (0, 200, 255)
#REACTIVE_COLOR = (0, 0, 0)

# Create a DeviceManager. This is used to get specific devices
device_manager = DeviceManager()

print("Found {} Razer devices".format(len(device_manager.devices)))

devices = device_manager.devices
for device in list(devices):
    if not device.fx.advanced:
        print("Skipping device " + device.name + " (" + device.serial + ")")
        devices.remove(device)

print()

# Disable daemon effect syncing.
# Without this, the daemon will try to set the lighting effect to every device.
device_manager.sync_effects = False

# Colors functions
def random_color():
    rgb = colorsys.hsv_to_rgb(random.uniform(0, 1), random.uniform(0.5, 1), 1)
    return tuple(map(lambda x: int(256 * x), rgb))

# Interpolation
def lerp(start, end, percentage):
    return start + percentage * (end - start)

def fade(device, x, y, start_color, end_color, time): # time in tens of ms
    for t in range(0, time):
        # Check if this thread must terminate
        if getattr(th.current_thread(), "stop", False): 
            break
        # Calcul the new color and draw the zone
        device.fx.advanced.matrix[x, y] = (
            int(lerp(start_color[0]/255, end_color[0]/255, t/time)*255), 
            int(lerp(start_color[1]/255, end_color[1]/255, t/time)*255), 
            int(lerp(start_color[2]/255, end_color[2]/255, t/time)*255)
        )
        device.fx.advanced.draw()
        sleep(0.01)


# Handle keyboard events
def reactivePress(x, y):
    for device in devices:
        try:
            device.fx.advanced.matrix[x, y] = REACTIVE_COLOR
            device.fx.advanced.draw()
        except Exception as e:
            print(e)
            continue

def reactiveRelease(x, y):
    for device in devices:
        try:
            fade(device, x, y, REACTIVE_COLOR, STATIC_COLOR, FADE_TIME)
        except Exception as e:
            print(e)
            continue

def default():
    for device in devices:
        rows, cols = device.fx.advanced.rows, device.fx.advanced.cols
        for row in range(rows):
            for col in range(cols):
                device.fx.advanced.matrix[row, col] = STATIC_COLOR
        device.fx.advanced.draw()

# Threads actions on events
ths = queue.Queue()
# A dictionary to know wich thread is active on keyboard's zones.
#   -> thsOnZones[y] = th
thsOnZones = {}

# What to do when an event occur ?
def on_action(event):
    xy = KEY_MAPPING.get(event.scan_code)
    # Key press
    if event.event_type == kb._keyboard_event.KEY_DOWN:
        # terminating other thread on that zone
        if xy[1] in thsOnZones:
            thsOnZones[xy[1]].stop = True
        # create the thread and start effects
        myT = th.Thread(target=reactivePress, args=(xy[0], xy[1]))
        myT.start()
        # saving references to that new thread
        ths.put(myT)
        thsOnZones[xy[1]] = myT
    # Key release
    elif event.event_type == kb._keyboard_event.KEY_UP:
        # terminating other thread on that zone
        if xy[1] in thsOnZones:
            thsOnZones[xy[1]].stop = True
        myT = th.Thread(target=reactiveRelease, args=(xy[0], xy[1]))
        myT.start()
        ths.put(myT)
        thsOnZones[xy[1]] = myT


# Set default keyboard background color
default()

# Start detecting events on kb
kb.hook(lambda e: on_action(e))

# Looping to join threads
while(1):
    ths.get(True).join()

# Waiting undefinitely
kb.wait()



