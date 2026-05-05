import re
import os
import html

# ================= CONFIGURAÇÕES =================
INPUT_FILE = 'conversa.txt'
OUTPUT_FILE = 'visualizador.html'
# Ajustado para refletir exatamente o nome da sua pasta (Case-sensitive)
MEDIA_FOLDER = 'Media' 
# =================================================

def parse_txt(file_path):
    """Lê o arquivo TXT do WhatsApp e extrai as mensagens."""
    # Padrão para mensagens normais (com ':')
    pattern = re.compile(r"^\[(\d{2}/\d{2}/\d{2,4}[, ]+\d{2}:\d{2}:\d{2})\] (.*?): (.*)")
    # Padrão para mensagens do sistema (sem ':')
    sys_pattern = re.compile(r"^\[(\d{2}/\d{2}/\d{2,4}[, ]+\d{2}:\d{2}:\d{2})\] (.*)")
    
    messages = []
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        current_msg = None
        
        for line in f:
            clean_line = line.replace('\u200e', '').replace('\u200f', '').lstrip()
            if not clean_line:
                continue

            match = pattern.match(clean_line)
            if match:
                if current_msg:
                    messages.append(current_msg)
                
                current_msg = {
                    'timestamp': match.group(1).strip(),
                    'sender': match.group(2).strip(),
                    'text': match.group(3),
                    'is_system': False
                }
            else:
                sys_match = sys_pattern.match(clean_line)
                if sys_match:
                    if current_msg:
                        messages.append(current_msg)
                        current_msg = None
                    
                    messages.append({
                        'timestamp': sys_match.group(1).strip(),
                        'sender': None,
                        'text': sys_match.group(2).strip(),
                        'is_system': True
                    })
                else:
                    if current_msg:
                        current_msg['text'] += "\n" + clean_line.strip()
        
        if current_msg:
            messages.append(current_msg)
            
    return messages

def determinar_tipo_midia(filename):
    """Determina o tipo de mídia baseado na extensão do arquivo."""
    ext = filename.split('.')[-1].lower()
    if ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
        return 'image'
    elif ext in ['mp4', 'mov', 'avi', 'mkv']:
        return 'video'
    elif ext in ['mp3', 'ogg', 'wav', 'm4a', 'opus', 'aac']:
        return 'audio'
    return 'file'

def gerar_html_whatsapp(mensagens, dono_celular):
    """Gera o código HTML baseado nas mensagens lidas."""
    html_code = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Visualizador de Conversa - WhatsApp</title>
        <style>
            body {
                background-color: #efeae2;
                background-image: url('bg_chat.png');
                font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
            }
            .chat-container {
                width: 100%;
                max-width: 800px;
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            .msg {
                max-width: 75%;
                width: fit-content;
                padding: 6px 10px;
                border-radius: 8px;
                position: relative;
                box-shadow: 0 1px 1px rgba(0,0,0,0.1);
                word-wrap: break-word;
                margin-bottom: 2px;
            }
            .msg.first-of-group { margin-top: 8px; }
            
            /* ======== CSS DAS MENSAGENS DE SISTEMA ======== */
            .msg.system {
                align-self: center;
                background-color: #ffeebd;
                color: #555;
                font-size: 0.85em;
                text-align: center;
                border-radius: 12px;
                max-width: 90%;
            }
            /* ============================================== */

            .msg.left { align-self: flex-start; background-color: #ffffff; border-top-left-radius: 0; }
            .msg.right { align-self: flex-end; background-color: #d9fdd3; border-top-right-radius: 0; }
            .author { font-weight: bold; font-size: 0.85em; margin-bottom: 2px; color: #029d00; }
            .msg.right .author { color: #35a8e0; }
            .text { font-size: 0.95em; line-height: 1.3; color: #111; white-space: pre-wrap; }
            .time { font-size: 0.65em; color: #667781; text-align: right; display: block; margin-top: 2px; }
            .media-container { margin-top: 4px; margin-bottom: 4px; }
            img.media, video.media { max-width: 100%; border-radius: 6px; max-height: 350px; object-fit: cover; }
            audio.media { max-width: 300px; height: 40px; margin-top: 4px; }
            a.document {
                display: block; background: rgba(0,0,0,0.05); padding: 10px;
                border-radius: 6px; text-decoration: none; color: #000; font-size: 0.9em;
                display: flex; align-items: center; gap: 8px;
            }
            i { color: #555; font-style: italic; }
            
            /* Twemoji CSS para garantir os emojis como o bumerangue 🪃 */
            img.emoji {
                height: 1.2em;
                width: 1.2em;
                margin: 0 .05em 0 .1em;
                vertical-align: -0.1em;
            }
        </style>
        
        <script src="https://cdn.jsdelivr.net/npm/@twemoji/api@latest/dist/twemoji.min.js" crossorigin="anonymous"></script>
    </head>
    <body>
        <div class="chat-container">
    """

    autor_anterior = None

    for m in mensagens:
        text_raw = m.get('text', '')
        author = m.get('sender')
        time_str = m.get('timestamp')
        
        if m.get('is_system'):
            html_code += f'<div class="msg system"><div class="text">{html.escape(text_raw)}</div><span class="time">{time_str}</span></div>\n'
            autor_anterior = None
            continue

        media_html = ""
        media_match = re.search(r"<attached:\s*(.*?)>", text_raw)
        
        if media_match:
            filename = media_match.group(1).strip()
            caminho_midia_html = f"{MEDIA_FOLDER}/{filename}"
            tipo_midia = determinar_tipo_midia(filename)
            
            if tipo_midia == 'image':
                media_html = f'<div class="media-container"><img class="media" src="{caminho_midia_html}" alt="Imagem anexada" loading="lazy"></div>'
            elif tipo_midia == 'video':
                media_html = f'<div class="media-container"><video class="media" controls preload="metadata"><source src="{caminho_midia_html}"></video></div>'
            elif tipo_midia == 'audio':
                media_html = f'<div class="media-container"><audio class="media" controls preload="metadata"><source src="{caminho_midia_html}"></audio></div>'
            else:
                media_html = f'<div class="media-container"><a class="document" href="{caminho_midia_html}" target="_blank">📄 Documento: {filename}</a></div>'
            
            text_raw = text_raw.replace(media_match.group(0), "").strip()

        text_safe = html.escape(text_raw)

        # Inserção de itálicos nos metadados
        text_safe = text_safe.replace("&lt;This message was edited&gt;", "<i>(Mensagem editada)</i>")
        text_safe = text_safe.replace("image omitted", "<i> Imagem indisponível</i>")
        text_safe = text_safe.replace("document omitted", "<i> Documento indisponível </i>")

        # Formatação WhatsApp
        text_formatado = re.sub(r'\*(.+?)\*', r'<b>\1</b>', text_safe)
        text_formatado = re.sub(r'_(.+?)_', r'<i>\1</i>', text_formatado)
        text_formatado = re.sub(r'~(.+?)~', r'<s>\1</s>', text_formatado)

        # Lógica de dono do celular
        align_class = 'right' if author == dono_celular else 'left'

        mostrar_autor = True
        classes_extras = "first-of-group"
        if author == autor_anterior:
            mostrar_autor = False
            classes_extras = ""
        
        autor_anterior = author

        html_code += f'<div class="msg {align_class} {classes_extras}">'
        
        if mostrar_autor and author:
            html_code += f'<div class="author">{author}</div>'
            
        html_code += media_html
        
        if text_formatado.strip():
            html_code += f'<div class="text">{text_formatado}</div>'
            
        html_code += f'<span class="time">{time_str}</span></div>\n'

    html_code += """
        </div>
        
        <script>
            window.onload = function() {
                twemoji.parse(document.body, { folder: 'svg', ext: '.svg' });
            };
        </script>
    </body>
    </html>
    """
    
    return html_code

if __name__ == "__main__":
    if os.path.exists(INPUT_FILE):
        print(f"Lendo {INPUT_FILE}...\n")
        
        dono_input = input("Digite o nome do 'dono' do celular (para alinhar à direita), exatamente como aparece no TXT: ")
        dono_celular = dono_input.strip() 

        chat_data = parse_txt(INPUT_FILE)
        
        if not chat_data:
            print("Nenhuma mensagem foi lida. Verifique o formato do arquivo TXT.")
        else:
            print("\nProcessando conversas e gerando visualizador...")
            html_final = gerar_html_whatsapp(chat_data, dono_celular)
            
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(html_final)
            
            print(f"\nSucesso! Foram processadas {len(chat_data)} mensagens.")
            print(f"Abra o arquivo '{OUTPUT_FILE}' no seu navegador.")
    else:
        print(f"Erro: Arquivo '{INPUT_FILE}' não encontrado na pasta atual.")