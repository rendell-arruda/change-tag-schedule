'''
O  intuito desse script é verificar se o cluster está com a tag Schedule com o valor running, caso não esteja, ele irá atualizar a tag para running.
Os parâmetros que devem ser alterados são:
- account_id: ID da conta AWS
- regions: Lista de regiões que devem ser verificadas
- rds_clusters_name: Lista de clusters que devem ser verificados
- profile_name: Nome do profile que será utilizado para realizar a autenticação na AWS
- tag_key: Nome da tag que será verificada
- tag_value: Valor da tag que será verificada
'''

import boto3
account_id = "266549158321"
regions = ["us-east-1"]
list__clusters_rds = ["rds-test-tag-schedule"]
desired_tag_value = "stopped"


def update_tag_schedule(client, region, rds_cluster_id, desired_tag_value):
    # faz o descibre do cluster:
    try:
        response = client.list_tags_for_resource(
            ResourceName=f'arn:aws:rds:{region}:{account_id}:db:{rds_cluster_id}'
        )
        current_tags = response['TagList']
        
        schedule_tag = next((tag for tag in current_tags if tag['Key'] == 'Schedule'), None)
        
        if schedule_tag:
            updated_tags = [{'Key': 'Schedule', 'Value': desired_tag_value}]
            client.add_tags_to_resource(
                ResourceName=f'arn:aws:rds:{region}:{account_id}:db:{rds_cluster_id}',
                # ResourceName=f'arn:aws:rds:{region}:{account_id}:cluster:{rds_cluster_id}',
                Tags=updated_tags
            )
            print(f"Tag 'Schedule' atualizada para {desired_tag_value} no cluster {rds_cluster_id} na região {region}")
        else:
            print(f"O cluster {rds_cluster_id} na região {region} não possui a tag 'Schedule', sem atualização necessária.")
        
    except Exception as e:
        print(f"Erro ao atualizar o cluster {rds_cluster_id} na região {region}: {str(e)}")
        
def lambda_handler(event, context):
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::266549158321:role/role-secundary-describe-rds",
        RoleSessionName="cross_acct_lambda"
    )

    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # create service client using the assumed role credentials, e.g. S3
    client = boto3.client(
        'rds',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    
    for region in regions:
        for rds_cluster_id in list__clusters_rds:
            update_tag_schedule(client, region, rds_cluster_id, desired_tag_value)

        
        
if __name__ == "__main__":
    lambda_handler()