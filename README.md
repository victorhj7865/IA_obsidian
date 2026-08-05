# 🧠 Teia de Aprendizado Contínuo: Video-to-Obsidian Local AI

Este é um script automatizado em Python que atua como uma **IA de Aprendizado Contínuo Local**. O sistema assiste a tutoriais em vídeo (de Blender, Cybersecurity ou qualquer outra matéria), extrai o conhecimento através de processamento híbrido e gera automaticamente notas estruturadas e interconectadas em Markdown direto para o seu cofre do **Obsidian**, alimentando o seu *Graph View*.

---

## 🚀 Funcionalidades Clave

- **Análise Híbrida Inteligente**: Utiliza o modelo multimodal **Qwen2.5-VL** local via Ollama para "assistir" aos quadros do vídeo, tornando o script capaz de entender tutoriais de modelagem 3D 100% silenciosos através dos menus e ferramentas na tela.
- **Transcrição Precisa de Áudio**: Integração com o **OpenAI Whisper** rodando localmente para transcrever falas e explicações textuais.
- **Roteamento Automático de Temas**: O script analisa o conteúdo gerado e envia a nota para a pasta correspondente (`Teia_Blender`, `Teia_Cybersecurity` ou `Teia_Geral`).
- **Memória de Conhecimento Prévio**: A IA lê os títulos das notas já salvas no seu Obsidian para forçar a criação de links internos (`[[Conceito]]`), garantindo que seus aprendizados novos se conectem com os antigos no Grafo.
- **Privacidade Total e Custo Zero**: Todo o processamento (Visão computacional, IA Generativa e Transcrição) roda **100% offline** na sua própria máquina.

---

## 🛠️ Pré-requisitos

Antes de rodar o projeto, certifique-se de ter configurado em seu sistema:

1. **Python 3.10+** instalado.
2. **FFmpeg** instalado e adicionado às Variáveis de Ambiente do seu sistema (obrigatório para o Whisper processar mídias).
3. **Ollama** instalado e com o modelo de visão pronto. Baixe o modelo rodando o comando no terminal:
   ```bash
   ollama run qwen2.5vl
   ```

---

## 🔧 Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd NOME-DO-REPOSITORIO
   ```

2. **Instale as dependências necessárias:**
   ```bash
   pip install opencv-python ollama openai-whisper
   ```

3. **Configure seu caminho do Obsidian:**
   Abra o arquivo `llava.py` (ou o nome do seu script) e ajuste a linha que aponta para o diretório raiz do seu cofre do Obsidian:
   ```python
   PASTA_OBSIDIAN = r"C:\Users\SEU_USUARIO\Documents\Obsidian Vault"
   ```

---

## 🎬 Como Usar

1. Coloque o arquivo de vídeo do tutorial (ex: `aula_blender.mp4`) dentro da **mesma pasta** do script.
2. Execute o script no terminal:
   ```bash
   python llava.py
   ```
3. Digite o nome do vídeo quando solicitado e pressione `Enter`.
4. O script executará o pipeline em 5 etapas e enviará a nota formatada direto para o seu Obsidian. Abra o aplicativo e aproveite o seu mapa mental atualizado!

---

## 📄 Estrutura das Notas Geradas

A nota gerada pela IA segue o padrão de metadados exigidos para criar conexões eficientes no Obsidian:

```markdown
TITULO: Nome_Do_Topico
---
tags: [blender ou cybersecurity ou geral]
---
# 📌 [Título Principal]

## 🎯 Resumo dos Pontos Chave
- Lições aprendidas observadas nas imagens ou falas.

## 💡 Explicação Detalhada
- Passo a passo técnico dos procedimentos.

## 🔗 Teia de Conexões
- [[Links para notas antigas baseadas na memória do cofre]]
```

---

## 🛠️ Tecnologias Utilizadas

- **Python** (Linguagem base)
- **OpenCV (cv2)** (Extração e compressão inteligente de frames de vídeo)
- **OpenAI Whisper** (Transcrição local de áudio para texto)
- **Ollama & Qwen2.5-VL** (Modelo de Visão Computacional e LLM local)
- **Obsidian** (Ecossistema receptor das notas markdown)
