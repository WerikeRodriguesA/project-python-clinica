import json 
import os 

def carregar(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
'''
na função de carregar o codigo tenta abrir o arquivo e carregar os dados usando json.load. Se o arquivo não existir,
(os.path.exists(arquivo))ou se houver um erro de decodificação JSON, por exemplo, se o arquivo estiver vazio ou corrompido, a função retorna uma lista vazia.
Isso garante que o programa possa continuar funcionando mesmo que o arquivo de dados esteja ausente ou inválido.
O operador with é usado para garantir que o arquivo seja fechado assim que terminar a leitura, evitando vazamentos de memória.
Enconding="utf-8" para quem vem de linguagnes como C e JAVA já sabem para que server.
Para validação usamos o isinstance(data, list) memso que alguém altere o banco manualemente e coloque um objeto diferente ,
o programa não quebra, irá apenas retornar uma lista vazia
E também a função except (json.JSONDecodeError, ValueError) para tratar de jsons mal formaados ou comrropidos 
'''
def salvar(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

'''
ensure_ascii=False para converter caracteres não ASCII, fazendo asssim com que o pyhton salve os textos
puramente, mantendo o json legível a olho humano.
indent=2 para formatar o json com uma indedentação de 2 espaços, para ajudar na leitura e evitar aquela linha gigante do python.

'''
