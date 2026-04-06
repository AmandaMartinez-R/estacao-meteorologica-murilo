function atualizar() {
    location.reload();
}

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