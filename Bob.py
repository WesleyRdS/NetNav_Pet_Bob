import ollama
import sys
import pyttsx3
import threading
import pygame
import ctypes
import random


class Bob(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = [pygame.image.load("sprites/personagem_0.png"), pygame.image.load("sprites/personagem_1.png"), pygame.image.load("sprites/personagem_2.png"), pygame.image.load("sprites/personagem_3.png")]
        self.x = x
        self.y = y
        self.velocity = 1
        self.rect = self.image[0].get_rect(center=(self.x, self.y))
        self.speaking = False

    def BobBrain(self, question):
        response = ollama.chat(
            model='phi3',
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'Você é meu pet virtual e também um assistente de navegação.' 
                        'Quero que você sempre responda de forma direta e objetiva em português do Brasil!!!'
                        )
                },
                {
                    'role': 'user', 
                    'content': question
                }
                ]
        )
        return response['message']['content']
    
    def speak(self, res):
        bob_voice = pyttsx3.init()
        bob_voice.setProperty('rate', 150)  # Velocidade da fala
        bob_voice.setProperty('volume', 1)  # Volume (0.0 a 1.0)
        bob_voice.say(res)
        bob_voice.runAndWait()
        self.speaking = False
        bob_voice.stop()
    
    def update(self):    
        self.x += self.velocity
        self.rect.x = self.x
        if(self.x < 100 or self.x > 700):
            self.velocity *= -1
    

    

pygame.init()

transparent = (0, 0, 0)
displayArea = pygame.display.set_mode((800, 600), pygame.NOFRAME) #janela sem borda
# --- TRANSPARÊNCIA REAL (Windows) ---
hwnd = pygame.display.get_wm_info()["window"]

# Ativa modo "layered window"
ctypes.windll.user32.SetWindowLongW(
    hwnd,
    -20,
    ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80000
)

# Define a cor preta como transparente (RGB 0,0,0)
ctypes.windll.user32.SetLayeredWindowAttributes(
    hwnd,
    0x000000,
    255,
    0x1
)

pygame.display.set_caption("Bob")

FPS = pygame.time.Clock()
font = pygame.font.Font(None, 24)

user_input = ""
bob_response = ""

pet = Bob(700,500)
current_image = pet.image[2]

running = True
while running:
    FPS.tick(60)
    if pet.speaking == True:
        current_image = pet.image[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                bob_response = pet.BobBrain(user_input)
                user_input = ""
                pet.velocity = 0
                current_image = pet.image[1]
                if bob_response and not pet.speaking:
                    pet.speaking = True
                    threading.Thread(
                        target=pet.speak,
                        args=(bob_response,),
                        daemon=True
                    ).start()
            elif event.key == pygame.K_BACKSPACE and pet.speaking != True:
                pet.velocity = 0
                user_input = user_input[:-1]
                current_image = pet.image[0]
            else:
                pet.velocity = 0
                user_input += event.unicode
                current_image = pet.image[1]
        if event.type == pygame.KEYUP:
            while(True):
                numero = random.randint(-1,1)
                if numero != 0:
                    break
            
            pet.velocity = numero

    displayArea.fill(transparent)
    displayArea.blit(current_image, pet.rect)

    inputArea = font.render("$ "+user_input, True, (255,255,255))
    displayArea.blit(inputArea, (10, 550))
    
    pet.update()
    if pet.velocity == 1 and pet.speaking != True:
        current_image = pet.image[3]
    if pet.velocity == -1 and pet.speaking != True:
        current_image = pet.image[2]
    displayArea.blit(current_image, pet.rect)
    

    pygame.display.update()
