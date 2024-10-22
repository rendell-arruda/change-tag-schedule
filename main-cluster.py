import boto3
import csv

def update_rds_cluster_tag_if_exists(rds_cluster_id):
    # Inicializa o cliente do RDS
    rds_client = boto3.client('rds')
    region = 'us-east-1'  # Substitua pela região correta
    account_id = '471112936182'  # Substitua pelo ID da sua conta
    
    try:
        # Obtém as tags existentes para o cluster RDS
        response = rds_client.list_tags_for_resource(
            ResourceName=f'arn:aws:rds:REGION:ACCOUNT_ID:cluster:{rds_cluster_id}'  # Substitua REGION e ACCOUNT_ID
        )
        current_tags = response['TagList']
        
        # Verifica se a tag "Schedule" existe
        schedule_tag = next((tag for tag in current_tags if tag['Key'] == 'Schedule'), None)
        
        if schedule_tag:
            # Se a tag "Schedule" existir, atualiza o valor para "running"
            updated_tags = [{'Key': 'Schedule', 'Value': 'running'}]
            
            # Aplica a tag atualizada no cluster RDS
            rds_client.add_tags_to_resource(
                ResourceName=f'arn:aws:rds:REGION:ACCOUNT_ID:cluster:{rds_cluster_id}',  # Substitua REGION e ACCOUNT_ID
                Tags=updated_tags
            )
            print(f"Tag 'Schedule' atualizada para 'running' no cluster {rds_cluster_id}")
        else:
            print(f"O cluster {rds_cluster_id} não possui a tag 'Schedule', sem atualização necessária.")
    
    except Exception as e:
        print(f"Erro ao atualizar o cluster {rds_cluster_id}: {str(e)}")

def process_rds_clusters(file_path):
    # Lê a lista de clusters RDS de um arquivo CSV ou TXT
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            rds_cluster_id = row[0]
            update_rds_cluster_tag_if_exists(rds_cluster_id)

# Defina o caminho do arquivo com os IDs dos clusters RDS
file_path = 'lista_rds_clusters.csv'  # Substitua pelo caminho correto do seu arquivo

# Executa o script para processar a lista de clusters RDS
process_rds_clusters(file_path)
