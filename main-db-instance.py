import boto3
import csv

def update_rds_tag_if_exists(rds_arn):
    # Inicializa a sessão com o perfil "sandbox"
    session = boto3.Session(profile_name='sandbox')
    
    # Inicializa o cliente do RDS a partir da sessão
    rds_client = session.client('rds')
    
    try:
        # Obtém as tags existentes para o cluster ou instância RDS
        response = rds_client.list_tags_for_resource(
            ResourceName=rds_arn  # ARN completo do cluster ou instância RDS
        )
        current_tags = response['TagList']
        
        # Verifica se a tag "Schedule" existe
        schedule_tag = next((tag for tag in current_tags if tag['Key'] == 'Schedule'), None)
        
        if schedule_tag:
            # Se a tag "Schedule" existir, atualiza o valor para "running"
            updated_tags = [{'Key': 'Schedule', 'Value': 'running'}]
            
            # Aplica a tag atualizada na instância ou cluster RDS
            rds_client.add_tags_to_resource(
                ResourceName=rds_arn,  # Aqui você já tem o ARN correto
                Tags=updated_tags
            )
            print(f"Tag 'Schedule' atualizada para 'running' na instância {rds_arn}")
        else:
            print(f"A instância {rds_arn} não possui a tag 'Schedule', sem atualização necessária.")
    
    except Exception as e:
        print(f"Erro ao atualizar a instância {rds_arn}: {str(e)}")

# Exemplo de uso
update_rds_tag_if_exists("arn:aws:rds:us-east-1:471112936182:db:database-1")
