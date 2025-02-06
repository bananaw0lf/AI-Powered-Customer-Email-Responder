🚀 AI-Powered Customer Email Responder (Serverless, AWS-based RAG System)

This is a fully serverless AI-driven email response system built on AWS. It automatically detects incoming customer emails, retrieves relevant data from a knowledge base when necessary, and generates accurate replies using LLMs. The system then autonomously sends responses to customers, streamlining customer support and improving efficiency.

🛠 Architecture Overview ((https://github.com/bananaw0lf/AI-Powered-Customer-Email-Responder/blob/main/diagram.png))
1️⃣ AWS SES detects incoming customer emails and forwards them to SNS (or S3).
2️⃣ SNS triggers Lambda 1, which calls the AWS Bedrock API to generate a response. The response is stored in DynamoDB.
3️⃣ DynamoDB triggers Lambda 2, which sends the generated response email back to the customer.

🔍 Retrieval-Augmented Generation (RAG) Features

Uses AWS Bedrock Agent and Knowledge Base connected to Redshift.
Retrieves customer payment details from the knowledge base when necessary.
Agent calculates relevant time-based information based on payment details.
DynamoDB stores all email interactions, enabling both single email inspection and high-level analysis of customer communications.
