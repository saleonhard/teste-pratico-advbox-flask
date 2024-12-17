import re
import pandas as pd

# Função para formatar CPF ou CNPJ
def format_cpf_cnpj(value):
    """Formata CPF ou CNPJ, preenchendo zeros à esquerda se necessário."""
    value = re.sub(r'\D', '', str(value))  # Remove caracteres não numéricos
    if len(value) == 11 or len(value) == 14:  # Verifica se é CPF (11) ou CNPJ (14)
        return value.zfill(14 if len(value) == 14 else 11)  # Adiciona zeros à esquerda
    return None  # Retorna None se não for válido

def selecionar_cpf_cnpj(cpf, cnpj):
    """Seleciona CPF ou CNPJ válido. Move inválidos para 'ANOTAÇÕES GERAIS'."""
    cpf_formatado = format_cpf_cnpj(cpf)
    
    if cpf_formatado:  # Se CPF for válido, retorna ele
        return cpf_formatado, None
    else: 
        pass
    # Se o CPF for inválido, tenta verificar o CNPJ
    cnpj_formatado = format_cpf_cnpj(cnpj)
    
    if cnpj_formatado:  # Se CNPJ for válido, retorna o CNPJ
        return cnpj_formatado, None
    
    # Se ambos forem inválidos, retorna um erro
    return None, "CPF/CNPJ inválido"  # Só retorna erro se ambos forem inválidos

# Função para validar e formatar números de telefone
def format_phone(value):
    """Formata o telefone, mantendo 10 ou 11 dígitos, preenchendo zeros à esquerda se necessário."""
    value = re.sub(r'\D', '', str(value))  # Remove caracteres não numéricos
    if value:  # Verifica se há valor
        if len(value) < 10:
            value = value.zfill(10)  # Preenche com zeros à esquerda se faltar dígitos
        if len(value) in [10, 11]:  # Aceita telefones com 10 ou 11 dígitos
            return f"({value[:2]}) {value[2:7]}-{value[7:]}" if len(value) == 10 else f"({value[:2]}) {value[2:8]}-{value[8:]}"
    return ''  # Retorna vazio se não houver valor ou for inválido

# Função para validar e selecionar email
def validate_email(value):
    """Valida o email e retorna apenas o primeiro válido, ou None."""
    emails = str(value).split(';')
    for email in emails:
        email = email.strip()
        if re.match(r'^[^@]+@[^@]+\.[^@]+$', email):  # Regex para validação básica de email
            return email
    return None

# Função para formatar o CEP
def format_cep(value):
    """Formata o CEP para ter exatamente 8 dígitos, adicionando zeros no final se necessário e removendo caracteres especiais."""
    value = re.sub(r'\D', '', str(value))  # Remove qualquer caractere não numérico
    if len(value) == 0:
        return ''  # Retorna vazio se não houver dígitos
    return value.zfill(8)  # Preenche com zeros à direita até atingir 8 dígitos



################  PROCESSOS ###################

# Função para validar e formatar o número do processo
def formatar_numero_processo(numero):
    
    numero = re.sub(r'\D', '', str(numero))   # Remove caracteres não numéricos
    if len(numero) == 20:
        return f"{numero[:7]}-{numero[7:9]}.{numero[9:13]}.{numero[13:14]}.{numero[14:16]}.{numero[16:20]}"
    elif len(numero) < 20 and len(numero) > 0:  # Apenas se houver algo a preencher
        numero = numero.zfill(20)  # Preenche com zeros à esquerda até atingir 20 dígitos
        return f"{numero[:7]}-{numero[7:9]}.{numero[9:13]}.{numero[13:14]}.{numero[14:16]}.{numero[16:20]}"
    
    return None  # Retorna None se o número for inválido ou vazio



def find(chave_pk, tabela_busca, chave_busca, coluna_retorno):

    # Se chave_pk for uma lista ou série, iterar sobre ela
    if isinstance(chave_pk, (list, pd.Series)):
        resultados = []
        for chave in chave_pk:
            resultado = tabela_busca[tabela_busca[chave_busca] == chave]
            if not resultado.empty:
                resultados.extend(resultado[coluna_retorno].tolist())
        return resultados
    else:
        # Caso contrário, é um valor único (string, por exemplo)
        resultados = tabela_busca[tabela_busca[chave_busca] == chave_pk]
        if not resultados.empty:
            return resultados[coluna_retorno].tolist()
        else:
            return []