====================================================================================
VISUALIZADOR FORENSE DE CONVERSAS DO WHATSAPP / WHATSAPP CHAT FORENSIC VIEWER
====================================================================================

--- [ PORTUGUÊS ] ---

# SOBRE O PROJETO
Este script em Python converte arquivos de exportação nativos do WhatsApp (.txt) em uma página HTML autossuficiente. O objetivo é facilitar a visualização, leitura e análise da conversa, replicando o layout original do aplicativo, suportando mídias (fotos, vídeos, áudios e documentos) e operando de forma 100% offline e portátil (via USB ou armazenamento local).

# ESTRUTURA DE DIRETÓRIOS EXIGIDA
Para que o programa funcione e o HTML gerado seja portátil, garanta que a pasta raiz do projeto contenha exatamente a seguinte estrutura antes de executar o script:

/Pasta_do_Projeto
 │-- whatsapp_viewer.py      (O script Python)
 │-- conversa.txt            (O log exportado do WhatsApp renomeado para este nome)
 │-- bg_chat.png             (A imagem de fundo do WhatsApp para uso offline)
 │-- read_me.txt             (Este arquivo)
 └── /Media                  (Pasta contendo todas as fotos, vídeos e áudios citados no .txt)

# COMO EXECUTAR
1. Abra o terminal ou prompt de comando na pasta do projeto.
2. Execute o comando: python whatsapp_viewer.py
3. O terminal solicitará o nome do "dono do celular". Digite o nome exatamente como aparece no arquivo .txt para que as mensagens dessa pessoa fiquem alinhadas à direita.
4. O arquivo "visualizador.html" será gerado. Abra-o em qualquer navegador web.

# NOTAS DE REVISÃO E MENSAGENS DE SISTEMA (IMPORTANTE)
Sempre confirme se as mensagens renderizadas no HTML estão fiéis ao arquivo TXT original.
O WhatsApp, ao exportar o log, ocasionalmente atribui mensagens de sistema (ex: "Fulano is a contact", "Security code changed") a um usuário específico dentro do arquivo TXT, formatando-as como se fossem mensagens comuns.

O script tenta identificar automaticamente o que é do sistema, mas as anomalias nativas do exportador do WhatsApp devem ser corrigidas manualmente no HTML final para garantir a lisura da exibição.

COMO FAZER A CORREÇÃO MANUAL DE MENSAGENS ANÔMALAS:
Se você abrir o HTML e vir uma mensagem de sistema formatada como um balão de usuário comum, siga estes passos:
1. Abra o arquivo "visualizador.html" em um editor de texto (Bloco de Notas, VS Code, etc.).
2. Pressione Ctrl+F (Localizar) e busque pelo texto da mensagem (ex: "author2 is a contact").
3. Você encontrará um bloco de código parecido com este:

<div class="msg left first-of-group">
    <div class="author">author1</div>
    <div class="text">author2 is a contact.</div>
    <span class="time">10:45:00</span>
</div>

4. Altere a classe da primeira linha para <div class="msg system"> e apague a linha inteira correspondente ao <div class="author">. O resultado final deve ficar assim:

<div class="msg system">
    <div class="text">author2 is a contact.</div>
    <span class="time">10:45:00</span>
</div>

5. Salve o arquivo HTML e recarregue a página no navegador.


====================================================================================


--- [ ENGLISH ] ---

# ABOUT THE PROJECT
This Python script converts native WhatsApp export files (.txt) into a self-contained HTML page. The goal is to facilitate the visualization, reading, and analysis of the chat by replicating the app's original layout, supporting media (photos, videos, audios, and documents), and operating 100% offline and portably (via USB or local storage).

# REQUIRED DIRECTORY STRUCTURE
For the script to work and the generated HTML to be portable, ensure the root folder contains exactly the following structure before running the script:

/Project_Folder
 │-- whatsapp_viewer.py      (The Python script)
 │-- conversa.txt            (The exported WhatsApp log, renamed to this)
 │-- bg_chat.png             (The WhatsApp background image for offline use)
 │-- read_me.txt             (This file)
 └── /Media                  (Folder containing all media referenced in the .txt)

# HOW TO RUN
1. Open the terminal or command prompt in the project folder.
2. Run the command: python whatsapp_viewer.py
3. The terminal will ask for the "phone owner's" name. Type the name exactly as it appears in the .txt file so their messages align to the right.
4. The "visualizador.html" file will be generated. Open it in any web browser.

# REVIEW NOTES AND SYSTEM MESSAGES (IMPORTANT)
Always confirm that the rendered messages in the HTML accurately reflect the original TXT file.
When exporting the log, WhatsApp occasionally attributes system messages (e.g., "John Doe is a contact", "Security code changed") to a specific user within the TXT file, formatting them as regular messages.

The script attempts to automatically identify system messages, but native anomalies from WhatsApp's exporter must be corrected manually in the final HTML to ensure display accuracy.

HOW TO MANUALLY CORRECT ANOMALOUS MESSAGES:
If you open the HTML and see a system message formatted as a regular user bubble, follow these steps:
1. Open the "visualizador.html" file in a text editor (Notepad, VS Code, etc.).
2. Press Ctrl+F (Find) and search for the message text (e.g., "author2 is a contact").
3. You will find a code block similar to this:

<div class="msg left first-of-group">
    <div class="author">author1</div>
    <div class="text">author2 is a contact.</div>
    <span class="time">10:45:00</span>
</div>

4. Change the class of the first line to <div class="msg system"> and delete the entire <div class="author"> line. The final result should look like this:

<div class="msg system">
    <div class="text">author2 is a contact.</div>
    <span class="time">10:45:00</span>
</div>

5. Save the HTML file and refresh the page in your browser.