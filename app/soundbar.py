import tkinter as tk
import pygame
import keyboard  # Libreria per rilevare tasti globalmente
import re

# Mappa combinazioni di tasti ai suoni
# key_comb, song, button_pos(raw, column)
sounds = [ ("ctrl+0", r"Soundbar\app\sounds\stop.mp3",       (3,1)),   
           ("ctrl+1", r"Soundbar\app\sounds\cricket.mp3",    (2,0)), 
           ("ctrl+2", r"Soundbar\app\sounds\splash.mp3",     (2,1)),
           ("ctrl+3", r"Soundbar\app\sounds\faccetta.mp3",   (2,2)),   
           ("ctrl+4", r"Soundbar\app\sounds\beep.mp3",       (1,0)),   
           ("ctrl+5", r"Soundbar\app\sounds\fart.mp3",       (1,1)),
           ("ctrl+6", r"Soundbar\app\sounds\problemi.mp3",   (1,2)),   
           ("ctrl+7", r"Soundbar\app\sounds\ngr.mp3",        (0,0)),   
           ("ctrl+8", r"Soundbar\app\sounds\macellaio.mp3",  (0,1)),
           ("ctrl+9", r"Soundbar\app\sounds\oh_no.mp3",      (0,2))
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
