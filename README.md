# Data-Pipelines
## Introduction
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

You are to create a dag to load the data, create required fact and dimension tables and check the data quality.
![image](https://github.com/SwethaaRaya/Data-Pipelines/assets/90500990/d94ddbcc-648d-4f67-b821-afd15edc41cc)

## Prerequisites:
Create an IAM User in AWS.
Configure Redshift Serverless in AWS.
## Setting up Connections
Connect Airflow and AWS
Connect Airflow to AWS Redshift Serverless

## Datasets
Here are the s3 links for each:
**Log data:** s3://udacity-dend/log_data
**Song data:** s3://udacity-dend/song_data

## Steps:
1. Copy the data to your s3 bucket 'raya-swethaa'.
  a. aws s3 cp s3://udacity-dend/log-data/ s3://raya-swethaa/log-data/ --recursive
  b. aws s3 cp s3://udacity-dend/song-data/ s3://raya-swethaa/song-data/ --recursive
  c. aws s3 cp s3://udacity-dend/log_json_path.json s3://raya-swethaa/
2. Complete the final_project.py dag and the operqator codes required for it.
  Configure following in Dag
    The DAG does not have dependencies on past runs
      On failure, the task are retried 3 times
      Retries happen every 5 minutes
      Catchup is turned off
      Do not email on retry
  Connect the tasks as per image shown above
4. ** Stage Operator**
  The stage operator is expected to be able to load any JSON-formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters 
  should specify where in S3 the file is loaded and what is the target table.
5. ** Fact and Dimension Operator**
  Most of the logic is within the SQL transformations, and the operator is expected to take as input a SQL statement and target database on which to run the query against. You can also define a target table that will 
  contain the results of the transformation.
6. ** Data Quality Operator**
  The data quality operator, which runs checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each test, the 
  test result and expected result need to be checked, and if there is no match, the operator should raise an exception, and the task should retry and fail eventually.
