# EC2UtilizationAnalyzer

**EC2UtilizationAnalyzer** is a Python script for AWS that identifies and reports EC2 instances with low CPU utilization over the past week. This tool is designed to assist in efficient resource management and cost optimization.

## Features

- Retrieve information about running EC2 instances in specified AWS regions.
- Calculate CPU utilization metrics using AWS CloudWatch data.
- Identify instances with CPU utilization less than 10% over the past week.
- Generate an email report with a summary of low-utilization instances.

## How to Use

1. Clone this repository or download the Python script (`ec2_utilization_analyzer.py`).

2. Set up AWS credentials using the AWS CLI or environment variables.

3. Install required Python libraries using `pip`:
  pip install pandas boto3

4. Modify the regions list and email settings in the script to suit your AWS environment.

5. Run the script:
  python ec2_utilization_analyzer.py
6. Check your email for a report on EC2 instances with low CPU utilization.

## Configuration

- Adjust the `regions` list to specify the AWS regions you want to analyze.
- Configure email settings in the script to receive reports.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

- Anshuman Thakur

Feel free to contribute, report issues, or suggest improvements.

Enjoy optimizing your EC2 resources!
