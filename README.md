3. 🏥 Sistema de Clínica Médica/Odontológica
   A clínica conta com diversos profissionais de saúde, de diferentes especialidades, que atuam em consultórios próprios. Eventualmente um profissional é afastado, desligado ou tem a agenda suspensa, e novos profissionais são contratados — sendo necessário manter o cadastro de profissionais, especialidades e horários sempre atualizado.

Os pacientes procuram a clínica para marcar consultas. Primeiro é necessário cadastrá-los, registrando se o atendimento será particular ou por convênio. Depois de identificado, o paciente escolhe a especialidade, o profissional e o horário disponível na agenda — o valor da consulta varia conforme a especialidade, o tipo de atendimento e se é primeira consulta ou retorno. O sistema deve impedir conflito de horário (dois pacientes no mesmo slot do mesmo profissional).

Realizada a consulta, define-se como concluída, registra-se data/hora e anotam-se no prontuário os procedimentos efetuados (cada procedimento extra tem valor próprio e soma ao total). Retornos dentro do prazo não são cobrados. Em caso de falta sem aviso ou remarcação fora do prazo, registra-se a ocorrência e aplicam-se as penalidades previstas.

Werike Rodrigues Alves 3

🚀 Como Executar
python main.py

🎯 Objetivo
Desenvolver um sistema de gestão completo, aplicando os conceitos estudados ao longo da disciplina: variáveis e tipos de dados, estruturas de decisão e repetição, listas e dicionários, funções, validação de dados e organização do código.

Cada equipe escolherá um dos temas disponíveis abaixo e deverá implementar o sistema atendendo aos requisitos descritos para aquele tema, além dos requisitos mínimos comuns a todos os projetos.

💡 Todos os temas têm o mesmo grau de complexidade. Não há tema "mais fácil" — a nota depende da qualidade da implementação, não do tema escolhido.

📋 Orientações Gerais
Equipes: de 2 integrantes (você e Deus).
Tema: cada equipe escolhe um tema.
Linguagem: Python 3.
Entrega: repositório/pasta com o código-fonte + este README preenchido com os nomes da equipe.
Apresentação: demonstração do sistema funcionando + explicação do código.
Prazo de entrega: 15/07/2026
✅ Requisitos Mínimos (comuns a todos os temas)
Independentemente do tema escolhido, o sistema deve conter:

Menu principal com navegação (laço de repetição até o usuário escolher sair).
Cadastro completo (CRUD) das principais entidades:
Criar (incluir novo registro)
Recuperar (listar / consultar)
Update (alterar dados de um registro)
Delete (remover registro)
Pelo menos 4 entidades relacionadas entre si.
Validação de dados de entrada (não aceitar valores inválidos, campos vazios, opção inexistente no menu etc.).
Regras de negócio específicas do tema (cálculos, multas, descontos, verificação de disponibilidade etc.).
Manipulação de datas/horas quando o tema exigir (uso do módulo datetime).
Pelo menos 2 relatórios/consultas com filtro (ex.: listar todos os registros de um período, calcular um total etc.).
Uso de funções para organizar o código (evitar todo o programa em um único bloco).

⭐ Diferenciais (pontuação extra)
Persistência de dados em arquivo (.json, .csv ou .txt).
Tratamento de exceções (try / except).
Interface organizada e amigável no terminal.
Código comentado e bem identado.

1. Contexto
   Vocês foram contratados para desenvolver um sistema que ajude uma pequena clínica médica a organizar seus atendimentos, pacientes e profissionais de saúde. O software deverá ser escrito em Python e deverá funcionar em linha de comando (CLI) ou com uma interface gráfica simples (Tkinter, PySimpleGUI ou semelhantes).

2. Objetivos Principais
   Cadastro de Pacientes

Nome completo, data de nascimento, CPF, telefone, convênio (opcional) e histórico clínico resumido.
Funções: inserir, listar, buscar (por nome ou CPF), atualizar e excluir.
Cadastro de Profissionais

Nome completo, CRM/COREN, especialidade, telefone, agenda de atendimento (dias + horários).
Funções: inserir, listar, buscar, atualizar e excluir.
Agendamento de Consultas

Selecionar paciente, profissional, data e horário.
Verificar conflitos de agenda automaticamente.
Funções: marcar, remarcar, cancelar e listar consultas futuras ou passadas.
Prontuário Simplificado

Após cada consulta, registrar data, sintomas, diagnóstico, prescrição e observações.
Vincular o prontuário ao paciente e ao profissional.