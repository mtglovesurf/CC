import json
import boto3
import requests

# Amazon Connectのコンタクトフローから呼び出されるメイン処理
def lambda_handler(event, context):
    try:
        # コンタクト情報を取得する
        contact_id = event['Details']['ContactData']['ContactId']
        phone_number = event['Details']['ContactData']['CustomerEndpoint']['Address']
        print(context.function_name, 'debug:', '保存するcontact_id = ', contact_id)
        print(context.function_name, 'debug:', '保存するphone_number = ', phone_number)
        
        # チケット内容作成
        subject = f'インシデント（コンタクトID：{contact_id}）'
        description = 'コールセンターシステムにより自動作成されました。'

        # RedmineのRestful APIとAPIアクセスキーを取得する
        params = get_ssm_params('/redmine/api/url','/redmine/api/key')
        api_url = 'http://' + params['/redmine/api/url'] + '/issues.json'
        api_key = params['/redmine/api/key']

        # ヘッダー情報
        headers = {
            'Content-Type': 'application/json',
            'X-Redmine-API-Key': api_key
        }           
        
        # チケット情報
        ticket = {
            'issue': {
                'project_id': 'support',
                'subject': subject,
                'description': description,
                'custom_field_values': {
                    "2": phone_number
                }
            }
        }        
        
        # リクエスト送信
        response = requests.post(api_url, data=json.dumps(ticket), headers=headers)
        print(context.function_name, 'debug:', 'status_code = ', response.status_code)
        response_json = response.json()
        print(context.function_name, 'debug:', 'ticket_id = ', response_json['issue']['id'])
        
        # DyanmoDBに保存
        item = {
            'contact_id': contact_id,
            'phone_number': phone_number,
            'ticket_id': response_json['issue']['id']
        }
        db = boto3.resource('dynamodb')
        db_table = db.Table('CONTACT')
        db_table.put_item(Item=item)

        # 保存確認
        response = db_table.get_item(Key={'contact_id':contact_id}, ConsistentRead=True)
        db_item = response['Item']
        print(context.function_name, 'debug:', '保存されたアイテム = ', db_item)
        
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
        print(get_ssm_params.__name__, 'debug:', keys)
        response = ssm.get_parameters(
            Names=keys,
            WithDecryption=True,
        )
        
        for p in response['Parameters']:
            result[p['Name']] = p['Value']
        print(result)
        return result
    except Exception as e:
        print(get_ssm_params.__name__, 'exception:', e)
    finally:
        print(get_ssm_params.__name__, 'finished.')