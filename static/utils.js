// Controla tamanho da tabela em relação ao pai
export function ajustarLinhasVisiveis(divPaiSelector, tbodySelector) {
  const divPai = document.querySelector(divPaiSelector);
  const tbody = document.querySelector(tbodySelector);
  if (!divPai || !tbody) return;

  const linhas = tbody.querySelectorAll('tr');
  if (linhas.length === 0) return;

  const alturaLinha = 10; // altura da linha em px travada no css
  const alturaDisponivel = divPai.clientHeight;
  const maxLinhasVisiveis = Math.max(Math.floor(alturaDisponivel / alturaLinha) - 10, 1);

  linhas.forEach((linha, i) => {
  if (i < maxLinhasVisiveis) {
    linha.style.display = 'table-row'; // mostra linha da tabela
  } else {
    linha.style.display = 'none'; // esconde linha
  }
});
}

