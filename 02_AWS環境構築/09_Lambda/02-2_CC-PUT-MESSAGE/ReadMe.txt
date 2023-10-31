【ポリシー作成】
aws iam create-policy --policy-name CC-PUT-MESSAGE-POLICY --policy-document file://CC-PUT-MESSAGE-POLICY.json

【ポリシー更新（※変更時）】
aws iam create-policy-version --policy-arn arn:aws:iam::309956249298:policy/CC-PUT-MESSAGE-POLICY --policy-document file://CC-PUT-MESSAGE-POLICY.json --set-as-default

【ロール作成】
aws iam create-role --role-name CC-PUT-MESSAGE-ROLE --assume-role-policy-document file://CC-PUT-MESSAGE-ROLE.json

【ロールにポリシーをアタッチ】
aws iam attach-role-policy --role-name CC-PUT-MESSAGE-ROLE --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name CC-PUT-MESSAGE-ROLE --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
aws iam attach-role-policy --role-name CC-PUT-MESSAGE-ROLE --policy-arn arn:aws:iam::309956249298:policy/CC-PUT-MESSAGE-POLICY

【関数登録】
aws lambda create-function --function-name CC-PUT-MESSAGE --zip-file fileb://CC-PUT-MESSAGE.zip --handler CC-PUT-MESSAGE.lambda_handler --runtime python3.10 --role arn:aws:iam::309956249298:role/CC-PUT-MESSAGE-ROLE

【レイヤー設定】
aws lambda update-function-configuration --function-name CC-PUT-MESSAGE --layers "arn:aws:lambda:ap-northeast-1:309956249298:layer:CC-PYTHON-LAMBDA-LAYER:1"

【コンソールから設定】
Lambda＞関数＞CC-PUT-MESSAGE＞トリガーを追加
ソース：S3
Bucket：arn:aws:s3:::amazon-connect-92d7de397f7e
Suffix：.wav
↓
Lambda＞関数＞CC-CC-PUT-MESSAGE＞設定＞一般設定＞編集
タイムアウトを30秒に変更
↓
Lambda＞関数＞CC-CC-PUT-MESSAGE＞設定＞VPC＞編集
VPC：CC-DEV-VPC
サブネット：CC-DEV-PRIVATE-SUBNET-A2, CC-DEV-PRIVATE-SUBNET-B2
セキュリティグループ：Lambda
