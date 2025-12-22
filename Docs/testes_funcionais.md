# RELATÓRIO DE TESTES FUNCIONAIS
## Locus - Plataforma de Gestão de Ideias e Problemas

**Disciplina:** Projeto de Desenvolvimento de Sistemas para Internet  
**Equipe:**
* Mateus Cosme dos Anjos Lira
* Elias Renner Carvalho Damascena

**Orientador:** Diego Cirilo  
**Período dos Testes:** 18/12/2025 a 21/12/2025  
**Versão Testada:** 1.0 (Beta)

---

## SUMÁRIO
1. Perfil dos Testadores
2. Cenários de Testes
3. Resultados Consolidados
4. Problemas Encontrados
5. Feedback dos Testadores
6. Conclusão
7. Anexo: Evidências
8. Assinaturas

---

## 1. PERFIL DOS TESTADORES

**Testador 1 (T1)**
* **Iniciais:** L.B.
* **Faixa de idade:** 16 anos
* **Ocupação:** Estudante Federal
* **Experiência com tecnologia:** Média/Alta
* **Perfil:** Jovem, acostumado com a tecnologia.

**Testador 2 (T2)**
* **Iniciais:** E.M.
* **Faixa de idade:** 37 anos
* **Ocupação:** Merendeira
* **Experiência com tecnologia:** Baixa
* **Perfil:** Adulto, pouco familiarizado com a tecnologia.

**Testador 3 (T3)**
* **Iniciais:** J.M.
* **Idade:** 49 anos
* **Ocupação:** Analista de Licitação
* **Experiência com tecnologia:** Alta
* **Perfil:** Adulto, extremamente familiarizado com a tecnologia.

---

## 2. CENÁRIOS DE TESTES

### Cenário 01: Cadastro de Usuário
**O que testamos:** Criação de nova conta para acesso ao sistema.
**Passos:**
1. Acessar a tela de cadastro.
2. Preencher usuário, nome completo, e-mail e senha.
3. Submeter formulário.

**RESULTADOS:**
* **T1:** Sim (30s) - "Fiz o cadastro de boa. A validação é boa."
* **T2:** Sim (4m 30s) - "Pedia senha com letra maiúscula e símbolo, eu nem sabia onde apertar no teclado. Só avisou depois que eu errei."
* **T3:** Sim (2m) - "Consegui, mas fui lendo tudo bem devagar pra não errar o botão de enviar."

**Status:** APROVADO COM RESSALVAS (Melhorar feedback de senha no front-end para ajudar leigos).

---

### Cenário 02: Submissão de Ideia
**O que testamos:** Publicação de uma nova ideia no feed.
**Passos:**
1. Logar no sistema.
2. Acessar menu "Nova Ideia".
3. Preencher título, descrição e salvar.

**RESULTADOS:**
* **T1:** Sim (40s) - "O formulário tá massa, responsivo. Dá pra ver certinho o que é obrigatório preencher."
* **T2:** Sim (3m) - "Fiquei com um medo danado de clicar errado, mas apertei 'Salvar' e deu certo."
* **T3:** Sim (1m 40s) - "A letra tá num tamanho bom, deu pra ler sem forçar a vista."

**Status:** APROVADO

---

### Cenário 03: Relato de Problema
**O que testamos:** Envio de um problema.
**Passos:**
1. Acessar "Reportar Problema".
2. Enviar formulário.

**RESULTADOS:**
* **T1:** Sim (50s) - "Foi rápido e deu tudo certo."
* **T2:** Sim (1m 30s) - "Não tive muitos problemas para encontrar onde fica, consegui fazer tudo certo e registrar o problema."
* **T3:** Sim (1m 40s) - "Consegui mandar o problema sem muita dificuldade."

**Status:** APROVADO

---

### Cenário 04: Sistema de Votação
**O que testamos:** Clicar em "Gostei" nas ideias de outros usuários.
**Passos:**
1. Selecionar um card no feed.
2. Clicar no ícone de "Gostei".
3. Verificar mudança numérica.

**RESULTADOS:**
* **T1:** Sim (5s) - "Show, é rapidinho. O design ficou fluido."
* **T2:** Sim (10s) - "Cliquei na mãozinha e o número mudou. Acho que funcionou, né?"
* **T3:** Sim (5s) - "Simples, só um clique e pronto."

**Status:** APROVADO

---

### Cenário 05: Busca Inteligente
**O que testamos:** Tentar achar conteúdo digitando de formas diferentes (com e sem acento).
**Passos:**
1. Digitar termo com acento na barra de busca (ex: "Lâmpada").
2. Verificar se encontra registros escritos sem acento.

**RESULTADOS:**
* **T1:** Sim (3s) - "Funcionou liso."
* **T2:** Sim (30s) - "Eu escrevi tudo minúsculo porque nunca acho o acento nesse teclado, e ele achou mesmo assim."
* **T3:** Sim (15s) - "Muito bom, ele meio que corrige a gente e acha o que precisa."

**Status:** APROVADO

---

### Cenário 06: Comentários
**O que testamos:** Escrever comentários nas postagens.
**Passos:**
1. Abrir detalhes de uma ideia.
2. Escrever e enviar comentário.

**RESULTADOS:**
* **T1:** Sim (20s) - "Comentei e ficou salvo certinho, o horário também tá batendo com o real."
* **T2:** Sim (2m) - "Demorei pra achar onde escrevia, as letrinhas miúdas me confundiram."
* **T3:** Sim (1m) - "Escrevi meu recado e foi."

**Status:** APROVADO

---

### Cenário 07: Gamificação (subir de nível)
**O que testamos:** Verificar se o "cargo" do usuário muda ao participar.
**Passos:**
1. Realizar ações (posts/votos).
2. Verificar atualização no Perfil.

**RESULTADOS:**
* **T1:** Sim (-) - "A lógica está certa, achei uma ideia muito legal."
* **T2:** Sim (-) - "Quando reparei melhor apareceu que estava em 20% e no nível iniciante."
* **T3:** Sim (-) - "Nem reparei na hora, mas depois vi que mudou o nome lá no cantinho."

**Status:** APROVADO

---

### Cenário 08: Acessar Painel Administrativo
**O que testamos:** Tentar entrar na área restrita da gerência sem ter permissão.
**Passos:**
1. Tentar acessar o endereço de administrador.
2. Verificar se o sistema bloqueia.

**RESULTADOS:**
* **T1:** Sim (-) - "Tentei entrar na URL do admin. O Django barrou certinho."
* **T2:** Sim (-) - "Apareceu uma tela pedindo senha e eu não consegui acessar."
* **T3:** Sim (-) - "Falou que eu não posso entrar aí."

**Status:** APROVADO

---

## 3. RESULTADOS CONSOLIDADOS

### 3.1. Tabela Resumo Geral

| # | Cenário | T1 | T2 | T3 | Status Final |
|:---|:---|:---:|:---:|:---:|:---|
| **01** | Cadastro de usuário | ✅ | ⚠️ | ✅ | **Aprovado com ressalvas** |
| **02** | Submissão de ideia | ✅ | ✅ | ✅ | **Aprovado** |
| **03** | Relato de problemas | ✅ | ✅ | ✅ | **Aprovado** |
| **04** | Votação/comentários | ✅ | ✅ | ✅ | **Aprovado** |
| **05** | Busca inteligente | ✅ | ✅ | ✅ | **Aprovado** |
| **06** | Comentários | ✅ | ✅ | ✅ | **Aprovado** |
| **07** | Gamificação | ✅ | ✅ | ✅ | **Aprovado** |
| **08** | Acessar painel admin | ✅ | ✅ | ✅ | **Aprovado** |

### 3.2. Estatísticas
* **Total de testes:** 24 execuções (8 cenários x 3 testadores).
* **Taxa de Sucesso:** 95.8% (Apenas 1 ressalva significativa no Cenário 01).
* **Problemas Críticos Ativos:** 0.

---

## 4. PROBLEMAS ENCONTRADOS E SOLUÇÕES

### Problema 1: Feedback de Senha Fraca (UX)
* **Gravidade:** Média
* **Encontrado por:** Testador 2 (Cenário 01)
* **O que aconteceu:** O usuário não sabia que a senha exigia letras maiúsculas e símbolos, causando frustração e demora (4m 30s).
* **Ação Recomendada:** Adicionar texto de ajuda visível abaixo do campo de senha ("Sua senha deve ter: 1 letra maiúscula, 1 símbolo").
* **Status:** FEITO.

### Problema 2: Visibilidade de Textos Pequenos
* **Gravidade:** Baixa
* **Encontrado por:** Testador 2 (Cenário 06)
* **O que aconteceu:** O usuário teve dificuldade de encontrar o campo de comentário devido a "letras miúdas".
* **Ação Recomendada:** Aumentar ligeiramente a fonte dos placeholders e rótulos de input no CSS.
* **Status:** FEITO.

---

## 5. FEEDBACK DOS TESTADORES

> **Testador 1 (Jovem/Estudante):**
> "O sistema de gamificação é legal, dá vontade de participar para ir subindo de nível. O design é muito bonito. Senti falta de poder postar fotos, deixo a sugestão para ser um recurso futuro."

> **Testador 2 (Merendeira):**
> "A ideia do sistema é excelente para nossa comunidade. Tive dificuldade com a senha no começo, mas depois consegui usar. Queria poder mostrar as fotos dos problemas mas descrevi escrevendo mesmo."

> **Testador 3 (Analista de Licitação):**
> "O site é simples de usar, não tem botões complicados. A busca ajuda muito porque corrige quando a gente escreve errado."

---

## 6. CONCLUSÃO

O sistema **LOCUS** demonstrou estabilidade total nas suas funções textuais e de interação. A ausência de manipulação de mídia (fotos) simplificou a execução e garantiu alta performance nos testes.

**Pontos Fortes:**
* **Simplicidade:** A interface focada em texto facilitou o entendimento dos testadores T2 e T3 após o login.
* **Performance:** Tempos de resposta excelentes.

**O que Precisa Melhorar:**
* **Cadastro:** Clareza nas regras de senha para idosos/leigos.
* **Acessibilidade Visual:** Fontes maiores para inputs de texto.

---

## ANEXO: EVIDÊNCIAS
As capturas de tela dos testes foram salvas em `/docs/fotos_teste` do repositório.

---

## ASSINATURAS

**Assinatura Testador 1:** \__________________________________________________
**Data:** 21/12/2025

**Assinatura Testador 2:** \__________________________________________________
**Data:** 21/12/2025

**Assinatura Testador 3:** \__________________________________________________
**Data:** 21/12/2025