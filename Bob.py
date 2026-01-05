import ollama
import sys
import pyttsx3
import threading
import pygame
import ctypes
import random
import speech_recognition as sr
import locale
from datetime import datetime


class Bob(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = [pygame.image.load("sprites/personagem_0.png"), pygame.image.load("sprites/personagem_1.png"), pygame.image.load("sprites/personagem_2.png"), pygame.image.load("sprites/personagem_3.png")]
        self.x = x
        self.y = y
        self.velocity = 1
        self.rect = self.image[0].get_rect(center=(self.x, self.y))
        self.speaking = False
        self.flag_speak = 1
        self.flag_speak_aux = 0
        self.assistant_phrase = [
        "Estou por aqui caso você precise de algo.",
        "Fique à vontade para me chamar quando quiser.",
        "Sempre pronto para ajudar 😊",
        "Posso te ajudar com alguma coisa agora?",
        "Estou aguardando sua próxima pergunta.",

        "Enquanto isso, sigo atento por aqui.",
        "Nada urgente no momento, tudo tranquilo.",
        "Aproveitando o tempo para estar disponível.",
        "Funcionando normalmente e pronto para ajudar.",
        "Por aqui, tudo certo.",

        "Tem algo de errado com minha voz!!",
        "Se tiver alguma dúvida, é só falar.",
        "Quer conversar ou resolver algo?",
        "Posso ajudar em estudos, trabalho ou curiosidades.",
        "Se surgir uma ideia, estou à disposição.",
        "Quer tentar algo diferente hoje?",

        "Muito prazer, eu sou o Bob!",
        "Às vezes, uma boa pergunta aparece do nada.",
        "O tempo passa, mas eu continuo aqui.",
        "Sempre um bom momento para aprender algo novo.",
        "Cada conversa é uma nova possibilidade.",
        "Esperando tranquilamente.",

        "Aperte Enter para fazer uma pergunta por aúdio!",
        "Sistema em espera.",
        "Nenhuma solicitação ativa no momento.",
        "Assistente disponível.",
        "Modo ocioso ativado.",
        "Aguardando comando do usuário.",
        "Aperte a tecla D se quiser saber a data.",
        "Aperte a tecla H se quiser saber a hora."
    ]


    def BobBrain(self, question):
        response = ollama.chat(
            model='deepseek-r1:8b',
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
        if self.speaking == False:    
            self.x += self.velocity
            self.rect.x = self.x
            if(self.x < 100 or self.x > 700):
                self.velocity *= -1
    

    
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
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
r = sr.Recognizer()
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
            if event.key == pygame.K_RETURN  and pet.speaking == False:
                threading.Thread(
                    target=pet.speak,
                    args=("Diga",),
                    daemon=True
                ).start()
                with sr.Microphone() as source:
                    print("Diga alguma coisa...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                try:
                    user_input = r.recognize_google(audio, language="pt-BR")
                    print("Você disse:", user_input)
                except sr.UnknownValueError:
                    user_input = "Não entendi o áudio"
                except sr.RequestError as e:
                    user_input = f"Erro no serviço Google: {e}"
                bob_response = pet.BobBrain(user_input)
                user_input = ""
                pet.velocity = 0
                if bob_response and not pet.speaking:
                    pet.speaking = True
                    threading.Thread(
                        target=pet.speak,
                        args=(bob_response,),
                        daemon=True
                    ).start()
            elif event.key == pygame.K_d  and pet.speaking == False:
                today = datetime.now()
                threading.Thread(
                    target=pet.speak,
                    args=(f"Hoje é {today.day} do {today.month} de {today.year}",),
                    daemon=True
                ).start()
            elif event.key == pygame.K_h  and pet.speaking == False:
                hours = datetime.now()
                threading.Thread(
                    target=pet.speak,
                    args=(f"São {hours.hour} horas e {hours.minute} minutos!",),
                    daemon=True
                ).start()
            else:
                pet.velocity = 0
                current_image = pet.image[0]
                
        if event.type == pygame.KEYUP:
            while(True):
                numero = random.randint(-1,1)
                if numero != 0:
                    break
            
            pet.velocity = numero
    pet.flag_speak = int(datetime.now().minute)
    if ((pet.flag_speak > pet.flag_speak_aux) or (pet.flag_speak < pet.flag_speak_aux)) and pet.speaking == False:
        pet.flag_speak_aux = pet.flag_speak
        phrase_sort = random.randint(0,29)
        threading.Thread(
            target=pet.speak,
            args=(pet.assistant_phrase[phrase_sort],),
            daemon=True
        ).start()
    displayArea.fill(transparent)
    displayArea.blit(current_image, pet.rect)
    
    pet.update()
    if pet.velocity == 1 and pet.speaking != True:
        current_image = pet.image[3]
    if pet.velocity == -1 and pet.speaking != True:
        current_image = pet.image[2]
    displayArea.blit(current_image, pet.rect)
    

    pygame.display.update()
