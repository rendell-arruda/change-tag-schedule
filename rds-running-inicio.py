import boto3

account_id = "471112936182"
regions = ["us-east-1"]

# rds_clusters_name = ["cluster-rds-tag", "rds-test-tag-schedule", "cluster3"]
rds_clusters_name = ["rds-test-tag-schedule"]

session = boto3.Session(profile_name="sandbox")

def update_tag_to_running(rds_client, region, rds_cluster_id):
    try:
        response = rds_client.list_tags_for_resource(
            ResourceName=f'arn:aws:rds:{region}:{account_id}:db:{rds_cluster_id}'
        )
        current_tags = response['TagList']
        
        for tag in current_tags:
            if tag['Key'] == 'Schedule':
                print(tag['Value'])
        
    except Exception as e:
        print(f"Erro ao atualizar o cluster {rds_cluster_id} na região {region}: {str(e)}")
        
def lambda_handler():
    for region in regions:
        rds_client = session.client('rds', region_name=region)
        
        for rds_cluster_id in rds_clusters_name:
            update_tag_to_running(rds_client, region, rds_cluster_id)
        
        
if __name__ == "__main__":
    lambda_handler()