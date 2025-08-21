import boto3
import pandas as pd
from datetime import datetime, timezone

# Clients
ec2 = boto3.client("ec2")
s3 = boto3.client("s3")
eks = boto3.client("eks")
fsx = boto3.client("fsx")

report_data = []

# 1. Unused EBS Volumes
def get_unused_ebs_volumes():
    volumes = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"]
    for vol in volumes:
        report_data.append({
            "ResourceType": "EBS Volume",
            "ResourceId": vol["VolumeId"],
            "Region": ec2.meta.region_name,
            "Status": "Unattached",
            "Details": f"Size: {vol['Size']} GiB"
        })

# 2. Unassociated Elastic IPs
def get_unused_elastic_ips():
    eips = ec2.describe_addresses()["Addresses"]
    for eip in eips:
        if "InstanceId" not in eip:
            report_data.append({
                "ResourceType": "Elastic IP",
                "ResourceId": eip["PublicIp"],
                "Region": ec2.meta.region_name,
                "Status": "Unassociated",
                "Details": "Elastic IP not in use"
            })

# 3. S3 Buckets Usage Info
def get_s3_usage_info():
    buckets = s3.list_buckets()["Buckets"]
    for bucket in buckets:
        name = bucket["Name"]
        try:
            region = s3.get_bucket_location(Bucket=name).get("LocationConstraint") or "us-east-1"
            bucket_s3 = boto3.client("s3", region_name=region)
            objects = bucket_s3.list_objects_v2(Bucket=name)
            if "Contents" in objects:
                last_modified = max(obj["LastModified"] for obj in objects["Contents"])
                delta = datetime.now(timezone.utc) - last_modified
                report_data.append({
                    "ResourceType": "S3 Bucket",
                    "ResourceId": name,
                    "Region": region,
                    "Status": "Active",
                    "Details": f"Last Modified: {last_modified.date()}, Unused for {delta.days} days"
                })
            else:
                report_data.append({
                    "ResourceType": "S3 Bucket",
                    "ResourceId": name,
                    "Region": region,
                    "Status": "Empty",
                    "Details": "No objects in bucket"
                })
        except Exception as e:
            report_data.append({
                "ResourceType": "S3 Bucket",
                "ResourceId": name,
                "Region": "Unknown",
                "Status": "Error",
                "Details": str(e)
            })

# 4. EKS Clusters Info
def list_eks_clusters():
    try:
        cluster_names = eks.list_clusters()["clusters"]
        for name in cluster_names:
            cluster = eks.describe_cluster(name=name)["cluster"]
            report_data.append({
                "ResourceType": "EKS Cluster",
                "ResourceId": name,
                "Region": eks.meta.region_name,
                "Status": cluster["status"],
                "Details": f"Created at {cluster['createdAt'].date()}"
            })
    except Exception as e:
        report_data.append({
            "ResourceType": "EKS Cluster",
            "ResourceId": "N/A",
            "Region": eks.meta.region_name,
            "Status": "Error",
            "Details": str(e)
        })

# 5. FSx Info
def list_fsx_usage():
    try:
        filesystems = fsx.describe_file_systems()["FileSystems"]
        for fs in filesystems:
            report_data.append({
                "ResourceType": "FSx",
                "ResourceId": fs["FileSystemId"],
                "Region": fsx.meta.region_name,
                "Status": fs["Lifecycle"],
                "Details": f"Created: {fs['CreationTime'].date()}"
            })
    except Exception as e:
        report_data.append({
            "ResourceType": "FSx",
            "ResourceId": "N/A",
            "Region": fsx.meta.region_name,
            "Status": "Error",
            "Details": str(e)
        })

# Run all checks
get_unused_ebs_volumes()
get_unused_elastic_ips()
get_s3_usage_info()
list_eks_clusters()
list_fsx_usage()

# Output to CSV
df = pd.DataFrame(report_data)
csv_path = "aws_resource_audit_report.csv"
df.to_csv(csv_path, index=False)
print(f"✅ Report saved to {csv_path}")

