import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
bedrock = boto3.client("bedrock-runtime")

def lambda_handler(event, context):
    path = event.get("rawPath", "")

    if path.endswith("/submit-scores"):
        body = json.loads(event["body"])
        student_id = body.get("student_id", "anonymous")
        scores = body["scores"]

        table.put_item(Item={
            "student_id": student_id,
            "scores": scores
        })

        strengths = [k for k, v in scores.items() if v >= 75]
        weaknesses = [k for k, v in scores.items() if v < 50]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Scores submitted",
                "strengths": strengths,
                "weaknesses": weaknesses
            })
        }

    elif path.endswith("/llm-recommend"):
        body = json.loads(event["body"])
        scores = body["scores"]

        prompt = f"Student scores: {json.dumps(scores, indent=2)}. Recommend 3 books and habits to improve."

        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 300,
                "temperature": 0.7
            })
        )

        completion = json.loads(response['body'].read())['completion']

        return {
            "statusCode": 200,
            "body": json.dumps({"message": completion.strip()})
        }

    return {"statusCode": 404, "body": json.dumps({"message": "Not Found"})}