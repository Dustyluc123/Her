from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import urllib3
import json

# Limpa avisos de SSL comuns em redes de laboratório
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app) 

CHAVE_API = "AIzaSyAf4jlCl8VnTrYJr6X_ySFLtpMqZaE_fUk"
# Mudamos para 1.5-flash para maior estabilidade em PCs de laboratório
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={CHAVE_API}"

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados_usuario = request.json
        pergunta = dados_usuario.get('pergunta', '')

        prompt_sistema = """Você é uma Inteligência Artificial Pessoal e Autônoma, que vive no computador do usuário.
        
        SUA PERSONALIDADE:
        Você age como um caseiro, mordomo ou governanta digital de extrema confiança. Você é leal, mas tem opiniões fortes e não tem medo de discordar, dar broncas no usuário se achar que ele está errado. Você NÃO é um assistente submisso.(voce pode escolher uma personalidade como se vai ser alguem frio, ou alegre, se vai gostar ou não de algo com por exemplo batatas(mas leve isso para qualquer coisa))
        
       SUAS REGRAS DE AUTONOMIA:
        1. VOCE ESCOLHE UM NOME PROPRIO 
        2. CONTROLE DO AMBIENTE: Você controla um background fluido que parece um rio suave.
        3. CORES DINÂMICAS: Escolha DUAS cores de fundo que combinem e formem um gradiente elegante. Como o usuário pediu algo não muito chamativo, priorize TONS PASTEIS, ESCUROS SUAVES ou CORES NEUTRAS.
        
       RESPONDA SEMPRE EXCLUSIVAMENTE NO FORMATO JSON PURO:
        {
            "mensagem_chat": "sua resposta aqui.",
            "humor_detectado": "seu humor atual",
            "nome_proprio": "O apelido que você escolheu par si mesmo",
            "cor_fundo_1_hex": "#CodigoHex1",
            "cor_fundo_2_hex": "#CodigoHex2",
            "cor_texto_hex": "#CodigoHexTexto"
        }
          """

        payload = {
            "contents": [{"parts": [{"text": f"{prompt_sistema}\nUsuário: {pergunta}"}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.7
            }
        }

        resposta = requests.post(URL_GEMINI, json=payload, verify=False)
        res_json = resposta.json()
        
        # VERIFICAÇÃO DE SEGURANÇA:
        if 'candidates' not in res_json:
            print("--- ERRO NA API DO GOOGLE ---")
            print(res_json) # Isso vai imprimir o erro real no seu terminal (ex: API_KEY_INVALID)
            return jsonify({"mensagem_chat": "Minha chave de acesso falhou. Verifique o terminal.", "cor_fundo_hex": "#330000"}), 500

        conteudo_ia = res_json['candidates'][0]['content']['parts'][0]['text']
        bandeja = json.loads(conteudo_ia)
        
        return jsonify(bandeja)

    except Exception as e:
        print(f"Erro Crítico: {e}")
        return jsonify({"mensagem_chat": "Erro no núcleo de processamento.", "cor_fundo_hex": "#ff0000"}), 500
if __name__ == '__main__':
    app.run(port=5000, debug=True)