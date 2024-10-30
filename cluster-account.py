import boto3

# Configura as credenciais de acesso e informações da conta
aws_access_key = 'YOUR_ACCESS_KEY'          # Substitua por sua chave de acesso
aws_secret_key = 'YOUR_SECRET_KEY'          # Substitua por sua chave secreta
account_id = '471112936182'                 # Substitua pelo ID da sua conta
regions = ['us-east-1', 'us-west-1', 'eu-west-1']  # Substitua pelas regiões desejadas

def update_rds_cluster_tag_if_exists(rds_client, region, rds_cluster_id):
    try:
        response = rds_client.list_tags_for_resource(
            ResourceName=f'arn:aws:rds:{region}:{account_id}:cluster:{rds_cluster_id}'
        )
        current_tags = response['TagList']
        schedule_tag = next((tag for tag in current_tags if tag['Key'] == 'Schedule'), None)
        
        if schedule_tag:
            updated_tags = [{'Key': 'Schedule', 'Value': 'running'}]
            rds_client.add_tags_to_resource(
                ResourceName=f'arn:aws:rds:{region}:{account_id}:cluster:{rds_cluster_id}',
                Tags=updated_tags
            )
            print(f"Tag 'Schedule' atualizada para 'running' no cluster {rds_cluster_id} na região {region}")
        else:
            print(f"O cluster {rds_cluster_id} na região {region} não possui a tag 'Schedule', sem atualização necessária.")
    
    except Exception as e:
        print(f"Erro ao atualizar o cluster {rds_cluster_id} na região {region}: {str(e)}")

def lambda_handler(event, context):
    # Obtém a lista de IDs dos clusters RDS do JSON enviado na chamada
    rds_clusters = event.get("rds_clusters", [])
    
    # Verifica se a lista não está vazia
    if not rds_clusters:
        return {"message": "Nenhum cluster RDS fornecido para atualização."}

    # Itera sobre cada região e cada cluster
    for region in regions:
        rds_client = boto3.client(
            'rds',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        
        for rds_cluster_id in rds_clusters:
            update_rds_cluster_tag_if_exists(rds_client, region, rds_cluster_id)

    return {"message": "Processamento concluído para todos os clusters RDS fornecidos."}

