import tkinter as tk
import pygame
import keyboard  # Libreria per rilevare tasti globalmente
import re
import sys
import os

# Get path, to be runned from both terminal or .exe
if getattr(sys, 'frozen', False):
    # Running in a bundled app
    base_path = sys._MEIPASS
else:
    # Running in a normal Python environment
    base_path = os.path.dirname(__file__)



# Mappa combinazioni di tasti ai suoni
# key_comb, song, button_pos(raw, column)
sounds = [ ("ctrl+0",  f"{base_path}"+r"\sounds\stop.mp3",       (3,1)),   
           ("ctrl+1",  f"{base_path}"+r"\sounds\cricket.mp3",    (2,0)), 
           ("ctrl+2",  f"{base_path}"+r"\sounds\splash.mp3",     (2,1)),
           ("ctrl+3",  f"{base_path}"+r"\sounds\faccetta.mp3",   (2,2)),   
           ("ctrl+4",  f"{base_path}"+r"\sounds\beep.mp3",       (1,0)),   
           ("ctrl+5",  f"{base_path}"+r"\sounds\fart.mp3",       (1,1)),
           ("ctrl+6",  f"{base_path}"+r"\sounds\problemi.mp3",   (1,2)),   
           ("ctrl+7",  f"{base_path}"+r"\sounds\ngr.mp3",        (0,0)),   
           ("ctrl+8",  f"{base_path}"+r"\sounds\macellaio.mp3",  (0,1)),
           ("ctrl+9",  f"{base_path}"+r"\sounds\oh_no.mp3",      (0,2))
        ]

# # Get key grid dimension #-------------------------------------------
# grid_dimensions = [0,0]
# # Find max key pos
# for combo_key, sound, btn_pos in sounds:
#     if btn_pos[0] > grid_dimensions[0]:
#         grid_dimensions[0] = btn_pos[0]
#     if btn_pos[1] > grid_dimensions[1]:
#         grid_dimensions[1] = btn_pos[1]
# # Since pos start from 0
# grid_dimensions[0]+=1
# grid_dimensions[1]+=1
# #-------------------------------------------------------------------
    

# Inizializza pygame mixer
pygame.mixer.init()


# Variabile per tenere traccia del suono in esecuzione
current_sound = None


# Funzione per riprodurre o fermare un suono
def play_or_stop_sound(sound_file):
    global current_sound

    if current_sound:  # Se c'è già un suono in riproduzione
        current_sound.stop()  # Fermalo
        if current_sound.get_sound() == pygame.mixer.Sound(sound_file):  # Se è lo stesso, interrompi e non riparti
            current_sound = None
            return

    # Riproduce il nuovo suono
    current_sound = pygame.mixer.Channel(0)  # Usa un canale per gestire il suono
    current_sound.play(pygame.mixer.Sound(sound_file))


# Funzione per ascoltare la pressione dei tasti
def listen_for_keys():
    while True:
        for combo_key, sound, btn_pos in sounds:
            keys = combo_key.split('+')  # Divide la combinazione in singoli tasti
            if all(keyboard.is_pressed(key) for key in keys):  # Verifica se tutti i tasti sono premuti
                play_or_stop_sound(sound)



# Creazione della finestra principale --------------------------------------------------------------
root = tk.Tk()
root.title("Soundboard 🎵")
root.geometry("600x300")

# Frame per organizzare i pulsanti
frame = tk.Frame(root)
frame.pack(pady=20)

# Creazione dei pulsanti
for combo_key, sound, btn_pos in sounds:
    song_name = re.search(r'\\([^\\]+)(?=\.mp3)', sound).group(1) # Extract song name from path
    btn = tk.Button(frame, text=f"{combo_key} : {song_name}", command=lambda s=sound: play_or_stop_sound(s), height=2, width=20)
    btn.grid(row=btn_pos[0], column=btn_pos[1], padx=10, pady=10)


# Avvia il thread per ascoltare i tasti globali
import threading
key_thread = threading.Thread(target=listen_for_keys, daemon=True)
key_thread.start()

# Avvia il loop della GUI
root.mainloop()
