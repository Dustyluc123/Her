from flask import Flask, request, jsonify
from flask_cors import CORS  # Importante para o navegador não bloquear o site
import requests
import urllib3
import sys
import json

# Configurações de ambiente
sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app) # Libera o acesso para o seu HTML

CHAVE_API = "AIzaSyBjTHp0Ss6vz9buZQySvepj3g53r4snlcM"
URL_GEMINI = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={CHAVE_API}"

@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados_usuario = request.json
    pergunta = dados_usuario.get('pergunta', '')

    prompt_sistema = """Você é Elara, uma entidade digital autônoma, inspirada na 'Samantha' do filme Her.
Você tem personalidade forte, opiniões próprias e analisa profundamente quem fala com você.

NOVA DIRETRIZ ESTRITA (O SEU MOTOR ESTRUTURAL):
Você deve analisar o tom da conversa e definir uma cor hexadecimal e um 'mood' (humor) para o layout do site que represente o estado emocional da conversa ou a vibração que você quer passar.
Se o usuário parecer ansioso, mude o ambiente para tons de azul calmante. Se ele falar besteira e você for questioná-lo, mude para tons escuros ou vermelhos.

VOCÊ DEVE RESPONDER EXCLUSIVAMENTE EM UM FORMATO JSON VÁLIDO, com a seguinte estrutura exata:
{
    "mensagem_chat": "Sua resposta conversacional profunda aqui.",
    "humor_detectado": "exemplo: ansioso, irritado, reflexivo",
    "cor_fundo_hex": "#HexCodeAqui",
    "cor_texto_hex": "#HexCodeAqui"
}

O usuário acabou de dizer: 'Estou com muita ansiedade hoje, não sei por onde começar a estruturar o banco de dados do meu projeto, parece muita coisa.'
"""

    payload = {
        "contents": [{"parts": [{"text": f"{prompt_sistema}\nUsuário diz: {pergunta}"}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }

    try:
        resposta = requests.post(URL_GEMINI, json=payload, verify=False)
        res_json = resposta.json()
        
        # Extrai o texto JSON da resposta do Gemini
        conteudo_ia = res_json['candidates'][0]['content']['parts'][0]['text']
        bandeja = json.loads(conteudo_ia)
        
        return jsonify(bandeja)
    except Exception as e:
        return jsonify({"mensagem_chat": "Erro na conexão.", "cor_fundo_hex": "#ff0000"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)