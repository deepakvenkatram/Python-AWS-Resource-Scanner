# 🛠️ AWS Resource Scanner

Overview

AWS Resource Scanner is a Python-based automation script designed to scan and report key AWS resources in your account. It offers a high-level view of your AWS environment to help with cost optimization, resource visibility, and governance.

The script extracts details from the following AWS services:

EC2 Instances: Instance ID, EBS Volume ID, Region, Status
Elastic IPs: Public IPs in use and unused, with deletion candidates identified
S3 Buckets: Bucket Name, Size, Last Modified, and Status
EKS Clusters: Cluster Name, Region, Status, and Metadata
FSx File Systems: Resource ID, Region, Status, and Configuration

All results are exported to a structured CSV report for further analysis.

Features & Benefits

🔍 Comprehensive Inventory: Gain a complete view of critical AWS services and their current states.
💰 Cost Optimization: Identify unused Elastic IPs and underutilized resources to reduce monthly spend.
📈 Operational Visibility: Export data to CSV for compliance audits, reporting, or integration with dashboards.
⚙️ Simple & Scriptable: Lightweight script suitable for scheduled runs via cron or CI/CD workflows.

🧰 Requirements

Python 3.10
AWS CLI (configured with valid credentials)
Python Libraries: `boto3`, `pandas`

📦 Install Dependencies

On Ubuntu system

sudo apt update
sudo apt install python3.10 python3-pip -y
pip install boto3 pandas


🔐 Install & Configure AWS CLI

On ubuntu system - Install AWS CLI
sudo apt install awscli -y

Configure Your AWS cli with credentials
aws configure

During configuration, you'll be prompted to input the below details, so keep it handy.

* AWS Access Key ID
* AWS Secret Access Key
* Default region (e.g. `us-east-1`)
* Output format (`json`, `table`, or `text`)

🚀 How to Use

1. Clone this repository or download the script.
2. Ensure your AWS CLI is configured with the appropriate IAM permissions (read-only is sufficient).
3. Run the script, using the below command

python3.10 aws_audit.py

4. The output CSV file (e.g., `aws_resource_audit_report.csv`) will be generated in your working directory.

📌 IAM Permissions Required

Ensure the AWS credentials used have the following read permissions:

* `ec2:DescribeInstances`
* `ec2:DescribeAddresses`
* `s3:ListAllMyBuckets`
* `s3:GetBucketLocation`
* `eks:ListClusters`
* `eks:DescribeCluster`
* `fsx:DescribeFileSystems`

💡 AWS Native Alternatives

You can also explore AWS-native tools that provide similar visibility:

AWS Trusted Advisor - Provides real-time guidance to help provision resources following AWS best practices .
AWS Cost Explorer - Visualize, understand, and manage your AWS costs and usage over time.
AWS Config - Records and evaluates configurations of your AWS resources.
Resource Explorer - Quickly search and discover AWS resources across regions.

You can use this script in **conjunction** with these tools to supplement automation workflows, CI/CD reporting, or as part of an internal governance dashboard.

📞 Support

For issues, feature requests, or contributions, please open a GitHub Issue or Pull Request.

📜 License

Let me know if you'd like the actual script content structured or templated next.

More scripts like this are coming soon — follow for updates!

👤 Author

Deepak Venkatram – https://github.com/deepakvenkatram 
