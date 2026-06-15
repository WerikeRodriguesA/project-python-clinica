import json
import os

DB_FILE = "pacientes.json"
MED_FILE = "medicos.json"

pacientes = []
medicos = []

# ------------------ FUNÇÕES DE ARQUIVO ------------------

def carregar(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ------------------ FUNÇÕES AUXILIARES ------------------

def validar_idade(text):
    try:
        v = int(text)
        if v < 0:
            raise ValueError
        return v
    except ValueError:
        return None

# ------------------ CADASTRO PACIENTES ------------------

def cadastrar_paciente():
    nome = input("Nome do paciente: ").strip()
    if not nome:
        print("Nome inválido.")
        return

    idade = None
    while idade is None:
        idade_in = input("Idade: ").strip()
        idade = validar_idade(idade_in)
        if idade is None:
            print("Idade inválida. Digite um número inteiro não negativo.")

    telefone = input("Telefone: ").strip()

    paciente = {"nome": nome, "idade": idade, "telefone": telefone}
    pacientes.append(paciente)
    salvar(DB_FILE, pacientes)
    print("Paciente cadastrado com sucesso!")

# ------------------ CADASTRO MÉDICOS ------------------

def cadastrar_medico():
    nome = input("Nome do médico: ").strip()
    if not nome:
        print("Nome inválido.")
        return

    especialidade = input("Especialidade: ").strip()
    if not especialidade:
        print("Especialidade inválida.")
        return

    documentacao = input("Documento (CRM/CPF/RG): ").strip()
    if not documentacao:
        print("Documentação inválida.")
        return

    telefone = input("Telefone: ").strip()

    medico = {
        "nome": nome,
        "especialidade": especialidade,
        "documentacao": documentacao,
        "telefone": telefone
    }
    medicos.append(medico)
    salvar(MED_FILE, medicos)
    print("Médico cadastrado com sucesso!")

# ------------------ LISTAGENS ------------------

def listar_medicos():
    if not medicos:
        print("Nenhum médico cadastrado.")
        return
    print("\n=== LISTA DE MÉDICOS ===")
    for i, m in enumerate(medicos, start=1):
        print(f"{i}. {m['nome']} - {m['especialidade']} - {m['documentacao']} - {m['telefone']}")
    print()

def listar_pacientes():
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return
    print("\n=== LISTA DE PACIENTES ===")
    for i, p in enumerate(pacientes, start=1):
        print(f"{i}. {p['nome']} - {p['idade']} anos - {p['telefone']}")
    print()

# ------------------ ESTATÍSTICAS PACIENTES ------------------

def mostrar_estatisticas():
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return

    total = len(pacientes)
    idade_media = sum(p["idade"] for p in pacientes) / total
    mais_novo = min(pacientes, key=lambda x: x["idade"])
    mais_velho = max(pacientes, key=lambda x: x["idade"])

    print(f"\nTotal de pacientes: {total}")
    print(f"Idade média: {idade_media:.2f}")
    print(f"Paciente mais novo: {mais_novo['nome']} ({mais_novo['idade']} anos)")
    print(f"Paciente mais velho: {mais_velho['nome']} ({mais_velho['idade']} anos)\n")

# ------------------ BUSCA ------------------

def buscar_paciente():
    if not pacientes:
        print("Nenhum paciente cadastrado para buscar.")
        return

    termo = input("Digite o nome para busca: ").strip().lower()
    if not termo:
        print("Termo de busca inválido.")
        return

    encontrados = [p for p in pacientes if termo in p['nome'].lower()]

    if encontrados:
        print(f"\n=== PACIENTES ENCONTRADOS PARA '{termo}' ===")
        for i, p in enumerate(encontrados, start=1):
            print(f"{i}. {p['nome']} - {p['idade']} anos - {p['telefone']}")
        print()
    else:
        print(f"Nenhum paciente encontrado com o nome '{termo}'.")    