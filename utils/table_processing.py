from utils.validation import *
import pandas as pd

def processar_tabela_clientes(tabela):
# Campos de entrada esperados
    campos_entrada = [
        'razao_social', 'cpf', 'cnpj', 'rg', 'nacionalidade', 'nascimento', 'estado_civil',
        'profissao', 'telefone2', 'telefone1', 'email1', 'email2', 'uf', 'cidade', 'bairro', 'logradouro', 'cep', 'pis',
        'nome_mae', 'observacoes', 'tipocliente'  # Adicionando a coluna tipocliente
    ]

    # Selecionar somente os campos esperados
    df = tabela[campos_entrada]

    # Transformações
    df['NOME'] = df['razao_social'].str.strip()
    df[['CPF CNPJ', 'ANOTAÇÕES CPF/CNPJ']] = df.apply(
        lambda x: selecionar_cpf_cnpj(x['cpf'], x['cnpj']), axis=1, result_type='expand'
    )


    df['RG'] = df['rg'].str.strip()
    df['NACIONALIDADE'] = df['nacionalidade']
    df['DATA DE NASCIMENTO'] = pd.to_datetime(df['nascimento'], errors='coerce').dt.strftime('%d/%m/%Y')
    df['ESTADO CIVIL'] = df['estado_civil']
    df['PROFISSÃO'] = df['profissao']
    df['SEXO'] = ''
    
    # Atualizando celular e telefone
    df['CELULAR'] = df['telefone2'].apply(format_phone)  # Usando telefone diretamente
    df['TELEFONE'] = df['telefone1'].apply(format_phone)  # Usando telefone diretamente
    
    df['EMAIL'] = df['email1'].apply(validate_email)
    df['PAIS'] = 'BRASIL'
    df['ESTADO'] = df['uf'].str.upper()
    df['CIDADE'] = df['cidade'].str.strip()
    df['BAIRRO'] = df['bairro'].str.strip()
    df['ENDEREÇO'] = df['logradouro'].str.strip()
    df['CEP'] = df['cep'].apply(format_cep)
    df['PIS PASEP'] = df['pis'].fillna('').astype(str).str.strip()
    df['CTPS'] = ''
    df['CID'] = ''
    df['NOME DA MÃE'] = df['nome_mae'].str.strip()

    # Atualizando a origem do cliente com base na coluna tipocliente
    df['ORIGEM DO CLIENTE'] = df['tipocliente'].map({
        '1': 'MIGRAÇÃO',
        '2': 'PARTE CONTRÁRIA',
        '3': 'TERCEIRO'
    }).fillna('MIGRAÇÃO')  # Caso o valor de tipocliente não seja 1, 2 ou 3, será 'MIGRAÇÃO'

    # Inicializando a coluna ANOTAÇÕES GERAIS
    df['ANOTAÇÕES GERAIS'] = df['observacoes'].fillna('')

    # Adiciona o campo de anotações sobre CPF/CNPJ
    df['ANOTAÇÕES GERAIS'] = df.apply(
    lambda x: (
        f"{x['ANOTAÇÕES GERAIS']}; "
        f"{'CPF/CNPJ inválido: ' + (x['cpf'] if pd.notna(x['cpf']) and x['cpf'] != '' else x['cnpj']) if (pd.notna(x['cpf']) and x['cpf'] != '') or (pd.notna(x['cnpj']) and x['cnpj'] != '') else 'Sem CPF/CNPJ cadastrado'}"
    ).strip('; ')
    if pd.notna(x['ANOTAÇÕES CPF/CNPJ']) else x['ANOTAÇÕES GERAIS'],
    axis=1
    )

    # Se o email2 estiver presente e email1 também, adicionar email2 como anotação
    df['ANOTAÇÕES GERAIS'] = df.apply(
        lambda x: f"{x['ANOTAÇÕES GERAIS']}; email2: {x['email2']}" if pd.notna(x['email2']) and x['email2'].strip() != '' and pd.notna(x['email1']) else x['ANOTAÇÕES GERAIS'],
        axis=1
    )

    # Campos de saída
    campos_saida = [
        'NOME', 'CPF CNPJ','RG', 'NACIONALIDADE', 'DATA DE NASCIMENTO',
        'ESTADO CIVIL', 'PROFISSÃO', 'SEXO', 'CELULAR', 'TELEFONE', 'EMAIL',
        'PAIS', 'ESTADO', 'CIDADE', 'BAIRRO', 'ENDEREÇO', 'CEP',
        'PIS PASEP', 'CTPS', 'CID', 'NOME DA MÃE', 'ORIGEM DO CLIENTE',
        'ANOTAÇÕES GERAIS'
    ]

    return df[campos_saida]


def processar_tabela_processos(tabelas):
    

    tabela_processos = tabelas["processos"]
    tabela_litis_cliente = tabelas["litis_cliente"]
    tabela_litis_adverso = tabelas["litis_adverso"]
    tabela_assunto = tabelas["assunto"]
    tabela_fase = tabelas["fase"]
    tabela_tribunal = tabelas["tribunal"]
    tabela_comarca = tabelas["comarca"]
    tabela_pasta = tabelas["pastas"]
    tabela_usuario = tabelas["usuario"]
    tabela_area_atuacao = tabelas["area_atuacao"]
    tabela_local_tramite = tabelas["local_tramite"]
    tabela_clientes = tabelas["clientes"]

    # Campos de entrada esperados (ajuste conforme o CSV de entrada)
    campos_entrada = [
     'numero_processo', 'pasta',  'data_distribuicao', 'codarea_acao', 
     'cod_cliente', 'cod_usuario', 
     'valor_causa', 'observacoes',  'inclusao', 'ativo', 'codigo', 'objeto_acao', 
     'destino',  'data_entrada', 'cod_processo_apensar', 'exibir_apenso_raiz', 
     'tipoprocesso', 'codassunto', 'codobjetoadm', 'codlocaltramite',  'codcomarca', 
     'prognostico', 'statusprocessual', 'grupo_processo', 'codigo_fase', 'data_contratacao', 'pedido', 'codparceiros', 'data_transitojulgado', 
     'data_sentenca', 'data_execucao', 'contingencia', 'valor_causa2', 'migracao', 'acao_ajuizada', 'cod_fase_processo', 
     'campo_livre1', 'numero_pasta', 'numero_cnj', 'migra_parceiro', 'numero_vara'

    ]
    

    # Selecionar somente os campos esperados
    df = tabela_processos[campos_entrada]
   

    # Processamento e transformação
    df['NOME DO CLIENTE'] =  [
    (resultados[0] if resultados else None)
    for codigo in df['codigo']
    for resultados in [find(find(codigo, tabela_litis_cliente, 'cod_processo', 'cod_parte'), tabela_clientes,'codigo','razao_social')]
    ]
 
    df['PARTE CONTRÁRIA'] =  [
    (resultados[0] if resultados else None)
    for codigo in df['codigo']
    for resultados in [find(find(codigo, tabela_litis_adverso, 'cod_processo', 'cod_parte'), tabela_clientes,'codigo','razao_social')]
    ]
   
    df['TIPO DE AÇÃO'] = [
    (resultados[0] if resultados else None)
    for codigo in df['codassunto']
    for resultados in [find(codigo, tabela_assunto, 'codigo', 'descricao')]
    ]
    df['GRUPO DE AÇÃO'] = [
    (resultados[0] if resultados else None)
    for codigo in df['codarea_acao']
    for resultados in [find(codigo, tabela_area_atuacao, 'codigo', 'descricao')]
    ]
    
    df['FASE PROCESSUAL'] = [
    (resultados[0] if resultados else None)
    for codigo in df['codigo_fase']
    for resultados in [find(codigo, tabela_fase, 'codigo', 'fase')]
    ]

    df['ETAPA'] = df['FASE PROCESSUAL'].apply(lambda x: 'Conhecimento' if pd.isna(x) or x == '' else x) 


    # Aplicar a formatação e mover números inválidos para o campo PROTOCOLO
    df['NÚMERO DO PROCESSO'] = df['numero_processo'].apply(lambda x: formatar_numero_processo(x) if formatar_numero_processo(x) else '')
    df['PROTOCOLO'] = df.apply(lambda x: x['numero_processo'] if x['NÚMERO DO PROCESSO'] == '' else '', axis=1)


    df['PROCESSO ORIGINÁRIO'] = df['cod_processo_apensar'] 

    df['TRIBUNAL'] = ''

    df['VARA'] =  [
    (resultados[0] if resultados else None)
    for codigo in df['codlocaltramite']
    for resultados in [find(codigo, tabela_local_tramite, 'codigo', 'descricao')]
    ]
    df['COMARCA'] = [
    (resultados[0] if resultados else None)
    for codigo in df['codcomarca']
    for resultados in [find(codigo, tabela_comarca, 'codigo', 'descricao')]
    ]


    # # Formatação de valores monetários
    df['EXPECTATIVA/VALOR DA CAUSA'] = df['valor_causa'].apply(
        lambda x: f"{float(x):.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if pd.notna(x) else ''
    )
    df['VALOR HONORÁRIOS'] = ''
   
    df['PASTA'] = df['numero_pasta']

     # # Campos de datas
    df['DATA CADASTRO'] = pd.to_datetime(df['data_contratacao'], errors='coerce').dt.strftime('%d/%m/%Y')
    df['DATA FECHAMENTO'] = pd.to_datetime(df['data_sentenca'], errors='coerce').dt.strftime('%d/%m/%Y')
    df['DATA TRANSITO'] = pd.to_datetime(df['data_transitojulgado'], errors='coerce').dt.strftime('%d/%m/%Y')
    df['DATA ARQUIVAMENTO'] = ''
    df['DATA REQUERIMENTO'] = ''

    # # Campo de responsável
    df['RESPONSÁVEL'] =  [
    (resultados[0] if resultados else None)
    for codigo in df['cod_usuario']
    for resultados in [find(codigo, tabela_usuario, 'id', 'nome')]
    ]
    # # Anotações gerais
    df['ANOTAÇÕES GERAIS'] = df['observacoes'].fillna('').str.strip()

    # Campos de saída
    campos_saida = [

         'NOME DO CLIENTE',
         'PARTE CONTRÁRIA',
         'TIPO DE AÇÃO' ,  'GRUPO DE AÇÃO', 'FASE PROCESSUAL', 'ETAPA',
         'NÚMERO DO PROCESSO', 'PROCESSO ORIGINÁRIO', 'TRIBUNAL', 'VARA', 'COMARCA', 'PROTOCOLO',
         'EXPECTATIVA/VALOR DA CAUSA', 'VALOR HONORÁRIOS', 'PASTA', 'DATA CADASTRO', 'DATA FECHAMENTO',
         'DATA TRANSITO', 'DATA ARQUIVAMENTO', 'DATA REQUERIMENTO', 'RESPONSÁVEL', 'ANOTAÇÕES GERAIS'
    ]

    return df[campos_saida]