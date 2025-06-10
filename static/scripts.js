/*import { ajustarLinhasVisiveis } from './utils.js';

function init() {
  ajustarLinhasVisiveis('.tabela_cliente', '#tabela_dados');
  window.addEventListener('resize', () => ajustarLinhasVisiveis('.tabela_cliente', '#tabela_dados'));
}

window.addEventListener('DOMContentLoaded', init);*/


async function carregar_clientes() {
  fetch('http://localhost:5000/api/carregar_clientes')
    .then(response => response.json())
    .then(data => {
      console.log(data);
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

/* Chama as func ao iniciar o html*/
window.addEventListener('DOMContentLoaded', () => {
  carregar_clientes();
});


