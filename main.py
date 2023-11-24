import cx_Oracle
import time
import sys
import random
import re
import json
from datetime import datetime


def timer(tempo):
    if tempo == 5:
        print(f'Em {tempo} segundos o programa será fechado!')
        for i in range(0, tempo):
            sys.stdout.write("\r{}".format(i + 1))
            sys.stdout.flush()
            time.sleep(1)
        print('')

    elif tempo == 3:
        print(f'Em {tempo} segundos você voltará para fazer login!')
        print('-' * 100)
        for i in range(0, tempo):
            sys.stdout.write("\r{}".format(i + 1))
            sys.stdout.flush()
            time.sleep(1)
        print('')

    else:
        print(f'Em {tempo} segundos voltaremos para o menu incial...')
        for i in range(0, tempo):
            sys.stdout.write("\r{}".format(i + 1))
            sys.stdout.flush()
            time.sleep(1)
        print('')


def cpf_entrada():
    def validador_cpf(cpf):
        corpo_cpf = cpf[:9]
        digito_cpf = cpf[-2:]

        calculo_1 = 0
        calculo_2 = 0

        multiplicacao = [10, 9, 8, 7, 6, 5, 4, 3, 2]

        for i, j in zip(multiplicacao, corpo_cpf):
            calculo_1 += i * int(j)

        resto_1 = calculo_1 % 11

        digito_1 = 0 if resto_1 < 2 else 11 - resto_1

        corpo_cpf += str(digito_1)

        for i, j in zip(multiplicacao, corpo_cpf[1:]):
            calculo_2 += i * int(j)

        resto_2 = calculo_2 % 11

        digito_2 = 0 if resto_2 < 2 else 11 - resto_2

        return digito_cpf == f'{digito_1}{digito_2}'
    
    blocklist = [
        '00000000000',
        '11111111111',
        '22222222222',
        '33333333333',
        '44444444444',
        '55555555555',
        '66666666666',
        '77777777777',
        '88888888888',
        '99999999999'
    ]

    while True:
        print('-' * 100)
        cpf_inserido = input('Por favor digite seu CPF ou insira "X" para sair:')
        print('-' * 100)
        cpf_sem_barra = cpf_inserido.replace('-', '')
        cpf_formatado = cpf_sem_barra.replace('.', '')

        if cpf_formatado.isnumeric():
            if len(cpf_formatado) == 11:
                if cpf_formatado in blocklist:
                    print('O CPF não pode conter todos números iguais!\n')
                else:
                    if not validador_cpf(cpf_formatado):
                        print('Seu CPF está invalido\n')
                    else:
                        return cpf_formatado

            else:
                print('O CPF deve conter 11 dígitos!\n')

        elif cpf_formatado.lower() == 'x':
            return cpf_formatado

        else:
            print('Digite seu CPF corretamente ou apenas "x" para sair!\n')


def conexao_oracle():
    usuario = 'rm550269'
    senha = '291103'
    host = 'oracle.fiap.com.br'
    sid = 'ORCL'
    porta = '1521'
    
    try:
        credenciais = cx_Oracle.makedsn(host, porta, sid)
        conexao = cx_Oracle.connect(usuario, senha, credenciais)
        return conexao
    
    except cx_Oracle.Error as e:
        print(f"Erro ao conectar ao banco de dados Oracle: {e}")
    

def validar_email(email):
    padrao_email = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if padrao_email.match(email):
        return True
    else:
        return False


def validar_login(id): 
    try:
        conexao = conexao_oracle()
        cursor = conexao.cursor()
        cursor.execute(f'select id_paciente from tb_mtc_paciente where id_paciente = {id}')
        id_validar = cursor.fetchall()
        conexao.close()
        if len(id_validar) == 0:
            return ''
        else:
            return id_validar[0][0]
        
    except cx_Oracle.Error as e:
        print(f'Erro ao selecionar dados: {e}')


def login(conexao_oracle, cpf):
    print('-' * 100)
    print('Bem vindo a MediTracker!')
    print('-' * 100)

    documento_paciente = cpf
    
    if documento_paciente.lower() == 'x':
        return False
        
    else:
        id_paciente = documento_paciente[:3]
        id_validado = validar_login(id_paciente)

        if str(id_validado) == id_paciente:
            return True
        
        else:
            cadastro(conexao_oracle, documento_paciente)


def gerar_id_aleatoria():
    return random.randint(1, 1000000)


def cadastro(conexao_oracle, documento):
    print('-' * 100)
    print('Percebemos que seu CPF não possui cadastro no nosso sistema!\n'
          'Iremos te cadastrar neste exato momento! ')
    print('-' * 100)

    nome_paciente = dados_cadastro('nome paciente')
    email = dados_cadastro('email')
    dia_nascimento = dados_cadastro('dia nascimento')
    mes_nascimento = dados_cadastro('mes nascimento')
    ano_nascimento = dados_cadastro('ano nascimento')
    data_nascimento_paciente = f'{dia_nascimento}/{mes_nascimento}/{ano_nascimento}'
    nome_doenca = dados_cadastro('nome doenca')
    cid_doenca = dados_cadastro('cid doenca')
    medicamento = dados_cadastro('medicamento')
    dosagem = dados_cadastro('dosagem')
    str_dosagem = 'mg - ml'
    ano_tratamento = dados_cadastro('ano tratamento')
    mes_tratamento = dados_cadastro('mes tratamento')
    dia_tratamento = dados_cadastro('dia tratamento')
    data_tratamento = f'{ano_tratamento}/{mes_tratamento}/{dia_tratamento}'

    id_doenca = gerar_id_aleatoria()
    id_medicamento = gerar_id_aleatoria()
    id_tipo_dosagem = gerar_id_aleatoria()
    id_med_dosagem = gerar_id_aleatoria()
    id_trat_med_paciente = documento[3 :6]
    id_paciente = documento[:3]
    
    
    sql_tb_paciente = 'insert into TB_MTC_PACIENTE (ID_PACIENTE, NOME_PACIENTE, DATA_NASCIMENTO_PACIENTE, DOCUMENTO_PACIENTE, EMAIL_PACIENTE) values (:1, :2, :3, :4, :5)'
    sql_tb_doenca = 'insert into TB_MTC_DOENCA (ID_DOENCA, NOME_DOENCA, CID_DOENCA) values (:1, :2, :3)'
    sql_tb_medicamento = 'insert into TB_MTC_MEDICAMENTO (ID_MEDICAMENTO, NOME_MEDICAMENTO, DOSAGEM_MEDICAMENTO) values (:1, :2, :3)'
    sql_tb_forma_dosagem = 'insert into TB_MTC_FORMA_DOSAGEM (ID_TIPO_DOSAGEM, DESCRICAO_TIPO_DOSAGEM) values (:1, :2)'
    sql_tb_med_dosagem = 'insert into TB_MTC_MED_DOSAGEM (ID_MEDICAMENTO, ID_TIPO_DOSAGEM, ID_MED_DOSAGEM) values (:1, :2, :3)'
    sql_tb_trat_med_paciente = 'insert into TB_MTC_TRAT_MED_PACIENTE (ID_TRAT_MED_PACIENTE, DATA_INICIO_TRATAMENTO, ID_DOENCA, ID_PACIENTE, ID_MED_DOSAGEM) values (:1, :2, :3, :4, :5)'

    
    insert(conexao_oracle, sql_tb_paciente, id_paciente, nome_paciente, data_nascimento_paciente, documento, email)
    insert(conexao_oracle, sql_tb_doenca, id_doenca, nome_doenca, cid_doenca)
    insert(conexao_oracle, sql_tb_medicamento, id_medicamento, medicamento, dosagem)
    insert(conexao_oracle, sql_tb_forma_dosagem, id_tipo_dosagem, str_dosagem)
    insert(conexao_oracle, sql_tb_med_dosagem, id_medicamento, id_tipo_dosagem, id_med_dosagem)
    insert(conexao_oracle, sql_tb_trat_med_paciente, id_trat_med_paciente, data_tratamento, id_doenca, id_paciente, id_med_dosagem)


def dados_cadastro(item):
    if item == 'nome paciente':
        while True:
            nome = input('Digite o seu primeiro nome:')
            if nome.isnumeric():
                print('Não utilize numeros na hora de cadastrar o nome!')
            else:
                return nome

    elif item == 'dia nascimento':
        while True:
            dia_nascimento = input('Digite seu dia de nascimento (1-31): ')
            if dia_nascimento.isnumeric() and 0 < int(dia_nascimento) < 32:
                return dia_nascimento
            else:
                print('Utilize numeros na hora de cadastrar o dia do seu nascimento!')

    elif item == 'mes nascimento':
        while True:
            mes_nascimento = input('Digite seu mes de nascimento (1-12): ')
            if mes_nascimento.isnumeric() and 0 < int(mes_nascimento) < 13:
                return mes_nascimento
            else:
                print('Utilize numeros na hora de cadastrar o mes do seu nascimento!')

    elif item == 'ano nascimento':
        while True:
            ano_nascimento = input('Digite seu ano de nascimento (ex:1990): ')
            if ano_nascimento.isnumeric() and 0 < int(ano_nascimento) < 2024:
                return ano_nascimento
            else:
                print('Utilize numeros na hora de cadastrar o ano do seu nascimento!')
    
    if item == 'nome doenca':
        while True:
            nome_doenca = input('Digite o nome da sua enfermidade para acompanhamento:')
            if nome_doenca.isnumeric():
                print('Não utilize numeros na hora de cadastrar a enfermidade!')
            else:
                return nome_doenca
            
    elif item == 'cid doenca':
        while True:
            cid_doenca = input('Digite o CID da sua enfermidade (ex:A99): ')
            if any(char.isnumeric() for char in cid_doenca):
                return cid_doenca
            else:
                print('Seu CID deve conter pelo um numero!')

    if item == 'medicamento':
        while True:
            medicamento = input('Digite o nome do seu medicamento:')
            if medicamento.isnumeric():
                print('Não utilize numeros na hora de cadastrar o nome do medicamento!')
            else:
                return medicamento
            
    elif item == 'dosagem':
        while True:
            dosagem = input('Digite a dosagem do seu medicamento em miligramas ou mililitros(mg - ml): ')
            if dosagem.isnumeric():
                return dosagem
            else:
                print('Utilize numeros na hora de cadastrar a dosagem do medicamento!')

    elif item == 'dia tratamento':
        while True:
            dia_nascimento = input('Digite o dia do inicio do seu tratamento com o medicamento(1-31): ')
            if dia_nascimento.isnumeric() and 0 < int(dia_nascimento) < 32:
                return dia_nascimento
            else:
                print('Utilize numeros na hora de cadastrar o dia! Ou um dia valido!')

    elif item == 'mes tratamento':
        while True:
            mes_nascimento = input('Digite o mes do inicio do seu tratamento com o medicamento(1-12): ')
            if mes_nascimento.isnumeric() and 0 < int(mes_nascimento) < 13:
                return mes_nascimento
            else:
                print('Utilize numeros na hora de cadastrar o mes! Ou um mes valido!')

    elif item == 'ano tratamento':
        while True:
            ano_nascimento = input('Digite o ano de inicio do seu tratamento com o medicamento(ex:1990): ')
            if ano_nascimento.isnumeric() and 0 < int(ano_nascimento) < 2024:
                return ano_nascimento
            else:
                print('Utilize numeros na hora de cadastrar o ano! Ou um ano valido!')
    
    if item == 'descricao diaria':
        while True:
            descricao_diaria = input('Digite em poucas palavras como os sintomas afetaram sua rotina diária: ')
            if descricao_diaria.isnumeric():
                print('Não utilize apenas numeros na hora de cadastrar!')
            elif len(descricao_diaria) > 3000:
                print('Sua texto ficou muito grande! Por favor deixe ele com no maximo 3000 caracteres!')
            else:
                return descricao_diaria
            
    elif item == 'humor':
        while True:
            humor = input('Digite um numero de 1 - 10(um a dez) que represente seu humor hoje, sendo 1 péssimo e 10 incrivel: ')
            if humor.isnumeric() and 0 < int(humor) < 11:
                return humor
            else:
                print('Utilize numeros na hora de cadastrar humor! Ou um numero de 1 - 10(um a dez)!')

    if item == 'sintoma':
        while True:
            sintoma = input('Digite os sintomas que sentiu hoje: ')
            if sintoma.isnumeric():
                print('Não utilize apenas numeros na hora de cadastrar seus sintomas!')
            elif len(sintoma) > 300:
                print('Sua texto ficou muito grande, por favor deixe ele com no maximo 300 caracteres!')
            else:
                return sintoma

    elif item == 'intensidade sintoma':
        while True:
            intensidade_sintoma = input('Digite um numero de 1 - 10(um a dez) que represente a intensidade dos seus sintomas, sendo 1 leve e 10 insuportavel: ')
            if intensidade_sintoma.isnumeric() and 0 < int(intensidade_sintoma) < 11:
                return intensidade_sintoma
            else:
                print('Utilize numeros na hora de cadastrar a intensidade! Ou um numero de 1 - 10(um a dez)!')

    elif item == 'duracao sintoma':
        while True:
            duracao_sintoma = input('Digite o tempo de duração dos seus sintomas em horas: ')
            if duracao_sintoma.isnumeric():
                return str(duracao_sintoma)
            else:
                print('Utilize numeros na hora de cadastrar o tempo de duração!')

    elif item == 'sta medicamento tomado':
        while True:
            sta_medicamento_tomado = input('[0] Não\n[1] Sim\nTomou seus medicamentos hoje?: ')
            if sta_medicamento_tomado.isnumeric() and int(sta_medicamento_tomado) < 2:
                return sta_medicamento_tomado
            else:
                print('Utilize numeros! Ou digite somente 0 ou 1')

    elif item == 'email':
        while True:
            email_entrada = input('Digite seu email: ')
            if not validar_email(email_entrada):
                print('Email digitado incorretamente! Lembre-se de utilizar "@" e "."')
            elif len(email_entrada) > 300:
                print('Seu email é muito grande! Por favor digite um com no maximo 300 caracteres!')
            else:
                return email_entrada


def dados_diario(conexao_oracle, documento):
    data = datetime.now()
    data_registro = data.strftime(r"%Y/%m/%d")
    print('-' * 100)
    print('Olá, vamos fazer algumas perguntas para adicionarmos suas informações diárias!')
    print('-' * 100)

    descricao_diaria = dados_cadastro('descricao diaria')
    humor = dados_cadastro('humor')
    nome_sintoma = dados_cadastro('sintoma')
    intensidade_sintoma = dados_cadastro('intensidade sintoma')
    duracao_sintoma = dados_cadastro('duracao sintoma')
    medicamento_tomado = dados_cadastro('sta medicamento tomado')

    id_registro_diario = gerar_id_aleatoria()
    id_sintoma = gerar_id_aleatoria()
    id_sintoma_diario = gerar_id_aleatoria()
    id_registro_diario_med = gerar_id_aleatoria()
    id_paciente = documento[:3]
    id_trat_med_paciente = documento[3 :6]


    sql_tb_registro_diario = 'insert into TB_MTC_REGISTRO_DIARIO (ID_REGISTRO_DIARIO, DESCRICAO_REGISTRO, ID_PACIENTE, HUMOR, DATA_REGISTRO) values (:1, :2, :3, :4, :5)'
    sql_tb_sintoma_diario = 'insert into TB_MTC_SINTOMA_DIARIO (ID_SINTOMA_DIARIO, INTENSIDADE_SINTOMA, DURACAO_SINTOMA, ID_REGISTRO_DIARIO, ID_SINTOMA, NOME_SINTOMA) values (:1, :2, :3, :4, :5, :6)'
    sql_tb_reg_diario_medicamento = 'insert into TB_MTC_REG_DIARIO_MEDICAMENTO (ID_REGISTRO_DIARIO_MED, DATA_REGISTRO_DIARIO_MED, ID_TRAT_MED_PACIENTE, STA_MEDICAMENTO_TOMADO) values (:1, :2, :3, :4)'


    insert(conexao_oracle, sql_tb_registro_diario, id_registro_diario, descricao_diaria, id_paciente, humor, data_registro)
    insert(conexao_oracle, sql_tb_sintoma_diario, id_sintoma_diario, intensidade_sintoma, duracao_sintoma, id_registro_diario, id_sintoma, nome_sintoma)
    insert(conexao_oracle, sql_tb_reg_diario_medicamento, id_registro_diario_med, data_registro, id_trat_med_paciente, medicamento_tomado)


def escolha_usuario():
    while True:
        print('-' * 100)
        escolha = input('[1] Nome\n[2] Data de nascimento\n[3] Email\nPor favor escolha um dado que deseje alterar: ')
        print('-' * 100)
        if escolha.isnumeric():
            if 4 > int(escolha) > 0:
                return escolha
                
            else:
                print('Escolha somente as opções listadas')
                print('-' * 100)

        else:
            print('Por favor utilize números na escolha')
            print('-' * 100)


def alterar_dados_pessoais(conexao_oracle, documento, escolha):     
    id_paciente = documento[:3]

    if escolha == '1':
        novo_nome = dados_cadastro('nome paciente')

        update(conexao_oracle, 'NOME_PACIENTE', novo_nome, id_paciente)

    elif escolha == '2':
        dia_nascimento = dados_cadastro('dia nascimento')
        mes_nascimento = dados_cadastro('mes nascimento')
        ano_nascimento = dados_cadastro('ano nascimento')
        nova_data_nascimento_paciente = f'{dia_nascimento}/{mes_nascimento}/{ano_nascimento}'

        update(conexao_oracle, 'DATA_NASCIMENTO_PACIENTE', nova_data_nascimento_paciente, id_paciente)

    elif escolha == '3':
        novo_email = dados_cadastro('email')

        update(conexao_oracle, 'EMAIL_PACIENTE', novo_email, id_paciente)


def excluir_dados_pessoais(conexao_oracle, documento):
    print('-' * 100)
    print('Olá, vamos fazer uma confirmação de documento antes de excluir!')
    print('-' * 100)
    id_paciente = documento[:3]
    while True:
        cpf_confirmacao = cpf_entrada()
        if cpf_confirmacao == documento:
            update(conexao_oracle, 'NOME_PACIENTE', 'NULL', id_paciente)
            update(conexao_oracle, 'DATA_NASCIMENTO_PACIENTE', 'NULL', id_paciente)
            update(conexao_oracle, 'EMAIL_PACIENTE', 'NULL', id_paciente)
            print('-' * 100)
            print('-' * 100)
            print('Seus dados pessoais foram excluidos!')
            print('-' * 100)
            print('-' * 100)
            break

        elif cpf_confirmacao.lower() == 'x':
            print('Você escolheu sair!')
            break
        else:
            print('Documento incorreto')
            break


def insert(conexao_oracle, sql, *args):
    try:
        conexao = conexao_oracle
        cursor = conexao.cursor()
        cursor.execute(sql, (args))
        conexao.commit()
        print("Dados inseridos com sucesso.")


    except cx_Oracle.Error as e:
        print(f"Erro ao inserir dados: {e}")

    finally:
        cursor.close()


def update(conexao_oracle, nome_coluna, novo_valor, id):
    try:
        conexao = conexao_oracle
        cursor = conexao.cursor()
        cursor.execute(f"UPDATE TB_MTC_PACIENTE SET {nome_coluna} = :novo_valor WHERE ID_PACIENTE = :id", 
                       novo_valor=novo_valor, id=id)
        conexao.commit()
        print("Dados atualizados com sucesso.")


    except cx_Oracle.Error as e:
        print(f"Erro ao atualizar dados: {e}")

    finally:
        cursor.close()


def remedios_tomados(conexao_oracle):
    sql = '''select doen.nome_doenca
          ,      medi.nome_medicamento
          ,      trmp.data_inicio_tratamento
          ,      redm.data_registro_diario_med data_registro
          ,      'Medicamento tomado? '|| case when redm.sta_medicamento_tomado = 0 then 'NÃO'
                                               when redm.sta_medicamento_tomado = 1 then 'SIM'
                                               else null end medicamento_tomado
          ,     redm.id_registro_diario_med 
          ,     paci.id_paciente
          from tb_mtc_trat_med_paciente trmp
          ,    tb_mtc_reg_diario_medicamento redm
          ,    tb_mtc_paciente paci
          ,    tb_mtc_doenca doen
          ,    tb_mtc_med_dosagem medo
          ,    tb_mtc_medicamento medi
          where trmp.id_paciente          = paci.id_paciente
          and   trmp.id_trat_med_paciente = redm.id_trat_med_paciente
          and   doen.id_doenca            = trmp.id_doenca
          and   medo.id_medicamento       = medi.id_medicamento
          and   medo.id_med_dosagem       = trmp.id_med_dosagem
          order by trmp.id_trat_med_paciente'''
    

    try:
        conexao = conexao_oracle
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for linha in resultado:
            print(linha)

        while True:
            print('-' * 100)
            escolha = input('[0] Não\n[1] Sim\nDeseja salvar essa consulta em um arquivo?')
            if escolha.isnumeric():
                if 2 > int(escolha):
                    if escolha == '0':
                        print('Otimo, voltaremos ao menu inicial!')
                        break
                    elif escolha == '1':
                        dados_json = []
                        colunas = [desc[0] for desc in cursor.description]
                        for linha in resultado:
                            dados_json.append(dict(zip(colunas, linha)))

                            with open('remedios_tomados', 'w') as arquivo_json:
                                json.dump(dados_json, arquivo_json, indent=2)
                        break
                    else:
                        ('Erro!')
                    
                else:
                    print('Escolha somente as opções listadas')
                    print('-' * 100)

            else:
                print('Por favor utilize números na escolha')
                print('-' * 100)
                print('-' * 100)


    except cx_Oracle.Error as e:
        print(f"Erro ao executar a consulta: {e}")

    finally:
        cursor.close()


def registros_diarios(conexao_oracle):
    sql = '''select distinct paci.id_paciente
            ,      redi.data_registro 
            ,      redi.id_registro_diario
            ,      descricao_registro
            ,      case when sidi.id_registro_diario is not null then 
                        listagg(sidi.nome_sintoma||' - intensidade : '||sidi.intensidade_sintoma,' ; ')  over (partition by redi.id_registro_diario)
                        else null end sintomas
            from tb_mtc_paciente paci
            ,    tb_mtc_registro_diario redi
            ,    tb_mtc_sintoma_diario sidi
            where paci.id_paciente        = redi.id_paciente
            and   redi.id_registro_diario = sidi.id_registro_diario(+)
            group by paci.id_paciente
            ,        redi.data_registro 
            ,        redi.id_registro_diario
            ,        descricao_registro
            ,        sidi.nome_sintoma
            ,        sidi.intensidade_sintoma
            ,        sidi.id_registro_diario
            order by paci.id_paciente
            ,        redi.data_registro'''
    

    try:
        conexao = conexao_oracle
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for linha in resultado:
            print(linha)

        while True:
            print('-' * 100)
            escolha = input('[0] Não\n[1] Sim\nDeseja salvar essa consulta em um arquivo?')
            if escolha.isnumeric():
                if 2 > int(escolha):
                    if escolha == '0':
                        print('Otimo, voltaremos ao menu inicial!')
                        break
                    elif escolha == '1':
                        dados_json = []
                        colunas = [desc[0] for desc in cursor.description]
                        for linha in resultado:
                            dados_json.append(dict(zip(colunas, linha)))

                            with open('registros_diarios', 'w') as arquivo_json:
                                json.dump(dados_json, arquivo_json, indent=2)
                        break
                    else:
                        ('Erro!')
                    
                else:
                    print('Escolha somente as opções listadas')
                    print('-' * 100)

            else:
                print('Por favor utilize números na escolha')
                print('-' * 100)
                print('-' * 100)


    except cx_Oracle.Error as e:
        print(f"Erro ao executar a consulta: {e}")

    finally:
        cursor.close()


def medicamentos_nao_tomados(conexao_oracle):
    sql = '''select count(1)
            , nome_medicamento
            , nome_paciente
            from tb_mtc_paciente paci
            ,    tb_mtc_trat_med_paciente trme
            ,    tb_mtc_reg_diario_medicamento dime
            ,    tb_mtc_med_dosagem medo
            ,    tb_mtc_medicamento medi
            where paci.id_paciente = trme.id_paciente
            and   dime.id_trat_med_paciente = trme.id_trat_med_paciente
            and   trme.id_med_dosagem = medo.id_med_dosagem
            and   medo.id_medicamento = medi.id_medicamento
            and   dime.sta_medicamento_tomado = '0'
            group by  nome_medicamento
            ,         nome_paciente
            having count(1) > 1'''
    

    try:
        conexao = conexao_oracle
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for linha in resultado:
            print(linha)

        while True:
            print('-' * 100)
            escolha = input('[0] Não\n[1] Sim\nDeseja salvar essa consulta em um arquivo?')
            if escolha.isnumeric():
                if 2 > int(escolha):
                    if escolha == '0':
                        print('Otimo, voltaremos ao menu inicial!')
                        break
                    elif escolha == '1':
                        dados_json = []
                        colunas = [desc[0] for desc in cursor.description]
                        for linha in resultado:
                            dados_json.append(dict(zip(colunas, linha)))

                            with open('medicamentos_nao_tomados', 'w') as arquivo_json:
                                json.dump(dados_json, arquivo_json, indent=2)
                        break
                    else:
                        ('Erro!')
                    
                else:
                    print('Escolha somente as opções listadas')
                    print('-' * 100)

            else:
                print('Por favor utilize números na escolha')
                print('-' * 100)
                print('-' * 100)


    except cx_Oracle.Error as e:
        print(f"Erro ao executar a consulta: {e}")

    finally:
        cursor.close()


def menu_inicial():
    print('-' * 100)
    print((' ' * 30) + 'MENU INICIAL')
    print('-' * 100)
    print('[0] Sair\n'
          '[1] Adicionar informações diárias (sintomas, medicamentos tomados e etc)\n'
          '[2] Alterar dados pessoais\n'
          '[3] Excluir dados pessoais\n'
          '[4] Remédios tomados\n'
          '[5] Registros diários\n'
          '[6] Pacientes, seus medicamentos e quantidade de dias em que não foram tomados')
    print('-' * 100)

    while True:
        escolha_usuario = input('Por favor escolha a opção desejada: ')
        print('-' * 100)

        if escolha_usuario.isnumeric():
            if 8 > int(escolha_usuario) >= 0:
                return escolha_usuario
                
            else:
                print('Escolha somente as opções listadas')
                print('-' * 100)

        else:
            print('Por favor utilize números na escolha')
            print('-' * 100)


if __name__ == "__main__":

    cpf = cpf_entrada()
    conexao = conexao_oracle()

    if login(conexao, cpf) == False:
        print("Você escolheu sair!")
        print('-' * 100)
        print((' ' * 30) + 'Obrigado por usar MediTracker! <3')
        print('-' * 100)
        timer(5)

    else:
        while True:
            menu = menu_inicial()
            
            if menu == '0':
                print("Você escolheu sair!")
                print('-' * 100)
                print((' ' * 30) + 'Obrigado por usar MediTracker! <3')
                print('-' * 100)
                conexao.close
                timer(5)
                break

            elif menu == '1':
                print('-' * 100)
                print('Voce escolheu adicionar informações diárias')
                print('-' * 100)
                dados_diario(conexao, cpf)

            elif menu == '2':
                print('-' * 100)
                print('Voce escolheu alterar dados pessoais')
                print('-' * 100)
                escolha = escolha_usuario()
                alterar_dados_pessoais(conexao, cpf, escolha)


            elif menu == '3':
                print('-' * 100)
                print('Voce escolheu excluir seus dados pessoais')
                print('-' * 100)
                excluir_dados_pessoais(conexao, cpf)

                
            elif menu == '4':
                print('-' * 100)
                remedios_tomados(conexao)
                print('-' * 100)

            elif menu == '5':
                print('-' * 100)
                registros_diarios(conexao)
                print('-' * 100)

            elif menu == '6':
                print('-' * 100)
                medicamentos_nao_tomados(conexao)
                print('-' * 100)

