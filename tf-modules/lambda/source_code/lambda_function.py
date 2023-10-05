import ec2 as ec2


def lambda_handler(event, context):
    ec2.get_instances_list()




