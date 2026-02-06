# import os
# import boto3
# from moto import mock_aws

# # --------------------------------------------------
# # MOCK AWS CREDENTIALS (MUST BE SET FIRST)
# # --------------------------------------------------
# os.environ["AWS_ACCESS_KEY_ID"] = "testing"
# os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
# os.environ["AWS_SESSION_TOKEN"] = "testing"
# os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# REGION = "us-east-1"

# # --------------------------------------------------
# # START MOTO MOCK (INTERCEPTS ALL boto3 CALLS)
# # --------------------------------------------------
# mock = mock_aws()
# mock.start()

# # IMPORTANT: import AFTER mock.start()
# from app_aws import app
# import app_aws


# def setup_infrastructure():
#     print(">>> Creating Mock AWS Infrastructure (DynamoDB + SNS)")

#     dynamodb = boto3.resource("dynamodb", region_name=REGION)
#     sns = boto3.client("sns", region_name=REGION)

#     # -------------------------
#     # DynamoDB Tables
#     # -------------------------

#     dynamodb.create_table(
#         TableName="Students",
#         KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
#         AttributeDefinitions=[{"AttributeName": "email", "AttributeType": "S"}],
#         BillingMode="PAY_PER_REQUEST"
#     )

#     dynamodb.create_table(
#         TableName="Books",
#         KeySchema=[{"AttributeName": "book_id", "KeyType": "HASH"}],
#         AttributeDefinitions=[{"AttributeName": "book_id", "AttributeType": "S"}],
#         BillingMode="PAY_PER_REQUEST"
#     )

#     dynamodb.create_table(
#         TableName="Requests",
#         KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
#         AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
#         BillingMode="PAY_PER_REQUEST"
#     )

#     # -------------------------
#     # SNS Topic
#     # -------------------------
#     topic = sns.create_topic(Name="LibraryRequests")
#     app_aws.SNS_TOPIC_ARN = topic["TopicArn"]

#     print(">>> Mock AWS Ready")
#     print(f">>> SNS Topic ARN: {app_aws.SNS_TOPIC_ARN}")


# # --------------------------------------------------
# # RUN SERVER WITH MOCKED AWS
# # --------------------------------------------------
# if __name__ == "__main__":
#     try:
#         setup_infrastructure()
#         print("\n>>> Flask running at http://localhost:5000")
#         print(">>> AWS is FULLY MOCKED (Moto)")
#         print(">>> Stop with CTRL+C")

#         # use_reloader=False is CRITICAL
#         app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

#     finally:
#         mock.stop()
#         print("\n>>> Mock AWS stopped")













#WORKING
# import os
# import boto3
# from moto import mock_aws

# # --------------------------------------------------
# # MOCK AWS CREDENTIALS (MUST BE SET FIRST)
# # --------------------------------------------------
# os.environ["AWS_ACCESS_KEY_ID"] = "testing"
# os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
# os.environ["AWS_SESSION_TOKEN"] = "testing"
# os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# REGION = "us-east-1"

# # --------------------------------------------------
# # START MOTO MOCK
# # --------------------------------------------------
# mock = mock_aws()
# mock.start()

# # IMPORTANT: import AFTER mock.start()
# from app_aws import app
# import app_aws


# def setup_infrastructure():
#     print(">>> Creating Mock AWS Infrastructure (DynamoDB + SNS)")

#     dynamodb = boto3.resource("dynamodb", region_name=REGION)
#     sns = boto3.client("sns", region_name=REGION)

#     # --------------------------------------------------
#     # DYNAMODB TABLES
#     # --------------------------------------------------

#     dynamodb.create_table(
#         TableName="Students",
#         KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
#         AttributeDefinitions=[{"AttributeName": "email", "AttributeType": "S"}],
#         BillingMode="PAY_PER_REQUEST"
#     )

#     dynamodb.create_table(
#         TableName="Books",
#         KeySchema=[{"AttributeName": "book_id", "KeyType": "HASH"}],
#         AttributeDefinitions=[{"AttributeName": "book_id", "AttributeType": "S"}],
#         BillingMode="PAY_PER_REQUEST"
#     )

#     dynamodb.create_table(
#         TableName="Requests",
#         KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
#         AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
#         BillingMode="PAY_PER_REQUEST"
#     )

#     # --------------------------------------------------
#     # SEED BOOK DATA (CRITICAL FIX)
#     # --------------------------------------------------
#     books_table = dynamodb.Table("Books")

#     books_table.put_item(Item={
#         "book_id": "B101",
#         "title": "Engineering Mathematics",
#         "subject": "Mathematics",
#         "available": False,
#         "s3_url": "https://mock-bucket.s3.amazonaws.com/math.pdf"
#     })

#     books_table.put_item(Item={
#         "book_id": "B102",
#         "title": "Discrete Mathematics",
#         "subject": "Mathematics",
#         "available": True,
#         "s3_url": "https://mock-bucket.s3.amazonaws.com/discrete.pdf"
#     })

#     books_table.put_item(Item={
#         "book_id": "B201",
#         "title": "English Grammar & Composition",
#         "subject": "English",
#         "available": False,
#         "s3_url": "https://mock-bucket.s3.amazonaws.com/english.pdf"
#     })

#     # --------------------------------------------------
#     # SNS TOPIC
#     # --------------------------------------------------
#     topic = sns.create_topic(Name="LibraryRequests")
#     app_aws.SNS_TOPIC_ARN = topic["TopicArn"]

#     print(">>> Mock AWS Ready")
#     print(f">>> SNS Topic ARN: {app_aws.SNS_TOPIC_ARN}")


# # --------------------------------------------------
# # RUN FLASK APP WITH MOCKED AWS
# # --------------------------------------------------
# if __name__ == "__main__":
#     try:
#         setup_infrastructure()

#         print("\n>>> Flask running at http://localhost:5000")
#         print(">>> AWS is FULLY MOCKED using Moto")
#         print(">>> Books are preloaded")
#         print(">>> Stop server with CTRL+C")

#         # IMPORTANT: disable reloader or mock state is lost
#         app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

#     finally:
#         mock.stop()
#         print("\n>>> Mock AWS stopped")
















import os
import boto3
from moto import mock_aws

# --------------------------------------------------
# MOCK AWS CREDENTIALS (MUST BE SET FIRST)
# --------------------------------------------------
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

REGION = "us-east-1"

# --------------------------------------------------
# START MOTO MOCK
# --------------------------------------------------
mock = mock_aws()
mock.start()

# IMPORTANT: import AFTER mock.start()
from app_aws import app
import app_aws


def setup_infrastructure():
    print(">>> Creating Mock AWS Infrastructure (DynamoDB + SNS)")

    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    sns = boto3.client("sns", region_name=REGION)

    # --------------------------------------------------
    # DYNAMODB TABLES
    # --------------------------------------------------
    dynamodb.create_table(
        TableName="Students",
        KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "email", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

    dynamodb.create_table(
        TableName="Books",
        KeySchema=[{"AttributeName": "book_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "book_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

    dynamodb.create_table(
        TableName="Requests",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

    # --------------------------------------------------
    # SEED BOOK DATA (LOCAL MOCK PDF LINKS)
    # --------------------------------------------------
    books_table = dynamodb.Table("Books")

    books_table.put_item(Item={
        "book_id": "B101",
        "title": "Engineering Mathematics",
        "subject": "Mathematics",
        "available": False,
        "s3_url": "/static/books/Engineering_Maths.pdf"   # LOCAL MOCK PDF
    })

    books_table.put_item(Item={
        "book_id": "B102",
        "title": "Discrete Mathematics",
        "subject": "Mathematics",
        "available": True,
        "s3_url": "/static/books/Discrete_Maths.pdf"  # LOCAL MOCK PDF
    })

    books_table.put_item(Item={
        "book_id": "B201",
        "title": "English Grammar & Composition",
        "subject": "English",
        "available": False,
        "s3_url": "/static/books/English_Grammar&Composition.pdf"   # LOCAL MOCK PDF
    })

    # --------------------------------------------------
    # SNS TOPIC (MOCKED) – must be a valid string to avoid errors
    # --------------------------------------------------
    topic = sns.create_topic(Name="LibraryRequests")
    app_aws.SNS_TOPIC_ARN = topic["TopicArn"]

    print(">>> Mock AWS Ready")
    print(f">>> SNS Topic ARN (mocked): {app_aws.SNS_TOPIC_ARN}")


# --------------------------------------------------
# RUN FLASK APP WITH MOCKED AWS
# --------------------------------------------------
if __name__ == "__main__":
    try:
        setup_infrastructure()

        print("\n>>> Flask running at http://localhost:5000")
        print(">>> AWS is FULLY MOCKED using Moto")
        print(">>> Books are preloaded")
        print(">>> Stop server with CTRL+C")

        # IMPORTANT: disable reloader or mock state is lost
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

    finally:
        mock.stop()
        print("\n>>> Mock AWS stopped")
