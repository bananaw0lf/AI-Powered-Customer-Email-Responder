🚀 AI-Powered Customer Email Responder (Serverless, AWS-based RAG System)

This is a fully serverless AI-driven email response system built on AWS. It automatically detects incoming customer emails, retrieves relevant data from a knowledge base when necessary, and generates accurate replies using LLMs. The system then autonomously sends responses to customers, streamlining customer support and improving efficiency.

🌟 System Features

✅ Serverless & Fully Managed – No infrastructure to maintain, leveraging AWS services.

✅ Fully Automated – Runs end-to-end without human intervention.

✅ 100% on AWS – Utilizes AWS-native services for seamless integration.

✅ Extensible & Scalable – All data is stored in DynamoDB, enabling additional features like analytics and managerial insights.

🛠 Architecture Overview (https://github.com/bananaw0lf/AI-Powered-Customer-Email-Responder/blob/main/diagram.png)

1️⃣ AWS SES detects incoming customer emails and forwards them to SNS (or S3).

2️⃣ SNS triggers Lambda 1, which calls the AWS Bedrock API to generate a response. The response is stored in DynamoDB.

3️⃣ DynamoDB triggers Lambda 2, which sends the generated response email back to the customer.

🔍 Retrieval-Augmented Generation (RAG) Features

· Uses AWS Bedrock Agent and Knowledge Base connected to Redshift.
· Retrieves customer payment details from the knowledge base when necessary. (in my case)
· Agent calculates relevant time-based information based on payment details. (in my case)
· DynamoDB stores all email interactions, enabling both single email inspection and high-level analysis of customer communications.
