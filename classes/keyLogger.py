# Imports
import keyboard


def key():
    def on_key_press(event):
        tecla = event.name
        print(tecla)
        return tecla

    tecla = keyboard.on_press(on_key_press)
    # Mantém o programa em execução até que a tecla 'Esc' seja pressionada
    keyboard.wait('esc')