import json
from chat import chat_with_gpt


def faq_qa(event, context):
  print("event: ", event)
  if 'queryStringParameters' not in event or 'query' not in event['queryStringParameters']:
    return {
      'statusCode': 400,
      'body': 'query not found in request parameter'
    }
  query = event['queryStringParameters']['query']
  print("query: ", query)
  response = chat_with_gpt(query, 'data/index')
  print(json.dumps({'query': query, 'response': response}))
  return {
    'statusCode': 200,
    'body': response
  }


# ローカル確認用
if __name__ == '__main__':
  print(faq_qa({'queryStringParameters': {'query': 'メールアドレスを変更したい'}}, None))
