import json
import boto3
import requests

def lambda_handler(event, context):
    try:
        # JSONファイルからコンタクトIDと文字起こし結果を取得する
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        response = bucket.Object(object_key).get()
        body = response['Body'].read()
        json_body = json.loads(body)
        contact_id = json_body['CustomerMetadata']['ContactId']
        transcript = ''
        for Items in json_body['Transcript']:
            transcript = transcript + Items['ParticipantId'] + ':' + '\n' + Items['Content'] + '\n'
        print(context.function_name, 'debug:', 'contact_id = ', contact_id)
        print(context.function_name, 'debug:', 'transcript = ', transcript)
        
        # チケットIDを取得する
        db = boto3.resource('dynamodb')
        db_table = db.Table('CONTACT')
        response = db_table.get_item(Key={'contact_id':contact_id}, ConsistentRead=True)
        db_item = response['Item']
        print(context.function_name, 'debug:', 'db_item = ', db_item)
        ticket_id = str(db_item['ticket_id'])
        
        # RedmineのRestful APIとAPIアクセスキーを取得する
        params = get_ssm_params('/redmine/api/url','/redmine/api/key')
        api_url = 'http://' + params['/redmine/api/url'] + '/issues/' + ticket_id + '.json'
        api_key = params['/redmine/api/key']
        
        # リクエストヘッダー
        headers = {
            'Content-Type': 'application/json',
            'X-Redmine-API-Key': api_key
        }
        
        # コメントにオブジェクトURLを追加する
        ticket = {
            'issue': {
                'notes': '【文字起こし結果】' + '\n' + transcript
            }
        }
        print(context.function_name, 'debug:', 'ticket = ', ticket)
        
        # リクエスト送信
        response = requests.put(api_url, data=json.dumps(ticket), headers=headers)
        print(context.function_name, 'debug:', 'statusCode = ', response.status_code)
        print(context.function_name, 'debug:', 'body = ', response.text)
        
        return {'statusCode': 200, 'body': 'OK'}
    except Exception as e:
        print(context.function_name, 'exception:', e)
        return {'statusCode': -1, 'body': e}
    finally:
        print(context.function_name, 'finished.')
        
# パラメータストアから複数キーを取得する
def get_ssm_params(*keys, region='ap-northeast-1'):
    try:
        result = {}
        ssm = boto3.client('ssm', region)
        #print(get_ssm_params.__name__, 'debug:', keys)
        response = ssm.get_parameters(
            Names=keys,
            WithDecryption=True,
        )
        
        for p in response['Parameters']:
            result[p['Name']] = p['Value']
        #print(result)
        return result
    except Exception as e:
        print(get_ssm_params.__name__, 'exception:', e)
    finally:
        print(get_ssm_params.__name__, 'finished.')