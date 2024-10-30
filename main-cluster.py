import boto3  # Importa o boto3, uma biblioteca para interagir com os serviços AWS
import csv    # Importa o módulo CSV para ler arquivos CSV

# Função que atualiza a tag "Schedule" para "running" em um cluster RDS, se a tag existir
def update_rds_cluster_tag_if_exists(rds_cluster_id):
    # Inicializa o cliente do RDS usando boto3
    rds_client = boto3.client('rds')
    
    # Define a região e o ID da conta AWS (substitua pelos seus valores)
    REGION = 'us-east-1'  
    ACCOUNT_ID = '471112936182'  
    
    try:
        # Obtém as tags existentes do cluster RDS especificado pelo ARN
        response = rds_client.list_tags_for_resource(
            ResourceName=f'arn:aws:rds:{REGION}:{ACCOUNT_ID}:cluster:{rds_cluster_id}'
        )
        # Extrai a lista de tags da resposta da API
        current_tags = response['TagList']
        
        # Verifica se a tag "Schedule" está presente na lista de tags
        schedule_tag = next((tag for tag in current_tags if tag['Key'] == 'Schedule'), None)
        
        # Se a tag "Schedule" existir, atualiza o valor para "running"
        if schedule_tag:
            updated_tags = [{'Key': 'Schedule', 'Value': 'running'}]
            
            # Aplica a tag atualizada ao cluster RDS
            rds_client.add_tags_to_resource(
                ResourceName=f'arn:aws:rds:{REGION}:{ACCOUNT_ID}:cluster:{rds_cluster_id}',
                Tags=updated_tags
            )
            print(f"Tag 'Schedule' atualizada para 'running' no cluster {rds_cluster_id}")
        else:
            # Informa que a tag "Schedule" não foi encontrada no cluster
            print(f"O cluster {rds_cluster_id} não possui a tag 'Schedule', sem atualização necessária.")
    
    # Trata erros que possam ocorrer ao acessar ou atualizar o cluster RDS
    except Exception as e:
        print(f"Erro ao atualizar o cluster {rds_cluster_id}: {str(e)}")

# Função que processa uma lista de clusters RDS a partir de um arquivo CSV ou TXT
def process_rds_clusters(file_path):
    # Abre o arquivo CSV com os IDs dos clusters RDS
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        # Itera sobre cada linha do arquivo, chamando a função de atualização para cada ID
        for row in reader:
            rds_cluster_id = row[0]
            update_rds_cluster_tag_if_exists(rds_cluster_id)

# Define o caminho do arquivo com os IDs dos clusters RDS
file_path = 'lista_rds_clusters.csv'  # Substitua pelo caminho correto do seu arquivo

# Executa a função de processamento para a lista de clusters RDS
process_rds_clusters(file_path)
