import pygame

def reproduzir_som(caminho):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(caminho)
    try:
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()