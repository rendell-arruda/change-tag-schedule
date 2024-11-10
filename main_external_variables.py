import boto3
import os

# Recupera as variáveis de ambiente definidas no Lambda
account_id = os.environ.get("ACCOUNT_ID")
region = os.environ.get("REGION") 
list_clusters_rds = [cluster.strip() for cluster in os.environ.get("RDS_CLUSTERS").split(",")]  
desired_tag_value = os.environ.get("DESIRED_TAG_VALUE")

def update_tag_schedule(client, region, rds_cluster_id, tag_value):
    try:
        response = client.list_tags_for_resource(
            ResourceName=f'arn:aws:rds:{region}:{account_id}:db:{rds_cluster_id}'
        )
        current_tags = response['TagList']
        
        schedule_tag = next((tag for tag in current_tags if tag['Key'] == 'Schedule'), None)
        
        if schedule_tag:
            updated_tags = [{'Key': 'Schedule', 'Value': tag_value}]
            client.add_tags_to_resource(
                ResourceName=f'arn:aws:rds:{region}:{account_id}:db:{rds_cluster_id}',
                Tags=updated_tags
            )
            print(f"Tag 'Schedule' atualizada para {tag_value} no cluster {rds_cluster_id}")
        else:
            print(f"O cluster {rds_cluster_id} não possui a tag 'Schedule', sem atualização necessária.")
        
    except Exception as e:
        print(f"Erro ao atualizar o cluster {rds_cluster_id} na região {region}: {str(e)}")
        
def lambda_handler(event, context):
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/role-secundary-describe-rds",
        RoleSessionName="cross_acct_lambda"
    )

    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    client = boto3.client(
        'rds',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    for rds_cluster_id in list_clusters_rds:
        update_tag_schedule(client, region, rds_cluster_id, desired_tag_value)
