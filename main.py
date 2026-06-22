import services
from datetime import datetime

# ==================== FUNÇÕES DE VALIDAÇÃO ====================

def validar_idade(texto):
    """Valida se a idade é um número inteiro não negativo."""
    try:
        valor = int(texto)
        if valor < 0:
            return None
        return valor
    except ValueError:
        return None

def validar_float(texto):
    """Valida se o valor é um número decimal válido."""
    try:
        valor = float(texto)
        if valor < 0:
            return None
        return valor
    except ValueError:
        return None

def validar_data_hora(texto):
    """Valida se a string está no formato DD/MM/YYYY HH:MM."""
    try:
        datetime.strptime(texto, "%d/%m/%Y %H:%M")
        return True
    except ValueError:
        return False

def validar_tipo_atendimento(texto):
    """Valida se o tipo é 'particular' ou 'convenio'."""
    return texto.lower() in ["particular", "convenio"]

def validar_sim_nao(texto):
    """Valida resposta s/n e retorna True/False ou None se inválido."""
    if texto.lower() == "s":
        return True
    elif texto.lower() == "n":
        return False
    return None

# ==================== FUNÇÕES DE EXIBIÇÃO ====================

def exibir_paciente(paciente):
    """Exibe os dados de um paciente formatado."""
    print(f"  ID: {paciente['id']}")
    print(f"  Nome: {paciente['nome']}")
    print(f"  Idade: {paciente['idade']} anos")
    print(f"  Telefone: {paciente['telefone']}")
    print(f"  Atendimento: {paciente['tipo_atendimento']}")

def exibir_medico(medico):
    """Exibe os dados de um médico formatado."""
    status = "ativo" if medico["ativo"] else "afastado"
    print(f"  ID: {medico['id']}")
    print(f"  Nome: {medico['nome']}")
    print(f"  Especialidade: {medico['especialidade']}")
    print(f"  Documento: {medico['documentacao']}")
    print(f"  Telefone: {medico['telefone']}")
    print(f"  Status: {status}")

def exibir_consulta(consulta):
    """Exibe os dados de uma consulta formatado."""
    primeira = "Sim" if consulta["primeira_consulta"] else "Não"
    print(f"  ID: {consulta['id']}")
    print(f"  Paciente: {consulta['paciente_nome']}")
    print(f"  Médico: {consulta['medico_nome']} ({consulta['especialidade']})")
    print(f"  Data/Hora: {consulta['data_hora']}")
    print(f"  Tipo: {consulta['tipo_atendimento']}")
    print(f"  Primeira consulta: {primeira}")
    print(f"  Status: {consulta['status']}")
    print(f"  Valor: R$ {consulta['valor_total']:.2f}")

def exibir_prontuario(prontuario):
    """Exibe os dados de um prontuário formatado."""
    print(f"  ID: {prontuario['id']}")
    print(f"  Paciente: {prontuario['paciente_nome']}")
    print(f"  Médico: {prontuario['medico_nome']}")
    print(f"  Data conclusão: {prontuario['data_conclusao']}")
    print(f"  Observações: {prontuario['observacoes']}")
    print(f"  Procedimentos:")
    for proc in prontuario["procedimentos"]:
        print(f"    - {proc['nome']}: R$ {proc['valor']:.2f}")
    print(f"  Total procedimentos: R$ {prontuario['valor_procedimentos']:.2f}")


# ==================== MENU PRINCIPAL ====================

def menu_principal():
    while True:
        print("\n========================================")
        print("       SISTEMA CLÍNICA VIDA+")
        print("========================================")
        print("1. Pacientes")
        print("2. Médicos")
        print("3. Consultas")
        print("4. Prontuários")
        print("5. Relatórios")
        print("0. Sair")
        print("========================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_pacientes()
        elif opcao == "2":
            menu_medicos()
        elif opcao == "3":
            menu_consultas()
        elif opcao == "4":
            menu_prontuarios()
        elif opcao == "5":
            menu_relatorios()
        elif opcao == "0":
            print("Encerrando sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# ==================== PONTO DE ENTRADA ====================

if __name__ == "__main__":
    print("Inicializando sistema...")
    services.inicializar()
    print("Dados carregados com sucesso.")
    menu_principal()

# ==================== MENU PACIENTES ====================

def menu_pacientes():
    while True:
        print("\n=== PACIENTES ===")
        print("1. Cadastrar paciente")
        print("2. Listar pacientes")
        print("3. Buscar paciente por nome")
        print("4. Atualizar paciente")
        print("5. Remover paciente")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_paciente()
        elif opcao == "2":
            listar_pacientes()
        elif opcao == "3":
            buscar_paciente()
        elif opcao == "4":
            atualizar_paciente()
        elif opcao == "5":
            remover_paciente()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def cadastrar_paciente():
    print("\n--- CADASTRAR PACIENTE ---")

    nome = input("Nome: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return

    idade = None
    while idade is None:
        idade = validar_idade(input("Idade: ").strip())
        if idade is None:
            print("Idade inválida. Digite um número inteiro não negativo.")

    telefone = input("Telefone: ").strip()
    if not telefone:
        print("Telefone não pode ser vazio.")
        return

    tipo = None
    while tipo is None:
        tipo = input("Tipo de atendimento (particular/convenio): ").strip().lower()
        if not validar_tipo_atendimento(tipo):
            print("Tipo inválido. Digite 'particular' ou 'convenio'.")
            tipo = None

    paciente = services.cadastrar_paciente(nome, idade, telefone, tipo)
    print(f"\nPaciente cadastrado com sucesso!")
    exibir_paciente(paciente)

def listar_pacientes():
    print("\n--- LISTA DE PACIENTES ---")

    pacientes = services.listar_pacientes()

    if len(pacientes) == 0:
        print("Nenhum paciente cadastrado.")
        return

    for paciente in pacientes:
        print("-" * 30)
        exibir_paciente(paciente)
    print("-" * 30)
    print(f"Total: {len(pacientes)} paciente(s).")

def buscar_paciente():
    print("\n--- BUSCAR PACIENTE ---")

    termo = input("Digite o nome para buscar: ").strip()
    if not termo:
        print("Termo de busca vazio.")
        return

    encontrados = services.buscar_pacientes_por_nome(termo)

    if len(encontrados) == 0:
        print(f"Nenhum paciente encontrado com '{termo}'.")
        return

    print(f"\n{len(encontrados)} resultado(s):")
    for paciente in encontrados:
        print("-" * 30)
        exibir_paciente(paciente)
    print("-" * 30)

def atualizar_paciente():
    print("\n--- ATUALIZAR PACIENTE ---")

    listar_pacientes()

    try:
        id_paciente = int(input("Digite o ID do paciente a atualizar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    paciente = services.buscar_paciente_por_id(id_paciente)
    if paciente is None:
        print("Paciente não encontrado.")
        return

    print("\nDados atuais:")
    exibir_paciente(paciente)
    print("\nDigite os novos dados (Enter para manter o atual):")

    novo_nome = input(f"Nome [{paciente['nome']}]: ").strip()
    if not novo_nome:
        novo_nome = paciente["nome"]

    nova_idade_str = input(f"Idade [{paciente['idade']}]: ").strip()
    if not nova_idade_str:
        nova_idade = paciente["idade"]
    else:
        nova_idade = validar_idade(nova_idade_str)
        if nova_idade is None:
            print("Idade inválida. Atualização cancelada.")
            return

    novo_telefone = input(f"Telefone [{paciente['telefone']}]: ").strip()
    if not novo_telefone:
        novo_telefone = paciente["telefone"]

    novo_tipo = input(f"Tipo de atendimento [{paciente['tipo_atendimento']}]: ").strip().lower()
    if not novo_tipo:
        novo_tipo = paciente["tipo_atendimento"]
    elif not validar_tipo_atendimento(novo_tipo):
        print("Tipo inválido. Atualização cancelada.")
        return

    sucesso, mensagem = services.atualizar_paciente(
        id_paciente, novo_nome, nova_idade, novo_telefone, novo_tipo
    )
    print(mensagem)

def remover_paciente():
    print("\n--- REMOVER PACIENTE ---")

    listar_pacientes()

    try:
        id_paciente = int(input("Digite o ID do paciente a remover: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    paciente = services.buscar_paciente_por_id(id_paciente)
    if paciente is None:
        print("Paciente não encontrado.")
        return

    print("\nPaciente encontrado:")
    exibir_paciente(paciente)

    confirmacao = input("\nTem certeza que deseja remover? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Remoção cancelada.")
        return

    services.deletar_paciente(id_paciente)
    print("Paciente removido com sucesso.")

# ==================== MENU MÉDICOS ====================

def menu_medicos():
    while True:
        print("\n=== MÉDICOS ===")
        print("1. Cadastrar médico")
        print("2. Listar médicos ativos")
        print("3. Listar todos os médicos")
        print("4. Buscar por especialidade")
        print("5. Atualizar médico")
        print("6. Afastar médico")
        print("7. Reativar médico")
        print("8. Remover médico permanentemente")
        print("0. Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_medico()
        elif opcao == "2":
            listar_medicos(apenas_ativos=True)
        elif opcao == "3":
            listar_medicos(apenas_ativos=False)
        elif opcao == "4":
            buscar_medico_por_especialidade()
        elif opcao == "5":
            atualizar_medico()
        elif opcao == "6":
            afastar_medico()
        elif opcao == "7":
            reativar_medico()
        elif opcao == "8":
            remover_medico()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def cadastrar_medico():
    print("\n--- CADASTRAR MÉDICO ---")

    nome = input("Nome: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return

    print("\nEspecialidades disponíveis:", ", ".join(services.PRECOS.keys()))
    especialidade = input("Especialidade: ").strip().lower()
    if not especialidade:
        print("Especialidade não pode ser vazia.")
        return

    documentacao = input("Documento (CRM/CPF/RG): ").strip()
    if not documentacao:
        print("Documento não pode ser vazio.")
        return

    telefone = input("Telefone: ").strip()
    if not telefone:
        print("Telefone não pode ser vazio.")
        return

    medico = services.cadastrar_medico(nome, especialidade, documentacao, telefone)
    print("\nMédico cadastrado com sucesso!")
    exibir_medico(medico)

def listar_medicos(apenas_ativos=True):
    if apenas_ativos:
        print("\n--- MÉDICOS ATIVOS ---")
    else:
        print("\n--- TODOS OS MÉDICOS ---")

    medicos = services.listar_medicos(apenas_ativos)

    if len(medicos) == 0:
        print("Nenhum médico encontrado.")
        return

    for medico in medicos:
        print("-" * 30)
        exibir_medico(medico)
    print("-" * 30)
    print(f"Total: {len(medicos)} médico(s).")

def buscar_medico_por_especialidade():
    print("\n--- BUSCAR POR ESPECIALIDADE ---")

    print("Especialidades disponíveis:", ", ".join(services.PRECOS.keys()))
    especialidade = input("Especialidade: ").strip().lower()
    if not especialidade:
        print("Especialidade não pode ser vazia.")
        return

    encontrados = services.buscar_medicos_por_especialidade(especialidade)

    if len(encontrados) == 0:
        print(f"Nenhum médico ativo encontrado para '{especialidade}'.")
        return

    print(f"\n{len(encontrados)} resultado(s):")
    for medico in encontrados:
        print("-" * 30)
        exibir_medico(medico)
    print("-" * 30)

def atualizar_medico():
    print("\n--- ATUALIZAR MÉDICO ---")

    listar_medicos(apenas_ativos=False)

    try:
        id_medico = int(input("Digite o ID do médico a atualizar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    medico = services.buscar_medico_por_id(id_medico)
    if medico is None:
        print("Médico não encontrado.")
        return

    print("\nDados atuais:")
    exibir_medico(medico)
    print("\nDigite os novos dados (Enter para manter o atual):")

    novo_nome = input(f"Nome [{medico['nome']}]: ").strip()
    if not novo_nome:
        novo_nome = medico["nome"]

    print("Especialidades disponíveis:", ", ".join(services.PRECOS.keys()))
    nova_especialidade = input(f"Especialidade [{medico['especialidade']}]: ").strip().lower()
    if not nova_especialidade:
        nova_especialidade = medico["especialidade"]

    nova_documentacao = input(f"Documento [{medico['documentacao']}]: ").strip()
    if not nova_documentacao:
        nova_documentacao = medico["documentacao"]

    novo_telefone = input(f"Telefone [{medico['telefone']}]: ").strip()
    if not novo_telefone:
        novo_telefone = medico["telefone"]

    sucesso, mensagem = services.atualizar_medico(
        id_medico, novo_nome, nova_especialidade, nova_documentacao, novo_telefone
    )
    print(mensagem)

def afastar_medico():
    print("\n--- AFASTAR MÉDICO ---")

    listar_medicos(apenas_ativos=True)

    try:
        id_medico = int(input("Digite o ID do médico a afastar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    medico = services.buscar_medico_por_id(id_medico)
    if medico is None:
        print("Médico não encontrado.")
        return

    print("\nMédico encontrado:")
    exibir_medico(medico)

    confirmacao = input("\nConfirma o afastamento? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada.")
        return

    sucesso, mensagem = services.afastar_medico(id_medico)
    print(mensagem)

def reativar_medico():
    print("\n--- REATIVAR MÉDICO ---")

    listar_medicos(apenas_ativos=False)

    try:
        id_medico = int(input("Digite o ID do médico a reativar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    medico = services.buscar_medico_por_id(id_medico)
    if medico is None:
        print("Médico não encontrado.")
        return

    if medico["ativo"] == True:
        print("Médico já está ativo.")
        return

    sucesso, mensagem = services.reativar_medico(id_medico)
    print(mensagem)

def remover_medico():
    print("\n--- REMOVER MÉDICO PERMANENTEMENTE ---")
    print("Atenção: use 'Afastar' para preservar histórico de consultas.")

    listar_medicos(apenas_ativos=False)

    try:
        id_medico = int(input("Digite o ID do médico a remover: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    medico = services.buscar_medico_por_id(id_medico)
    if medico is None:
        print("Médico não encontrado.")
        return

    print("\nMédico encontrado:")
    exibir_medico(medico)

    confirmacao = input("\nTem certeza? Essa ação não pode ser desfeita. (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Remoção cancelada.")
        return

    services.deletar_medico(id_medico)
    print("Médico removido permanentemente.")