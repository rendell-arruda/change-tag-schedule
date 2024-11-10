''' 

CHANGE TAG SCHEDULE RDS CLUSTER
O  intuito desse script é verificar se o cluster está com a tag Schedule e atualizar a tag para o valor desejado.
Os parâmetros que devem ser alterados são:
- account_id: ID da conta AWS
- region: região em que os clusters RDS estão localizados
- rds_clusters_name: Lista de clusters que devem ser verificados
- desired_tag_value: Valor desejado para a tag 'Schedule'
'''

import boto3
import os

# Recupera as variáveis de ambiente definidas no Lambda para configurar parâmetros
account_id = os.environ.get("ACCOUNT_ID")                # ID da conta AWS alvo para os clusters
region = os.environ.get("REGION")                        # Região onde os clusters RDS estão localizados
list_clusters_rds = [cluster.strip() for cluster in os.environ.get("RDS_CLUSTERS").split(",")]  # Lista de IDs dos clusters RDS, separados por vírgula
desired_tag_value = os.environ.get("DESIRED_TAG_VALUE")  # Valor desejado para a tag 'Schedule'

# Função para atualizar a tag 'Schedule' de um cluster RDS específico
def update_tag_schedule(client, region, rds_cluster_id, tag_value):
    try:
        # Obtém as tags atuais do cluster
        response = client.list_tags_for_resource(
            ResourceName=f'arn:aws:rds:{region}:{account_id}:db:{rds_cluster_id}'
        )
        current_tags = response['TagList']  # Lista de tags atuais do cluster
        
        # Verifica se a tag 'Schedule' já existe no cluster
        schedule_tag = next((tag for tag in current_tags if tag['Key'] == 'Schedule'), None)
        
        # Atualiza a tag 'Schedule' para o valor desejado se ela já existir
        if schedule_tag:
            updated_tags = [{'Key': 'Schedule', 'Value': tag_value}]
            client.add_tags_to_resource(
                ResourceName=f'arn:aws:rds:{region}:{account_id}:db:{rds_cluster_id}',
                Tags=updated_tags
            )
            print(f"Tag 'Schedule' atualizada para {tag_value} no cluster {rds_cluster_id}")
        else:
            print(f"O cluster {rds_cluster_id} não possui a tag 'Schedule', sem atualização necessária.")
        
    # Captura e exibe quaisquer erros que ocorram durante o processo de atualização de tags
    except Exception as e:
        print(f"Erro ao atualizar o cluster {rds_cluster_id} na região {region}: {str(e)}")
        
# Função principal executada pelo AWS Lambda
def lambda_handler(event, context):
    # Assume a role para permitir acesso cross-account ao cluster
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/role-secundary-describe-rds",
        RoleSessionName="cross_acct_lambda"
    )

    # Extrai as credenciais temporárias obtidas pela role assumida
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # Cria um cliente RDS com as credenciais da role assumida para acessar os clusters na conta de destino
    client = boto3.client(
        'rds',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    # Itera sobre a lista de clusters e atualiza a tag 'Schedule' para cada um deles
    for rds_cluster_id in list_clusters_rds:
        update_tag_schedule(client, region, rds_cluster_id, desired_tag_value)
