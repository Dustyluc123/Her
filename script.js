const btnEnviar = document.getElementById('btn-enviar');
const inputUsuario = document.getElementById('input-usuario');
const historico = document.getElementById('historico-mensagens');
const nomeDisplay = document.getElementById('nome-proprio-display');

let nomeJaFoiDigitado = false;
let historicoConversa = []; // <-- memoria

function digitarNome(texto, velocidade = 150) {
    nomeDisplay.innerHTML = '';
    nomeDisplay.classList.add('cursor-pisca');
    let i = 0;
    function digitarLetra() {
        if (i < texto.length) {
            nomeDisplay.innerHTML += texto.charAt(i);
            i++;
            setTimeout(digitarLetra, velocidade);
        } else {
            setTimeout(() => nomeDisplay.classList.remove('cursor-pisca'), 3000);
        }
    }
    digitarLetra();
}

btnEnviar.addEventListener('click', async () => {
    const texto = inputUsuario.value;
    if (!texto) return;

    // 1. Mostra na tela
    historico.innerHTML += `<div class="mensagem usuario">${texto}</div>`;
    inputUsuario.value = '';
    historico.scrollTop = historico.scrollHeight;

    // 2. GUARDA NA MEMÓRIA:
    historicoConversa.push({ role: "Utilizador", content: texto });

    try {
        // 3. Envia o HISTÓRICO COMPLETO em vez de só uma pergunta
        const resposta = await fetch('http://127.0.0.1:5000/perguntar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ historico: historicoConversa }) 
        });
        
        if (!resposta.ok) throw new Error('Erro de ligação');

        const bandeja = await resposta.json();

        // 4. Mostra a resposta da IA e GUARDA NA MEMÓRIA
        historico.innerHTML += `<div class="mensagem ia">${bandeja.mensagem_chat}</div>`;
        historico.scrollTop = historico.scrollHeight;
        historicoConversa.push({ role: "Elara", content: bandeja.mensagem_chat });
        
        // 5. Aplica as TRÊS cores e a fonde (Fundo 1, Fundo 2 e Caixa Sólida)
        if(bandeja.cor_fundo_1_hex) document.documentElement.style.setProperty('--cor-fundo-1', bandeja.cor_fundo_1_hex);
        if(bandeja.cor_fundo_2_hex) document.documentElement.style.setProperty('--cor-fundo-2', bandeja.cor_fundo_2_hex);
        if(bandeja.cor_caixa_hex) document.documentElement.style.setProperty('--cor-caixa', bandeja.cor_caixa_hex);
        if(bandeja.cor_texto_hex) document.documentElement.style.setProperty('--cor-texto', bandeja.cor_texto_hex);

        // 6. Só digita o nome se ela o enviar E se ainda não tiver sido digitado
        if (bandeja.nome_proprio && !nomeJaFoiDigitado) {
            digitarNome("USER: " + bandeja.nome_proprio);
            nomeJaFoiDigitado = true;
        }

    } catch (erro) {
        console.error(erro);
        historico.innerHTML += `<div class="mensagem ia" style="color: red;">[Erro de sistema]</div>`;
    }
});

inputUsuario.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') btnEnviar.click();
});