from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
import pandas as pd
import tempfile
from utils.table_processing import processar_tabela_clientes, processar_tabela_processos

app = Flask(__name__)
app.secret_key = "123456789"

# Variáveis globais
tabelas_necessarias = {"clientes", "processos"}
tabelas_encontradas = set()
temp_dir = tempfile.mkdtemp()  # Diretório temporário para armazenar os arquivos


# Rota principal (carregar tabelas)
@app.route("/", methods=["GET", "POST"])
def index():
    global tabelas_encontradas

    # Limpar dados na sessão em caso de nova sessão
    if session.new or "tabelas" not in session:
        tabelas_encontradas.clear()
        session.clear()
        session.modified = True

    if request.method == "POST":
        arquivos = request.files.getlist("arquivos")
        if not arquivos:
            flash("Nenhum arquivo foi selecionado. Por favor, selecione uma pasta.", "danger")
            return redirect(url_for("index"))

        try:
            tabelas_encontradas.clear()
            session["tabelas"] = {}

            for arquivo in arquivos:
                if arquivo.filename.endswith(".csv"):
                    # Salva o arquivo no diretório temporário corretamente
                    nome_arquivo = os.path.basename(arquivo.filename)  # Nome puro do arquivo
                    temp_path = os.path.join(temp_dir, nome_arquivo)
                    
                    arquivo.save(temp_path)  # Salva o arquivo no diretório temporário

                    # Ler o arquivo usando open() com errors="replace"
                    with open(temp_path, mode="r", encoding="utf-8", errors="replace") as f:
                        tabela = pd.read_csv(f, delimiter=";") 
                        # tabela = csv.reader(f, delimiter=';')
                    # Nome da tabela
                    nome_tabela = nome_arquivo.replace("v_", "").replace("_CodEmpresa_92577.csv", "")

                    # Salvar DataFrame como pickle
                    pickle_path = os.path.join(temp_dir, f"{nome_tabela}.pkl")
                    tabela.to_pickle(pickle_path)

                    session["tabelas"][nome_tabela] = pickle_path
                    if nome_tabela in tabelas_necessarias:
                        tabelas_encontradas.add(nome_tabela)


            # Verificar tabelas faltantes
            faltando = tabelas_necessarias - tabelas_encontradas
            if faltando:
                flash(f"As seguintes tabelas estão faltando: {', '.join(faltando)}", "warning")
            else:
                flash("Tabelas carregadas com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao carregar tabelas: {str(e)}", "danger")

        return redirect(url_for("index"))

    return render_template("index.html", tabelas_encontradas=tabelas_encontradas)


@app.route("/apagar_dados", methods=["POST"])
def apagar_dados():
    # Verificar se as tabelas foram carregadas
    if "tabelas" not in session or not session["tabelas"]:
        flash("Nenhuma tabela foi carregada. Não há dados para apagar.", "warning")
        return redirect(url_for("index"))

    try:
        # Apagar os dados das tabelas na sessão
        session.pop("tabelas", None)  # Remove as tabelas da sessão
        session.modified = True  # Marca a sessão como modificada
        tabelas_encontradas.clear()
        flash("Dados apagados com sucesso.", "success")
    except Exception as e:
        flash(f"Erro ao apagar dados: {str(e)}", "danger")

    return redirect(url_for("index"))


# Rota para exportar e fazer download de uma tabela
@app.route("/download/<string:nome_tabela>", methods=["GET"])
def download(nome_tabela):
    if "tabelas" not in session or nome_tabela not in session["tabelas"]:
        flash("Tabela não encontrada para exportação.", "danger")
        return redirect(url_for("index"))

    try:

        # Processar tabelas específicas
        if nome_tabela == "clientes":

            # Carregar tabela do arquivo temporário
            tabela_path = session["tabelas"][nome_tabela]
            tabela = pd.read_pickle(tabela_path)
            tabela_processada = processar_tabela_clientes(tabela)
        else:
            # Carregar todas tabelas do arquivo temporário
            todas_tabelas = {}
            # Carregamos cada tabela
            for n_tabela, tabela_path in session["tabelas"].items():
                tabela = pd.read_pickle(tabela_path)  # Carrega o DataFrame
                todas_tabelas[n_tabela] = tabela  # Usa o nome da tabela como chave no dicionário

            tabela_processada = processar_tabela_processos(todas_tabelas)

        # Salvar tabela processada em um arquivo temporário para download
        output_path = os.path.join(temp_dir, f"{nome_tabela.upper()}.xlsx")
        tabela_processada.to_excel(output_path, index=False)

        # Retornar arquivo para download
        return send_file(output_path, as_attachment=True, download_name=f"{nome_tabela.upper()}.xlsx")
    except Exception as e:
        flash(f"Erro ao exportar tabela: {str(e)}", "danger")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
