from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai

# Configuração do Flask
app = Flask(__name__)

# Configuração do Google Generative AI
os.environ["GEMINI_API_KEY"] = "AIzaSyB0pmmCcFowVk0euSI5cg7T09SxCS4lMUk"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Configurações do modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Sessão de chat global (ou poderia ser gerenciada por usuário)
chat_session = model.start_chat(history=[])

# Rota API 1: Receber pergunta e retornar resposta diretamente
@app.route('/api/send_question', methods=['POST'])
def send_question():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "Pergunta não fornecida"}), 400

    # Enviar a pergunta ao modelo e obter a resposta
    response = chat_session.send_message(question)

    # Retornar o texto da resposta diretamente
    return jsonify({"message": "Pergunta recebida", "response_text": response.text})

# Rota HTML: Página para interação
@app.route('/')
def index():
    return render_template('index.html')

# Inicializar o servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
