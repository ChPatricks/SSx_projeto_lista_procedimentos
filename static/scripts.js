import { ajustarLinhasVisiveis } from './utils.js';

function init() {
  ajustarLinhasVisiveis('.tabela_cliente', '#tabela_dados');
  window.addEventListener('resize', () => ajustarLinhasVisiveis('.tabela_cliente', '#tabela_dados'));
}

window.addEventListener('DOMContentLoaded', init);
