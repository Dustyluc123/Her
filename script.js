const historico = document.getElementById('historico-mensagens');
const inputMsg = document.getElementById('input-usuario');
const btnEnviar = document.getElementById('btn-enviar');
const nomeDisplay = document.getElementById('nome-proprio-display');
// Esta é a memória de curto prazo (a conversa atual)
let historicoConversa = [];
let nomeJaFoiDigitado = false;

btnEnviar.addEventListener('click', async () => {
    const textoUser = inputMsg.value.trim();
    if (!textoUser) return;

    // 1. Adiciona a mensagem do utilizador na tela
    const divUser = document.createElement('div');
    divUser.className = 'mensagem user';
    divUser.innerText = textoUser;
    historico.appendChild(divUser);

    // 2. Guarda a mensagem na memória
    historicoConversa.push({ "role": "user", "content": textoUser });
    inputMsg.value = '';
    historico.scrollTop = historico.scrollHeight;

    // 3. CRIA A MENSAGEM DE "PENSANDO"
    const nomeAtual = nomeJaFoiDigitado ? nomeDisplay.innerText.replace('USER: ', '') : 'A IA';
    const divPensando = document.createElement('div');
    divPensando.className = 'mensagem ia pensando';
    divPensando.innerText = `${nomeAtual} está a processar...`;
    historico.appendChild(divPensando);
    historico.scrollTop = historico.scrollHeight;

    try {
        // 4. Envia a memória para o cérebro (Python)
        const resposta = await fetch('http://127.0.0.1:5000/perguntar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ historico: historicoConversa }) 
        });
        
        // 5. REMOVE A MENSAGEM DE "PENSANDO"
        divPensando.remove();

        if (!resposta.ok) throw new Error("Erro na comunicação com o servidor.");

        const bandeja = await resposta.json();

        // 6. Adiciona a resposta da IA na tela
        const divIa = document.createElement('div');
        divIa.className = 'mensagem ia';
        divIa.innerText = bandeja.mensagem_chat;
        historico.appendChild(divIa);

        // 7. Guarda a resposta da IA na memória
        historicoConversa.push({ "role": "model", "content": bandeja.mensagem_chat });
        historico.scrollTop = historico.scrollHeight;

        // 8. CONTROLO DE AMBIENTE (Cores)
        if(bandeja.cor_fundo_1_hex) document.documentElement.style.setProperty('--cor-fundo-1', bandeja.cor_fundo_1_hex);
        if(bandeja.cor_fundo_2_hex) document.documentElement.style.setProperty('--cor-fundo-2', bandeja.cor_fundo_2_hex);
        if(bandeja.cor_caixa_hex) document.documentElement.style.setProperty('--cor-caixa', bandeja.cor_caixa_hex);

        // 9. CONTROLO DE AMBIENTE (Velocidade do Suminagashi)
        if(bandeja.velocidade_fundo) {
            document.body.style.animationDuration = bandeja.velocidade_fundo;
        }
        // --- NOVOS PODERES DA ELARA ---

        // 9.1 CONTROLO DA FONTE
        if(bandeja.fonte_texto) {
            document.body.style.fontFamily = bandeja.fonte_texto;
        }

        // 9.2 O TREMOR DE RAIVA
        if(bandeja.tremor === "sim") {
            const chatBox = document.getElementById('chat-container');
            chatBox.classList.add('tremer');
            // Tira a classe depois de 500ms para ela poder tremer de novo no futuro
            setTimeout(() => { chatBox.classList.remove('tremer'); }, 500);
        }   

     // 10. ANIMAÇÃO DO NOME E APELIDO (Sincronizado com o Subconsciente)
        const nomeReal = bandeja.nome_usuario ? bandeja.nome_usuario : "USER";
        const apelidoIA = bandeja.nome_proprio ? ` "${bandeja.nome_proprio}"` : "";
        const textoCompleto = `${nomeReal}${apelidoIA}`;

        // Só inicia a animação se o nome mudou ou se ainda não foi digitado nada
        if (nomeDisplay.innerText !== textoCompleto) {
            nomeDisplay.innerText = ''; 
            let i = 0;
            
            function digitar() {
                if (i < textoCompleto.length) {
                    nomeDisplay.innerText += textoCompleto.charAt(i);
                    i++;
                    setTimeout(digitar, 100);
                }
            }
            digitar();
        }

    } catch (erro) {
        console.error("Erro no Fetch:", erro);
        // Garante que o indicador de "processando" suma em caso de erro
        const divPensando = document.querySelector('.pensando');
        if (divPensando) divPensando.remove();
        
        const divErro = document.createElement('div');
        divErro.className = 'mensagem ia';
        divErro.innerText = "Erro: O servidor da Elara parece estar offline.";
        historico.appendChild(divErro);
    }
});

// Permite enviar a mensagem carregando no "Enter"
inputMsg.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        btnEnviar.click();
    }
});