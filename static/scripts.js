
async function carregar_clientes(termo = '') {
  const baseUrl = 'https://dc13-177-21-141-9.ngrok-free.app'; /*url base do ngrok */
  const endpoint = termo.trim()
    ? `/api/filtrar_clientes?termo=${encodeURIComponent(termo)}` /*se houver conteudo de input no filtro */
    : '/api/carregar_clientes'; // rota que carrega todos (else)

  fetch(baseUrl + endpoint)
    .then(response => response.json())
    .then(data => {
      const tabela = document.getElementById('tabela_dados');
      tabela.innerHTML = ''; // limpa a tabela antes de preencher

      data.forEach(dado => {
        const linha = document.createElement('tr');

        const id = document.createElement('td');
        id.textContent = dado.ID;

        const nome = document.createElement('td');
        nome.textContent = dado.NOME;

        const idade = document.createElement('td');
        idade.textContent = dado.IDADE;

        const ativo = document.createElement('td');
        ativo.textContent = dado.ATIVO ? 'Sim' : 'Não';

        linha.appendChild(id);
        linha.appendChild(nome);
        linha.appendChild(idade);
        linha.appendChild(ativo);

        tabela.appendChild(linha);
      });
    })
    .catch(error => {
      console.error('Erro ao buscar dados:', error);
    });
}

async function carregar_procedimentos() {
    const baseUrl = 'https://dc13-177-21-141-9.ngrok-free.app/api/carregar_procedimentos';

    const response = await fetch(baseUrl);
    const dados = await response.json();
    console.log(dados)

    const container = document.getElementById('procedimento_container');
    container.innerHTML = ''; // Limpa antes de preencher

    dados.forEach(procedimento => {
      const caixa = document.createElement('div');
      caixa.className = 'procedimento_caixa';

      const input = document.createElement('input');
      input.type = 'checkbox';
      input.name = `cb${procedimento.id}`;
      input.id = `cb${procedimento.id}`;

      const label = document.createElement('label');
      label.setAttribute('for', input.id);
      label.textContent = procedimento.ativo ? procedimento.procedimento : 'PROCEDIMENTO INATIVADO';

      caixa.appendChild(input);
      caixa.appendChild(label);

      container.appendChild(caixa);
    });
  }

/* Chama as func ao iniciar o html / a cada F5 na pagina*/
window.addEventListener('DOMContentLoaded', () => {
const inputFiltro = document.getElementById('filtro_cliente');

  // Ao carregar a página, carrega todos os clientes
  carregar_clientes();
  carregar_procedimentos();

  // Enquanto digita, filtra com base no conteúdo
  inputFiltro.addEventListener('keyup', () => {
    const valor = inputFiltro.value;
    carregar_clientes(valor);
  });
});


