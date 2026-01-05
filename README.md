# 💻🤖 Assistente Virtual Animado com IA em Python

Este é um **projeto pessoal** de um assistente virtual interativo desenvolvido em **Python**, que combina **inteligência artificial local**, **interface gráfica animada**, **captura do microfone** e **síntese de voz**, tudo rodando **em tempo real no desktop**.

O objetivo do projeto é explorar a integração entre **LLMs locais**, **animação 2D**, **interação por teclado** e **feedback visual e sonoro**, criando um personagem virtual responsivo e expressivo.

## 🛠️ Tecnologias Utilizadas

- 🧠 **LLM local via Ollama** (modelo *deepseek-r1:8b*) para geração de respostas às entradas do usuário  
- 🎮 **Pygame** para renderização gráfica, animação de sprites e captura de eventos de teclado  
- 🗣️ **pyttsx3** para conversão de texto em fala (TTS), executado em **thread separada** para evitar bloqueios da interface
- 🗣️ **speech_recognition** para reconhecimento de fala.
- 🪟 **Janela transparente no Windows**, utilizando integração direta com a **API Win32** via `ctypes`, exibindo apenas o personagem na tela  
- 🔄 **Lógica de movimento autônomo**, com estados de *idle*, *resposta* e *fala*, sincronizados com o comportamento visual do personagem

## 🎥 Demonstração do Projeto

### Demonstração 1:
https://github.com/WesleyRdS/NetNav_Pet_Bob/blob/master/video/video1.mp4

### Demonstração 2:
https://github.com/WesleyRdS/NetNav_Pet_Bob/blob/master/video/video2.mp4
