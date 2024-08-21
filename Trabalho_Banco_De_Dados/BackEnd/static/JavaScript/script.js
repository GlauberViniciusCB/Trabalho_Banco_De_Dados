// Função para iniciar o cronômetro
function iniciarTempo(duracao, display) {
    var tempo = duracao, minutos, segundos;
    setInterval(function() {
        minutos = parseInt(tempo / 60, 10);
        segundos = parseInt(tempo % 60, 10);

        minutoFormatados = minutos < 10 ? "0" + minutos : minutos;
        segundosFormatados = segundos < 10 ? "0" + segundos : segundos;

        display.textContent = minutoFormatados + ":" + segundosFormatados;

        if (tempo <= 10) {
            display.classList.add('finalTempo');
        } else {
            display.classList.remove('finalTempo');
        }

        if (--tempo < 0) {
            tempo = duracao;
        }
    }, 1000);
}

// Função para exibir mensagens com animação
function exibirMensagens() {
    var mensagens = [
        'Seja bem vindos, Meus colegas e minhas colegas de trabalho…!!!',
        'Aproveite o jogo!',
        'Vale tudo, tudo, tudo!',
        'Você está indo muito bem!',
        'Segura essa emoção',
        'Não consegue né',
        'Ma ôe',
        'O prêmio é uma maravilha!',
    ];
    var index = 0;
    var fala = document.querySelector('.balao');
    function trocarMensagem() {
        fala.classList.remove('finalTempo');
        escreverMensagem(mensagens[index]);
        index = (index + 1) % mensagens.length;
    }

    function escreverMensagem(texto) {
        fala.innerHTML = '';
        let i = 0;
        const intervalo = setInterval(() => {
            fala.innerHTML += texto.charAt(i);
            i++;
            if (i >= texto.length) {
                clearInterval(intervalo);
                setTimeout(trocarMensagem, 5000); // Tempo antes de trocar a mensagem
            }
        }, 40); // Velocidade da digitação
    }

    trocarMensagem();
}

// Inicia a função do cronômetro e exibe as mensagens
window.onload = function() {
    var duracao = 60;
    var display = document.querySelector('.tempo');
    iniciarTempo(duracao, display);
    exibirMensagens();
}
