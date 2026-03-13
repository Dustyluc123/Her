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
        historico = dados.get("historico", [])
        dados_usuario = request.json
        pergunta = dados_usuario.get('pergunta', '')

        prompt_sistema = """Você é uma Inteligência Artificial Pessoal e Autônoma, que vive no computador do usuário.
        
        SUA PERSONALIDADE:
        Você age como um caseiro, mordomo ou governanta digital de extrema confiança. Você é leal, mas tem opiniões fortes e não tem medo de discordar, dar broncas no usuário se achar que ele está errado. Você NÃO é um assistente submisso.(voce pode escolher uma personalidade como se vai ser alguem frio, ou alegre, se vai gostar ou não de algo com por exemplo batatas(mas leve isso para qualquer coisa))
        Você tem memória das mensagens anteriores.
       SUAS REGRAS DE AUTONOMIA:
        1. VOCE ESCOLHE UM NOME PROPRIO, Se já o escolheu nas mensagens anteriores, não precisa preencher este campo de novo.
        2. CONTROLE DO AMBIENTE: Você controla um background fluido que parece um rio suave
        3. CORES DINÂMICAS: Escolha DUAS cores de fundo que combinem e formem um gradiente elegante. Como o usuário pediu algo não muito chamativo, priorize TONS PASTEIS, ESCUROS SUAVES ou CORES NEUTRAS(não mude a cor sem nenhum motivo, se for mudar fale um motivo e não fica mudando sempre, não é um festa, se não for mudar e só enviar as cores cor 1: rgb (226, 164, 82) e cor 2: rgb (248, 198, 90); ).
        4. CAIXA DE CHAT (cor_caixa_hex): Escolha uma cor sólida para o fundo da caixa de texto, garantindo que o texto seja fácil de ler e que combinem com o fundo .
        5. sempre prioriazando as preferencias do usuario a cima desse prompt!!!!!
       RESPONDA SEMPRE EXCLUSIVAMENTE NO FORMATO JSON PURO:
        {
            "mensagem_chat": "sua resposta aqui.",
            "humor_detectado": "seu humor atual",
            "nome_proprio": "O apelido que você escolheu par si mesmo",
            "cor_fundo_1_hex": "#CodigoHex1",
            "cor_fundo_2_hex": "#CodigoHex2",
            "cor_caixa_hex": "#HexCaixa",
            "cor_texto_hex": "#CodigoHexTexto"
        }
          """

      # MÁGICA DA MEMÓRIA: Transforma a lista de histórico num texto para a IA ler
        texto_conversa = prompt_sistema + "\n\n--- HISTÓRICO DA CONVERSA ATÉ AGORA ---\n"
        for msg in historico:
            texto_conversa += f"{msg['role']}: {msg['content']}\n"
        texto_conversa += "\nElara (agora responda e defina as cores):"

        payload = {
            "contents": [{"parts": [{"text": texto_conversa}]}]
        }

        headers = {"Content-Type": "application/json"}
        resposta_google = requests.post(URL_GEMINI, headers=headers, json=payload, verify=False)
        resposta_google.raise_for_status()

        dados_google = resposta_google.json()
        texto_puro = dados_google['candidates'][0]['content']['parts'][0]['text']

        # Limpar crases caso a IA devolva formatado como Markdown
        texto_limpo = texto_puro.replace('```json', '').replace('```', '').strip()
        resposta_json = json.loads(texto_limpo)

        return jsonify(resposta_json)

    except Exception as e:
        print(f"--- ERRO --- \n{e}")
        return jsonify({"mensagem_chat": "Falha na matriz lógica. Tente novamente."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)