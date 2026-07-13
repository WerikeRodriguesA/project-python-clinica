import database
from datetime import datetime
import os

# Define a pasta base onde os arquivos de persistência serão salvos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Arquivos de persistência
PACIENTES_FILE = os.path.join(BASE_DIR, "pacientes.json")
MEDICOS_FILE = os.path.join(BASE_DIR, "medicos.json")
CONSULTAS_FILE = os.path.join(BASE_DIR, "consultas.json")
PRONTUARIOS_FILE = os.path.join(BASE_DIR, "prontuarios.json")

# Dados em memória — carregados uma vez na inicialização
pacientes = []
medicos = []
consultas = []
prontuarios = []

# Tabela de preços base por especialidade
PRECOS = {
    "clinico geral": 150.0,
    "dentista": 200.0,
    "cardiologista": 300.0,
    "dermatologista": 250.0,
    "ortopedista": 280.0,
}

# Desconto para convênio e retorno
DESCONTO_CONVENIO = 0.30   # 30% de desconto
DESCONTO_RETORNO = 0.50    # 50% de desconto
PRAZO_RETORNO_DIAS = 30    # retorno gratuito dentro de 30 dias
MULTA_FALTA = 50.0         # multa por falta sem aviso

def inicializar():
    global pacientes, medicos, consultas, prontuarios
    pacientes = database.carregar(PACIENTES_FILE)
    medicos = database.carregar(MEDICOS_FILE)
    consultas = database.carregar(CONSULTAS_FILE)
    prontuarios = database.carregar(PRONTUARIOS_FILE)
    
def gerar_id(lista):
    """Gera um ID numérico único baseado no maior ID já existente na lista."""
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1

def calcular_valor(especialidade, tipo_atendimento, primeira_consulta):
    """
    Calcula o valor da consulta com base em três fatores:
    - especialidade: define o preço base
    - tipo_atendimento: 'particular' ou 'convenio' (convenio tem desconto)
    - primeira_consulta: True ou False (retorno tem desconto)
    """
    especialidade = especialidade.lower()

    if especialidade in PRECOS:
        valor = PRECOS[especialidade]
    else:
        valor = 180.0  # preço padrão para especialidades não mapeadas

    if tipo_atendimento == "convenio":
        valor = valor - (valor * DESCONTO_CONVENIO)

    if primeira_consulta == False:
        valor = valor - (valor * DESCONTO_RETORNO)

    return valor

def verificar_conflito(medico_nome, data_hora_str):
    """Verifica se já existe uma consulta agendada para o médico no mesmo horário."""
    for consulta in consultas:
        if consulta["medico_nome"] == medico_nome and consulta["data_hora"] == data_hora_str and consulta["status"] == "agendada":
            return True
    return False

def str_para_datetime(data_hora_str):
    """Converte string 'DD/MM/YYYY HH:MM' para objeto datetime."""
    try:
        return datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
    except ValueError:
        return None

def datetime_para_str(dt):
    #Converte objeto datetime para string 'DD/MM/YYYY HH:MM'.
    return dt.strftime("%d/%m/%Y %H:%M")

# ==================== PACIENTES ====================

def cadastrar_paciente(nome, idade, telefone, tipo_atendimento):
    """Cria um novo paciente e salva no arquivo."""
    paciente = {
        "id": gerar_id(pacientes),
        "nome": nome,
        "idade": idade,
        "telefone": telefone,
        "tipo_atendimento": tipo_atendimento  # 'particular' ou 'convenio'
    }
    pacientes.append(paciente)
    database.salvar(PACIENTES_FILE, pacientes)
    return paciente

def listar_pacientes():
    """Retorna a lista completa de pacientes."""
    return pacientes

def buscar_paciente_por_id(id_buscado):
    """Busca um paciente pelo ID. Retorna o paciente ou None."""
    for paciente in pacientes:
        if paciente["id"] == id_buscado:
            return paciente
    return None

def buscar_pacientes_por_nome(termo):
    """Busca pacientes cujo nome contenha o termo informado."""
    termo = termo.lower()
    encontrados = [p for p in pacientes if termo in p["nome"].lower()]
    return encontrados

def atualizar_paciente(id_paciente, novo_nome, nova_idade, novo_telefone, novo_tipo):
    """
    Atualiza os dados de um paciente existente.
    Retorna True e uma mensagem se encontrou e atualizou, False e uma mensagem se não encontrou.
    """
    for paciente in pacientes:
        if paciente["id"] == id_paciente:
            paciente["nome"] = novo_nome
            paciente["idade"] = nova_idade
            paciente["telefone"] = novo_telefone
            paciente["tipo_atendimento"] = novo_tipo
            database.salvar(PACIENTES_FILE, pacientes)
            return True, "Paciente atualizado com sucesso."
    return False, "Paciente não encontrado."

def deletar_paciente(id_paciente):
    """
    Remove um paciente da lista.
    Retorna True se removeu, False se não encontrou.
    """
    for paciente in pacientes:
        if paciente["id"] == id_paciente:
            pacientes.remove(paciente)
            database.salvar(PACIENTES_FILE, pacientes)
            return True
    return False

# ==================== MÉDICOS ====================

def cadastrar_medico(nome, especialidade, documentacao, telefone):
    """Cria um novo médico e salva no arquivo."""
    medico = {
        "id": gerar_id(medicos),
        "nome": nome,
        "especialidade": especialidade,
        "documentacao": documentacao,
        "telefone": telefone,
        "ativo": True  # médico pode ser afastado sem ser deletado
    }
    medicos.append(medico)
    database.salvar(MEDICOS_FILE, medicos)
    return medico

def listar_medicos(apenas_ativos=True):
    """
    Retorna médicos. Por padrão retorna apenas os ativos.
    Passando apenas_ativos=False retorna todos.
    """
    if apenas_ativos:
        ativos = [m for m in medicos if m["ativo"] == True]
        return ativos
    return medicos

def buscar_medico_por_id(id_buscado):
    """Busca um médico pelo ID. Retorna o médico ou None."""
    for medico in medicos:
        if medico["id"] == id_buscado:
            return medico
    return None

def buscar_medicos_por_especialidade(especialidade):
    """Retorna todos os médicos ativos de uma especialidade."""
    especialidade = especialidade.lower()
    encontrados = [m for m in medicos if m["especialidade"].lower() == especialidade and m["ativo"] == True]
    return encontrados

def atualizar_medico(id_medico, novo_nome, nova_especialidade, nova_documentacao, novo_telefone):
    """Atualiza dados de um médico. Retorna True e mensagem se atualizou."""
    for medico in medicos:
        if medico["id"] == id_medico:
            medico["nome"] = novo_nome
            medico["especialidade"] = nova_especialidade
            medico["documentacao"] = nova_documentacao
            medico["telefone"] = novo_telefone
            database.salvar(MEDICOS_FILE, medicos)
            return True, "Médico atualizado com sucesso."
    return False, "Médico não encontrado."

def afastar_medico(id_medico):
    """
    Marca um médico como inativo (afastado).
    Não deleta — preserva histórico de consultas.
    Retorna True e mensagem se encontrou e afastou.
    """
    for medico in medicos:
        if medico["id"] == id_medico:
            medico["ativo"] = False
            database.salvar(MEDICOS_FILE, medicos)
            return True, "Médico afastado com sucesso."
    return False, "Médico não encontrado."

def reativar_medico(id_medico):
    """Reativa um médico afastado. Retorna True e mensagem se encontrou."""
    for medico in medicos:
        if medico["id"] == id_medico:
            medico["ativo"] = True
            database.salvar(MEDICOS_FILE, medicos)
            return True, "Médico reativado com sucesso."
    return False, "Médico não encontrado."

def deletar_medico(id_medico):
    """
    Remove permanentemente um médico.
    Use afastar_medico() quando quiser preservar histórico.
    """
    for medico in medicos:
        if medico["id"] == id_medico:
            medicos.remove(medico)
            database.salvar(MEDICOS_FILE, medicos)
            return True
    return False

# ==================== CONSULTAS ====================

def agendar_consulta(paciente_id, medico_id, data_hora_str, primeira_consulta):
    """
    Agenda uma nova consulta verificando conflito de horário.
    Retorna a consulta criada ou None se houver conflito ou dados inválidos.
    """
    paciente = buscar_paciente_por_id(paciente_id)
    if paciente is None:
        return None, "Paciente não encontrado."

    medico = buscar_medico_por_id(medico_id)
    if medico is None:
        return None, "Médico não encontrado."

    if medico["ativo"] == False:
        return None, "Médico está afastado e não pode receber consultas."

    data_hora = str_para_datetime(data_hora_str)
    if data_hora is None:
        return None, "Data/hora inválida. Use o formato DD/MM/YYYY HH:MM."

    if verificar_conflito(medico["nome"], data_hora_str):
        return None, "Conflito de horário: esse médico já tem consulta nesse horário."

    valor = calcular_valor(
        medico["especialidade"],
        paciente["tipo_atendimento"],
        primeira_consulta
    )

    consulta = {
        "id": gerar_id(consultas),
        "paciente_id": paciente_id,
        "paciente_nome": paciente["nome"],
        "medico_id": medico_id,
        "medico_nome": medico["nome"],
        "especialidade": medico["especialidade"],
        "data_hora": data_hora_str,
        "tipo_atendimento": paciente["tipo_atendimento"],
        "primeira_consulta": primeira_consulta,
        "status": "agendada",
        "valor_total": valor
    }

    consultas.append(consulta)
    database.salvar(CONSULTAS_FILE, consultas)
    return consulta, "Consulta agendada com sucesso."

def listar_consultas():
    """Retorna todas as consultas."""
    return consultas

def buscar_consulta_por_id(id_buscado):
    """Busca uma consulta pelo ID. Retorna a consulta ou None."""
    for consulta in consultas:
        if consulta["id"] == id_buscado:
            return consulta
    return None

def buscar_consultas_por_paciente(paciente_id):
    """Retorna todas as consultas de um paciente específico."""
    encontradas = [c for c in consultas if c["paciente_id"] == paciente_id]
    return encontradas

def buscar_consultas_por_medico(medico_id):
    """Retorna todas as consultas de um médico específico."""
    encontradas = [c for c in consultas if c["medico_id"] == medico_id]
    return encontradas

def buscar_consultas_por_periodo(data_inicio_str, data_fim_str):
    """
    Retorna consultas dentro de um período.
    data_inicio_str e data_fim_str no formato 'DD/MM/YYYY HH:MM'.
    """
    data_inicio = str_para_datetime(data_inicio_str)
    data_fim = str_para_datetime(data_fim_str)

    if data_inicio is None or data_fim is None:
        return []

    encontradas = []
    for consulta in consultas:
        data_consulta = str_para_datetime(consulta["data_hora"])
        if data_consulta is None:
            continue
        if data_consulta >= data_inicio and data_consulta <= data_fim:
            encontradas.append(consulta)

    return encontradas

def concluir_consulta(consulta_id):
    """
    Marca uma consulta como concluída e registra a data/hora atual.
    Retorna True se concluiu, False se não encontrou ou já estava concluída.
    """
    for consulta in consultas:
        if consulta["id"] == consulta_id:
            if consulta["status"] != "agendada":
                return False, "Consulta não está com status 'agendada'."
            consulta["status"] = "concluida"
            consulta["data_conclusao"] = datetime_para_str(datetime.now())
            database.salvar(CONSULTAS_FILE, consultas)
            return True, "Consulta concluída com sucesso."
    return False, "Consulta não encontrada."

def registrar_falta(consulta_id):
    """Registra falta do paciente e aplica multa somando ao valor da consulta."""
    for consulta in consultas:
        if consulta["id"] == consulta_id:
            if consulta["status"] != "agendada":
                return False, "Consulta não está com status 'agendada'."
            consulta["status"] = "falta"
            consulta["valor_total"] += MULTA_FALTA
            consulta["data_falta"] = datetime_para_str(datetime.now())
            database.salvar(CONSULTAS_FILE, consultas)
            return True, f"Falta registrada. Multa de R$ {MULTA_FALTA:.2f} aplicada."
    return False, "Consulta não encontrada."

def cancelar_consulta(consulta_id):
    """
    Cancela uma consulta agendada.
    Não deleta — mantém histórico com status 'cancelada'.
    """
    for consulta in consultas:
        if consulta["id"] == consulta_id:
            if consulta["status"] != "agendada":
                return False, "Só é possível cancelar consultas com status 'agendada'."
            consulta["status"] = "cancelada"
            database.salvar(CONSULTAS_FILE, consultas)
            return True, "Consulta cancelada."
    return False, "Consulta não encontrada."

def deletar_consulta(consulta_id):
    """Remove permanentemente uma consulta. Use com cautela."""
    for consulta in consultas:
        if consulta["id"] == consulta_id:
            consultas.remove(consulta)
            database.salvar(CONSULTAS_FILE, consultas)
            return True
    return False
# ==================== PRONTUÁRIOS ====================

def criar_prontuario(consulta_id, procedimentos, observacoes):
    """Cria um prontuário de consulta concluída, calculando custos adicionais."""
    consulta = buscar_consulta_por_id(consulta_id)
    if consulta is None:
        return None, "Consulta não encontrada."
    if consulta["status"] != "concluida":
        return None, "Só é possível criar prontuário para consultas concluídas."

    valor_procedimentos = sum(p["valor"] for p in procedimentos)

    prontuario = {
        "id": gerar_id(prontuarios),
        "consulta_id": consulta_id,
        "paciente_id": consulta["paciente_id"],
        "paciente_nome": consulta["paciente_nome"],
        "medico_nome": consulta["medico_nome"],
        "data_conclusao": consulta["data_conclusao"],
        "procedimentos": procedimentos,
        "valor_procedimentos": valor_procedimentos,
        "observacoes": observacoes
    }

    consulta["valor_total"] += valor_procedimentos
    database.salvar(CONSULTAS_FILE, consultas)

    prontuarios.append(prontuario)
    database.salvar(PRONTUARIOS_FILE, prontuarios)
    return prontuario, "Prontuário criado com sucesso."
def buscar_prontuario_por_paciente(paciente_id):
    """Retorna todos os prontuários de um paciente."""
    encontrados = [p for p in prontuarios if p["paciente_id"] == paciente_id]
    return encontrados

def listar_prontuarios():
    """Retorna todos os prontuários."""
    return prontuarios

def buscar_prontuario_por_id(id_buscado):
    """Busca prontuário pelo ID."""
    for prontuario in prontuarios:
        if prontuario["id"] == id_buscado:
            return prontuario
    return None

def atualizar_prontuario(prontuario_id, novos_procedimentos, novas_observacoes):
    """Atualiza procedimentos e observações do prontuário, recalculando valores."""
    for prontuario in prontuarios:
        if prontuario["id"] == prontuario_id:
            valor_antigo = prontuario["valor_procedimentos"]
            novo_valor = sum(p["valor"] for p in novos_procedimentos)

            prontuario["procedimentos"] = novos_procedimentos
            prontuario["observacoes"] = novas_observacoes
            prontuario["valor_procedimentos"] = novo_valor

            consulta = buscar_consulta_por_id(prontuario["consulta_id"])
            if consulta is not None:
                consulta["valor_total"] = consulta["valor_total"] - valor_antigo + novo_valor
                database.salvar(CONSULTAS_FILE, consultas)

            database.salvar(PRONTUARIOS_FILE, prontuarios)
            return True, "Prontuário atualizado."
    return False, "Prontuário não encontrado."

def deletar_prontuario(prontuario_id):
    """Remove um prontuário permanentemente."""
    for prontuario in prontuarios:
        if prontuario["id"] == prontuario_id:
            prontuarios.remove(prontuario)
            database.salvar(PRONTUARIOS_FILE, prontuarios)
            return True
    return False

# ==================== RELATÓRIOS ====================

def relatorio_consultas_por_periodo(data_inicio_str, data_fim_str):
    """Relatório 1: Lista todas as consultas de um período com total arrecadado."""
    encontradas = buscar_consultas_por_periodo(data_inicio_str, data_fim_str)
    total = sum(c["valor_total"] for c in encontradas if c["status"] == "concluida")
    return encontradas, total

def relatorio_consultas_por_medico(medico_id):
    """Relatório 2: Lista todas as consultas de um médico com contagem por status."""
    encontradas = buscar_consultas_por_medico(medico_id)
    status_list = [c["status"] for c in encontradas]
    resumo = {
        "agendadas": status_list.count("agendada"),
        "concluidas": status_list.count("concluida"),
        "faltas": status_list.count("falta"),
        "canceladas": status_list.count("cancelada"),
        "total_consultas": len(encontradas)
    }
    return encontradas, resumo

def relatorio_financeiro_paciente(paciente_id):
    """Relatório 3: Detalha total gasto por um paciente em consultas e multas."""
    consultas_paciente = buscar_consultas_por_paciente(paciente_id)
    total_consultas = sum(c["valor_total"] for c in consultas_paciente if c["status"] == "concluida")
    total_multas = sum(MULTA_FALTA for c in consultas_paciente if c["status"] == "falta")
    return {
        "consultas": consultas_paciente,
        "total_consultas": total_consultas,
        "total_multas": total_multas,
        "total_geral": total_consultas + total_multas
    }

