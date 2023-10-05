import pandas as pd
from datetime import datetime, timedelta
import boto3
import mail
import tags

def get_instances_list():
    print("Started Execution for ec2 service: ")
    regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    ec2_details = []
    for i in range(len(regions)):

        print(f"\tRegion Name = {regions[i]}")
        cloudwatch = boto3.client('cloudwatch', region_name=regions[i])
        ec2 = boto3.client('ec2', region_name=regions[i])
        instances = ec2.describe_instances()
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                cpu_metrics = cloudwatch.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': instance['InstanceId']
                        },
                    ],
                    StartTime=datetime.utcnow() - timedelta(seconds=604800),
                    EndTime=datetime.utcnow(),
                    Period=604800,
                    Statistics=['Average', 'Maximum'],
                )
                if len(cpu_metrics['Datapoints']) > 0 and cpu_metrics['Datapoints'][0]['Maximum'] < 10 and \
                        instance['State']['Name'] == 'running':
                    if instance["NetworkInterfaces"]:
                        s_group = instance["NetworkInterfaces"][0]["Groups"][0]["GroupName"]
                    else:
                        s_group = '---'
                    # print(instance)
                    name_ec2 = tags.find_dates_main(instance['Tags'], instance['InstanceId'])
                    dict = {
                        'AvailabilityZone': regions[i],
                        'Instance_id': instance['InstanceId'],
                        'CPU_Utilization': round(cpu_metrics['Datapoints'][0]['Maximum'], 2),
                        'instance_type': instance["InstanceType"],
                        'Ec2_Ins_Name' : name_ec2[1]['Value'],
                        'Security_group': s_group,

                    }
                    # print(dict)
                    ec2_details.append(dict)
    if not ec2_details:
        ec2_details.append({'Details':'There is No Ec2 instances which are utilizing less than 10% over a week'})
        df = pd.DataFrame(ec2_details)
    else:
        df = pd.DataFrame(ec2_details)
        df = df.sort_values('CPU_Utilization', ascending=True,ignore_index=True)
        df['CPU_Utilization'] = df['CPU_Utilization'].astype(str) + '%'
    subject=f"Less Utilized EC2 instances in Dev(082) Account | Week - {datetime.utcnow().isocalendar()[1]}"
    body=f"<pre>The following ec2 instances have less than 10% CPU utilization over a week in these regions(us-east-1, us-east-2, us-west-1 & us-west-2).</pre><br>{df.to_html()}"
    mail.SendMail(subject,body)

