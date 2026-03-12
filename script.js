const btnEnviar = document.getElementById('btn-enviar');
const inputUsuario = document.getElementById('input-usuario');
const historico = document.getElementById('historico-mensagens');
const nomeDisplay = document.getElementById('nome-proprio-display');
let nomeJaFoiDigitado = false; // Memória para não digitar toda vez

// Função que cria o efeito de máquina de escrever
function digitarNome(texto, velocidade = 150) {
    nomeDisplay.innerHTML = ''; // Limpa antes de começar
    nomeDisplay.classList.add('cursor-pisca'); // Liga o cursor piscando
    
    let i = 0;
    function digitarLetra() {
        if (i < texto.length) {
            nomeDisplay.innerHTML += texto.charAt(i);
            i++;
            setTimeout(digitarLetra, velocidade);
        } else {
            // Quando terminar de digitar, espera 3 segundos e tira o cursor
            setTimeout(() => nomeDisplay.classList.remove('cursor-pisca'), 3000);
        }
    }
    digitarLetra();
}

btnEnviar.addEventListener('click', async () => {
    const texto = inputUsuario.value;
    if (!texto) return;

    // 1. Mostra a mensagem do usuário na tela
    historico.innerHTML += `<div class="mensagem usuario">${texto}</div>`;
    inputUsuario.value = '';
    
    // Faz o chat rolar para baixo automaticamente
    historico.scrollTop = historico.scrollHeight;

    try {
        // 2. Chama o seu servidor Python (Flask)
        const resposta = await fetch('http://127.0.0.1:5000/perguntar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pergunta: texto })
        });
        
        if (!resposta.ok) throw new Error('Erro de conexão');

        const bandeja = await resposta.json();

        // 3. Injeta a resposta da IA
        historico.innerHTML += `<div class="mensagem ia">${bandeja.mensagem_chat}</div>`;
        historico.scrollTop = historico.scrollHeight; // Rola para baixo de novo
        
        // 4. Aplica as DUAS cores do rio animado e a cor do texto
        if(bandeja.cor_fundo_1_hex && bandeja.cor_fundo_2_hex) {
            document.documentElement.style.setProperty('--cor-fundo-1', bandeja.cor_fundo_1_hex);
            document.documentElement.style.setProperty('--cor-fundo-2', bandeja.cor_fundo_2_hex);
            document.documentElement.style.setProperty('--cor-texto', bandeja.cor_texto_hex);
        }

            // Atualize para ler bandeja.nome_proprio
        if (bandeja.nome_proprio && !nomeJaFoiDigitado) {
            digitarNome("USER: " + bandeja.nome_proprio);
            nomeJaFoiDigitado = true;
        }

    } catch (erro) {
        console.error(erro);
        historico.innerHTML += `<div class="mensagem ia" style="color: red;">[Sistema]: Perdi a conexão com o núcleo lógico.</div>`;
    }
});

// BÔNUS: Faz o "Enter" do teclado também enviar a mensagem (melhora a experiência)
inputUsuario.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        btnEnviar.click();
    }
});