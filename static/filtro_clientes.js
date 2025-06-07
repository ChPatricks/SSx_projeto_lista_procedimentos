document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('filtro').addEventListener('input', function () {
    const termo = this.value;
    fetch(`/filtro_clientes?termo=${encodeURIComponent(termo)}`)
      .then(response => response.json())
      .then(dados => {
        const tbody = document.getElementById('tabela_dados');
        tbody.innerHTML = ''; // limpa a tabela
        dados.forEach(cliente => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${cliente[0]}</td>
            <td>${cliente[1]}</td>
            <td>${cliente[2]}</td>
            <td>${cliente[3] ? 'Sim' : 'Não'}</td>
          `;
          tbody.appendChild(tr);
        });
      });
  });
});