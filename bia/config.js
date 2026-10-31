/*
 * BIA — Teaser de lançamento · CONFIGURAÇÃO EDITÁVEL
 * --------------------------------------------------
 * Tudo o que costuma mudar fica aqui: textos, imagens e tempos (em segundos).
 * Depois de editar, abra a prévia (index.html) para conferir e rode render.mjs para gerar o MP4.
 */
window.TEASER_CONFIG = {
  largura: 1920,
  altura: 1080,
  fps: 30,
  duracao: 30, // segundos

  cores: {
    marinho: '#101D2B',     // fundo principal (Paleta oficial BIA)
    azul: '#2387F5',        // azul vibrante (usado com parcimônia)
    branco: '#FFFFFF',
    cinza: '#6B7280',
    textoApoio: '#AEB8C6',
  },

  textos: {
    suspense: ['ALGO NOVO', 'ESTÁ CHEGANDO.'],
    plataforma: ['TUDO EM UM', 'SÓ LUGAR.'],
    funcionalidades: ['SUA JORNADA', 'ACADÊMICA,', 'MAIS CONECTADA.'],
    convergencia: ['MAIS SIMPLES.', 'MAIS PERTO.', 'MAIS BIA.'],
    final: 'EM BREVE AQUI.',
    // Etiquetas que acompanham as telas
    rotulos: {
      painel: 'Painel principal',
      materiais: 'Materiais e apostilas',
      navegacao: 'Notas e frequência',
      notas: 'Notas',
      trabalhos: 'Trabalhos e atividades',
      bibliotecaApp: 'Materiais de estudo',
      perfis: 'Estudantes e professores',
    },
  },

  // Arquivos oficiais (copiados do repositório bia-v2, sem alteração de desenho)
  imagens: {
    desktopPainel: 'assets/telas/01_Estudante_Desktop.jpg',
    desktopBiblioteca: 'assets/telas/03_Biblioteca.jpg',
    desktopNotas: 'assets/telas/04_Notas_e_Frequencia.jpg',
    celularEstudante: 'assets/telas/02_Estudante_Smartphone.png',
    celularProfessora: 'assets/telas/04_Professora_Smartphone.png',
    logoBIA: 'assets/marca/BIA_Horizontal_Fundo_Escuro.svg',
    envolveSimbolo: 'assets/marca/envolvelabs-simbolo-E_PROVISORIO.png', // trocar pelo arquivo oficial transparente
    envolveNome: 'assets/marca/envolvelabs-nome-claro.svg',
  },

  // Linha do tempo (segundos). Alterar aqui desloca as cenas.
  cenas: {
    suspense: [0, 4],
    plataforma: [4, 10],
    funcionalidades: [10, 19],
    convergencia: [19, 22],
    revelacao: [22, 26],
    mensagem: [26, 28],
    assinatura: [28, 30],
  },
};
