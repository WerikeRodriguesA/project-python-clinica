import json
import os
import traceback

DB_FILE = "pacientes.json"
MED_FILE = "medicos.json"

pacientes = []
medicos = []

def carregar(arquivo):
    if not os.path.exists(arquivo):
        return []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, ValueError):
        return []
    except Exception:
        return []

def salvar(arquivo, dados):
    
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar {arquivo}: {e}")

def validar_idade(text):
    try:
        v = int(text)
        if v < 0:
            return None
        return v
    except Exception:
        return None

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

def listar_medicos():
    if not medicos:
        print("Nenhum médico cadastrado.")
        return
    print("\n=== LISTA DE MÉDICOS ===")
    for i, m in enumerate(medicos, start=1):
        print(f"{i}. {m.get('nome','-')} - {m.get('especialidade','-')} - {m.get('documentacao','-')} - {m.get('telefone','-')}")
    print()

def listar_pacientes():
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return
    print("\n=== LISTA DE PACIENTES ===")
    for i, p in enumerate(pacientes, start=1):
        print(f"{i}. {p.get('nome','-')} - {p.get('idade','-')} anos - {p.get('telefone','-')}")
    print()

def mostrar_estatisticas():
    if not pacientes:
        print("Nenhum paciente cadastrado.")
        return

    try:
        total = len(pacientes)
        idade_media = sum(p["idade"] for p in pacientes) / total
        mais_novo = min(pacientes, key=lambda x: x["idade"])
        mais_velho = max(pacientes, key=lambda x: x["idade"])

        print(f"\nTotal de pacientes: {total}")
        print(f"Idade média: {idade_media:.2f}")
        print(f"Paciente mais novo: {mais_novo.get('nome','-')} ({mais_novo.get('idade','-')} anos)")
        print(f"Paciente mais velho: {mais_velho.get('nome','-')} ({mais_velho.get('idade','-')} anos)\n")
    except Exception as e:
        print("Erro ao calcular estatísticas:", e)

def buscar_paciente():
    termo = input("Digite o nome para buscar: ").strip().lower()
    if not termo:
        print("Termo de busca vazio.")
        return
    achados = [p for p in pacientes if termo in p.get("nome","").lower()]
    if not achados:
        print("Paciente não encontrado.")
        return
    print(f"{len(achados)} resultado(s):")
    for p in achados:
        print(f"- {p.get('nome','-')} - {p.get('idade','-')} anos - {p.get('telefone','-')}")

def consulta_normal(A, B, C, D):
    return (A and B and C) or (B and C and D)

def emergencia(A, B, C, D):
    return C and (B or D)

def sistema_acesso():
    print("\n=== Sistema de Controle de Acesso - Clínica Vida+ ===")

    A = input("Tem agendamento? (s/n): ").strip().lower() == "s"
    B = input("Documentos OK? (s/n): ").strip().lower() == "s"
    C = input("Médico disponível? (s/n): ").strip().lower() == "s"
    D = input("Pagamentos em dia? (s/n): ").strip().lower() == "s"

    resultado_CN = consulta_normal(A, B, C, D)
    resultado_EM = emergencia(A, B, C, D)

    print("\n--- RESULTADOS ---")
    print(f"Consulta Normal: {'ATENDENDO' if resultado_CN else 'SEM ATENDIMENTO'}")
    print(f"Emergência: {'ATENDENDO' if resultado_EM else 'SEM ATENDIMENTO'}")
    print()

def menu():
    while True:
        print("=== SISTEMA CLÍNICA VIDA+ ===")
        print("1. Cadastrar paciente")
        print("2. Cadastrar médico")
        print("3. Ver estatísticas")
        print("4. Buscar paciente")
        print("5. Listar pacientes")
        print("6. Listar médicos")
        print("7. Sistema de Controle de Acesso")
        print("8. Sair")

        opc = input("Escolha uma opção: ").strip()

        if opc == "1":
            cadastrar_paciente()
        elif opc == "2":
            cadastrar_medico()
        elif opc == "3":
            mostrar_estatisticas()
        elif opc == "4":
            buscar_paciente()
        elif opc == "5":
            listar_pacientes()
        elif opc == "6":
            listar_medicos()
        elif opc == "7":
            sistema_acesso()
        elif opc == "8":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    try:
        pacientes = carregar(DB_FILE)
        medicos = carregar(MED_FILE)
        menu()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
    except Exception:
        print("Ocorreu um erro inesperado. Trace abaixo:")
        traceback.print_exc()
