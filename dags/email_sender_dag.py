from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import pandas as pd
import unicodedata
import os
from datetime import datetime


# Configuração da conta do email
load_dotenv()
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

# Caminho da pasta onde os arquivos csv estão armazenados
PASTA_ENVIOS = os.getenv("PASTA_ENVIOS")

# Função para enviar e-mail com anexo
def send_email(destinatario, file_path):
    try:
        # Extrair o nome do gerente a partir do nome do arquivo
        nome_arquivo = file_path.split('/')[-1]
        nome_gerente = nome_arquivo.replace("teste_tratado_", "").replace(".xlsx", "")

        # Criar mensagem do corpo do email
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = destinatario
        msg['Subject'] = "Relatório de Saldo de Banco de Horas"

        # Mensagem customizada com o nome do gerente em questão
        corpo_email = f"""{nome_gerente}, bom dia! Segue anexo a lista do saldo de banco de horas dos colaboradores do time."""

        msg.attach(MIMEText(corpo_email, 'plain'))

        # Anexar arquivo elaborado
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={file_path.split('/')[-1]}")
            msg.attach(part)

        # Configurar servidor SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, SENHA)
        server.sendmail(EMAIL, destinatario, msg.as_string())
        server.quit()
        
        print(f"Email enviado para {destinatario} com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar e-mail para {destinatario}: {str(e)}")



def extract_data(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id = 'postgresql_padrao')
    sql_query = """SELECT * FROM public.tb_banco_horas WHERE "Saldo_Horas" < 0;"""

    conn = pg_hook.get_conn()
    df = pd.read_sql(sql_query, conn)

    kwargs['ti'].xcom_push(key='dataframe_dados', value=df.to_json())


def transform_data(**kwargs):
    ti = kwargs['ti']
    df = pd.read_json(ti.xcom_pull(key='dataframe_dados', task_ids='extract_data'))

    df_tratado = df[df['Unidade'] == 'Unidade 9']
    
    output_dir = PASTA_ENVIOS
    os.makedirs(output_dir, exist_ok=True)
    
    for gerente in df_tratado['Gerente_Tecnico'].unique():
        nome_gerente_clean = unicodedata.normalize('NFKD', gerente).encode('ASCII', 'ignore').decode('ASCII')
        file_path = os.path.join(output_dir, f"teste_tratado_{nome_gerente_clean}.xlsx")
        df_tratado[df_tratado['Gerente_Tecnico'] == gerente].to_excel(file_path, index=False)


def enviar_emails(**kwargs):
    # Listar todos os arquivos na pasta de envios
    arquivos = [f for f in os.listdir(PASTA_ENVIOS) if f.endswith(".xlsx")]

    for arquivo in arquivos:
        file_path = os.path.join(PASTA_ENVIOS, arquivo)
        
        try:
            # Ler o arquivo Excel como DataFrame
            df = pd.read_excel(file_path)

            # Verificar se a coluna "email" existe
            if "Email" in df.columns:
                destinatario = df["Email"].iloc[0]  # Pega o primeiro email encontrado

                # Enviar e-mail com o arquivo como anexo
                send_email(destinatario, file_path)
            else:
                print(f"A coluna 'email' não foi encontrada no arquivo: {arquivo}")

        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo}: {str(e)}")
    

with DAG('email_sender',
         start_date = datetime(2025, 2, 23),
         schedule_interval=None, catchup=False) as dag:


    extract_task = PythonOperator(
        task_id = 'extract_data',
        python_callable=extract_data,
        provide_context=True
        )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True
    )

    enviar_emails = PythonOperator(
        task_id='enviar_emails',
        python_callable=enviar_emails,
        provide_context=True
    )

 
extract_task >> transform_data >> enviar_emails