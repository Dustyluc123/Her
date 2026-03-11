const btnEnviar = document.getElementById('btn-enviar');
const inputUsuario = document.getElementById('input-usuario');
const historico = document.getElementById('historico-mensagens');

btnEnviar.addEventListener('click', async () => {
    const texto = inputUsuario.value;
    if (!texto) return;

    // 1. Mostra a mensagem do usuário na tela
    historico.innerHTML += `<div class="mensagem usuario">${texto}</div>`;
    inputUsuario.value = '';

    // 2. Chama o seu servidor Python (Flask)
    const resposta = await fetch('http://127.0.0.1:5000/perguntar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pergunta: texto })
    });

    const bandeja = await resposta.json();

    // 3. A MÁGICA: Injeta a resposta e as cores da Elara
    historico.innerHTML += `<div class="mensagem ia">${bandeja.mensagem_chat}</div>`;
    
    // Altera as cores do :root em tempo real
    document.documentElement.style.setProperty('--cor-fundo', bandeja.cor_fundo_hex);
    document.documentElement.style.setProperty('--cor-texto', bandeja.cor_texto_hex);
    document.documentElement.style.setProperty('--cor-ia-bolha', bandeja.cor_fundo_hex); // Opcional: bolha da IA combina com fundo
});