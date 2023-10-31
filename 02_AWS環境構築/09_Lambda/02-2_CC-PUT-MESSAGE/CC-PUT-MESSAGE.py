import json
import boto3
import requests

def lambda_handler(event, context):
    try:
        # S3のオブジェクトURLを取得する
        object_url = 'https://' + event['Records'][0]['s3']['bucket']['name'] + '.s3.' + event['Records'][0]['awsRegion'] + '.amazonaws.com/' + event['Records'][0]['s3']['object']['key']
        print(context.function_name, 'debug:', 'object_url = ', object_url)
        
        # コンタクトIDを取得する
        object_key = event['Records'][0]['s3']['object']['key']
        print(context.function_name, 'debug:', 'object_key = ', object_key)
        start = object_key.rfind('/') + 1
        end = object_key.find('_')
        contact_id = object_key[start:end]
        print(context.function_name, 'debug:', 'contact_id = ', contact_id)
        
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
                'notes': '【録音メッセージ】' + '\n' + object_url
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