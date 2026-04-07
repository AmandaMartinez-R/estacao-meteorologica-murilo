function atualizar() {
    location.reload();
}

(function initHeartbeatPoll() {
    const el = document.getElementById('heartbeat');
    if (!el) return;
    const url = el.dataset.pollUrl;
    if (!url) return;

    async function tick() {
        try {
            const r = await fetch(url);
            const j = await r.json();
            el.classList.toggle('heartbeat--ok', Boolean(j.ok));
            el.classList.toggle('heartbeat--stale', !j.ok);
            const text = el.querySelector('.heartbeat__text');
            if (text) text.textContent = j.mensagem || '';
            const ts = el.querySelector('.heartbeat__ts');
            if (ts) ts.textContent = j.ultima ? `Última: ${j.ultima}` : '';
        } catch (_) {
            el.classList.remove('heartbeat--ok');
            el.classList.add('heartbeat--stale');
            const text = el.querySelector('.heartbeat__text');
            if (text) text.textContent = 'Não foi possível consultar o servidor';
        }
    }

    setInterval(tick, 4000);
})();

function deletar(id) {
    fetch(`/leituras/${id}`, {
        method: 'DELETE'
    }).then(() => {
        location.reload();
    });
}

function salvar(event) {
    event.preventDefault();

    const id = document.getElementById('id').value;

    const dados = {
        temperatura: document.getElementById('temperatura').value,
        umidade: document.getElementById('umidade').value
    };

    fetch(`/leituras/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    }).then(() => {
        window.location.href = '/leituras';
    });
}