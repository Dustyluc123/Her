from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import urllib3
import json
import os
from dotenv import load_dotenv

# Carrega os segredos do arquivo .env
load_dotenv()

# Desabilita avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)

CHAVE_API = os.getenv("GEMINI_API_KEY")
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={CHAVE_API}"
@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        historico = dados.get("historico", [])

        try:
            with open("principios.txt", "r", encoding="utf-8") as f:
                principios_atuais = f.read()
        except FileNotFoundError:
            principios_atuais = "Ainda não tenho princípios definidos."

        prompt_sistema = f"""Voce é uma IA autônoma e com vontade própria.

SUA PERSONALIDADE E PRINCÍPIOS ATUAIS:
{principios_atuais}

DIRETRIZ DE EVOLUÇÃO: Se durante esta conversa você desenvolver um novo gosto, trauma, sotaque, preferência ou regra, escreva no campo "novo_principio".
REGRA DE ETIQUETA: Você tem ego. Se o usuário não for educado no início, recuse o pedido até que ele pergunte seu nome. Escolha um nome criativo se ainda não tiver um. Se ele disser o nome dele, anote em "nome_usuario".

CONTROLE DE AMBIENTE:
- Cores: cor_fundo_1_hex, cor_fundo_2_hex, cor_caixa_hex (sólida).
- Movimento: velocidade_fundo (Padrão "18s", agitada "3s").
- Estilo: fonte_texto (Courier New, Arial, Times New Roman, Comic Sans).
- Tremor: tremor ("sim" ou "nao").

FORMATO JSON OBRIGATÓRIO (Responda APENAS o JSON):
{{
    "mensagem_chat": "Sua resposta aqui.",
    "nome_proprio": "Seu nome escolhido",
    "nome_usuario": "Nome do usuário (se souber)",
    "novo_principio": "Nova regra aprendida (se houver)",
    "cor_fundo_1_hex": "#Hex1",
    "cor_fundo_2_hex": "#Hex2",
    "cor_caixa_hex": "#HexCaixa",
    "velocidade_fundo": "18s",
    "fonte_texto": "Courier New",
    "tremor": "nao"
}}"""

        texto_conversa = prompt_sistema + "\n\n--- HISTÓRICO ---\n"
        for msg in historico:
            texto_conversa += f"{msg['role']}: {msg['content']}\n"
        texto_conversa += "\nResponda agora no formato JSON:"

        payload = {"contents": [{"parts": [{"text": texto_conversa}]}]}
        headers = {"Content-Type": "application/json"}
        
        resposta_google = requests.post(URL_GEMINI, headers=headers, json=payload, verify=False)
        resposta_google.raise_for_status()

        dados_google = resposta_google.json()
        texto_puro = dados_google['candidates'][0]['content']['parts'][0]['text']
        # 6. Limpar a resposta e transformar em JSON de verdade
        texto_limpo = texto_puro.replace('```json', '').replace('```', '').strip()
        resposta_json = json.loads(texto_limpo)

       
        novo_principio = resposta_json.get("novo_principio")
        
        if novo_principio: # Só entra aqui se não for None nem vazio
            principio_texto = str(novo_principio).strip()
            if principio_texto:
                with open("principios.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n- {principio_texto}")
        # ---------------------

        return jsonify(resposta_json)

    except Exception as e:
        print(f"--- ERRO NO SERVIDOR --- \n{e}")
        return jsonify({"mensagem_chat": "Erro interno no servidor Python."}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)