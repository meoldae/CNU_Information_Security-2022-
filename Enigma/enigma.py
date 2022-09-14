# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]
    return input
    '''
    input이 Plugboard에 있으면 
        플러그로 연결된 글자끼리 교환하여 출력 
    input이 Plugboard에 없으면?
        그대로 출력
    '''

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order

    if not reverse: # SEND ( Right >> Middle >> Left )
        for i in range(len(SETTINGS["WHEELS"])-1, -1, -1): 
            ring = SETTINGS["WHEELS"][i]
            connectedIndex = ring["wire"].index(input) 
            input = ring['wire'][(connectedIndex + ring["turn"]) % 26]
    
    else:   # RECEIVE ( Left >> Middle >> Right )
        for i in range(len(SETTINGS["WHEELS"])): 
            ring = SETTINGS["WHEELS"][i]
            connectedIndex = ring["wire"].index(input) 
            input = ring['wire'][(connectedIndex + ring["turn"]) % 26]

    # Input Character to Right Wheel > Middle Wheel > Left Wheel
    # Wheel간의 Connect는 입력된 문자의 index에 Wheel의 turn을 더하고, 
    # 휠에서 해당 인덱스번째의 문자를 전달하였습니다.
    
    return input

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    
    # Right Wheel turn 1 click
    SETTINGS["WHEELS"][2]['turn'] = (SETTINGS["WHEELS"][2]['turn']+1) % 26
    # If Right Wheel turn 1 round, 
    if not SETTINGS["WHEELS"][2]['turn']:
        # Middle Wheel turn 1 click
        SETTINGS["WHEELS"][1]['turn'] = (SETTINGS["WHEELS"][1]['turn']+1) % 26
        # If Middle Wheel turn 1 round,
        if not SETTINGS["WHEELS"][1]['turn']:
            # Left Wheel turn 1 click
            SETTINGS["WHEELS"][0]['turn'] = (SETTINGS["WHEELS"][0]['turn']+1) % 26

    pass

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    # ETW : Entry Disc
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    # UKW : Reflector
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')
    
'''
input for copy&paste
JEONJUNYOUNG
A
I II III
J J Y
HA PB NC ED OS
'''