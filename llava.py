import base64
import os
import re
import cv2
import ollama
import whisper

# ---------------------------------------------------------
# CONFIGURAÇÕES DE CAMINHO DO OBSIDIAN
# ---------------------------------------------------------
PASTA_OBSIDIAN = r"C:\Users\Vittela\Documents\Obsidian Vault"

PASTA_BLENDER = os.path.join(PASTA_OBSIDIAN, "Teia_Blender")
PASTA_CYBER = os.path.join(PASTA_OBSIDIAN, "Teia_Cybersecurity")
PASTA_GERAL = os.path.join(PASTA_OBSIDIAN, "Teia_Geral")

os.makedirs(PASTA_BLENDER, exist_ok=True)
os.makedirs(PASTA_CYBER, exist_ok=True)
os.makedirs(PASTA_GERAL, exist_ok=True)


def extrair_frames(caminho_video, max_frames=4):
    cap = cv2.VideoCapture(caminho_video)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        return []
        
    intervalo = max(1, total_frames // max_frames)
    frames_base64 = []
    
    for i in range(max_frames):
        posicao_frame = i * intervalo
        cap.set(cv2.CAP_PROP_POS_FRAMES, posicao_frame)
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_redimensionado = cv2.resize(frame, (400, 300))
        _, buffer = cv2.imencode(".jpg", frame_redimensionado, [cv2.IMWRITE_JPEG_QUALITY, 50])
        frames_base64.append(base64.b64encode(buffer).decode("utf-8"))
        
    cap.release()
    return frames_base64


def transcrever_video(caminho_video):
    try:
        modelo = whisper.load_model("base")
        txt = modelo.transcribe(caminho_video, fp16=False)["text"].strip()
        return txt if txt else "[Vídeo sem fala / Apenas instrução visual]"
    except Exception:
        return "[Não foi possível extrair áudio - Possível vídeo silencioso]"


def obter_resumo_conhecimento_previo():
    conhecimentos = []
    for pasta in [PASTA_BLENDER, PASTA_CYBER, PASTA_GERAL]:
        if os.path.exists(pasta):
            for arq in os.listdir(pasta):
                if arq.endswith(".md"):
                    conhecimentos.append(f"[[{arq.replace('.md', '')}]]")
    return ", ".join(conhecimentos) if conhecimentos else "Nenhum aprendizado anterior registrado ainda."


def limpar_nome_arquivo(titulo):
    titulo_limpo = re.sub(r'[\\/*?:"<>|]', "", titulo)
    titulo_limpo = titulo_limpo.strip().replace(" ", "_")
    return titulo_limpo if titulo_limpo else "Nota_Aprendizado"


# =========================================================
# INÍCIO DA EXECUÇÃO
# =========================================================
print("\n" + "=" * 50)
entrada_usuario = input("🎬 Digite o nome do vídeo (ex: tutorial.mp4): ").strip()
print("=" * 50 + "\n")

if not entrada_usuario.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".webm")):
    ARQUIVO_VIDEO = entrada_usuario + ".mp4"
else:
    ARQUIVO_VIDEO = entrada_usuario

if not os.path.exists(ARQUIVO_VIDEO):
    print(f"❌ ERRO: O arquivo '{ARQUIVO_VIDEO}' não foi encontrado!")
    exit()

print(f"1/5 🎧 Analisando áudio do vídeo '{ARQUIVO_VIDEO}'...")
audio = transcrever_video(ARQUIVO_VIDEO)

print(f"2/5 📸 Extraindo quadros visuais (essencial para tutoriais práticos)...")
frames = extrair_frames(ARQUIVO_VIDEO)

print("3/5 📚 Carregando a memória do Obsidian...")
conhecimento_acumulado = obter_resumo_conhecimento_previo()

print("4/5 🧠 IA interpretando tela e áudio em conjunto...")

prompt_teia = f"""Você é uma IA assistente educacional de anotações técnicas.
Descreva o procedimento técnico realizado no vídeo com base nas imagens anexadas e na transcrição fornecida.

ATENÇÃO: Se a transcrição indicar falta de fala, analise estritamente as ações práticas exibidas nos frames (ex: modelagem no Blender, ferramentas utilizadas, menus ou linhas de código na tela) e monte o passo a passo técnico.

MEMÓRIA DE CONHECIMENTOS JÁ SALVOS NO OBSIDIAN:
{conhecimento_acumulado}

REGRAS OBRIGATÓRIAS:
1. Identifique se o tema é predominantemente BLENDER, CYBERSECURITY ou GERAL.
2. Na PRIMEIRA LINHA da resposta, escreva exatamente: TITULO: [Nome Curto do Tópico]
3. Use a tag apropriada: 'blender', 'cybersecurity' ou 'geral'.
4. Crie de 4 a 6 links internos [[Nome do Conceito]] conectando as ideias.

ESTRUTURA DA NOTA:

TITULO: [Título Curto]
---
tags: [tag_do_tema]
---

# 📌 [Título Principal]

## 🎯 Resumo dos Pontos Chave
- Descrição clara da lição aprendida no vídeo.

## 💡 Explicação Detalhada
Passo a passo detalhado do procedimento ensinado no vídeo ou observado nas imagens.

## 🔗 Teia de Conexões
- [[Conceito Importante]]

ÁUDIO/TEXTO DA TRANSCRIÇÃO:
{audio}
"""

# Alterado de "llava" para o "qwen2.5vl" recém-baixado para evitar recusas visuais
resposta = ollama.chat(
    model="qwen2.5vl",
    messages=[
        {
            "role": "user",
            "content": prompt_teia,
            "images": frames
        }
    ],
    options={
        "num_ctx": 16384,
        "temperature": 0.2
    }
)

conteudo_resposta = resposta["message"]["content"]

# Processamento seguro do título
linhas = conteudo_resposta.split("\n")
titulo_sugerido = "Nota_Aprendizado"
conteudo_nota_limpo = conteudo_resposta

for linha in linhas:
    if "TITULO:" in linha:
        titulo_sugerido = linha.replace("TITULO:", "").strip()
        conteudo_nota_limpo = conteudo_resposta.replace(linha, "").strip()
        break

nome_arquivo = limpar_nome_arquivo(titulo_sugerido) + ".md"
texto_para_analise = (audio + conteudo_resposta).lower()

palavras_cyber = ["pentest", "cyber", "segurança", "hack", "nmap", "linux", "port", "ip", "ollydbg", "wi-fi"]
palavras_blender = ["blender", "bpy", "3d", "mesh", "uv", "unwrap", "render", "vertice", "face", "extrude"]

if any(p in texto_para_analise for p in palavras_cyber):
    caminho_final = os.path.join(PASTA_CYBER, nome_arquivo)
    categoria = "Cybersecurity"
elif any(p in texto_para_analise for p in palavras_blender):
    caminho_final = os.path.join(PASTA_BLENDER, nome_arquivo)
    categoria = "Blender"
else:
    caminho_final = os.path.join(PASTA_GERAL, nome_arquivo)
    categoria = "Geral"

with open(caminho_final, "w", encoding="utf-8") as f:
    f.write(conteudo_nota_limpo)

print(f"5/5 💾 Novo aprendizado de [{categoria}] salvo com sucesso em:\n   ➡️ {caminho_final}")
print("🚀 Processo concluído com sucesso!")
