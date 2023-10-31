【ポリシー作成】
aws iam create-policy --policy-name CC-PUT-CONTACT-POLICY --policy-document file://CC-PUT-CONTACT-POLICY.json

【ポリシー更新（※変更時）】
aws iam create-policy-version --policy-arn arn:aws:iam::309956249298:policy/CC-PUT-CONTACT-POLICY --policy-document file://CC-PUT-CONTACT-POLICY.json --set-as-default

【ロール作成】
aws iam create-role --role-name CC-PUT-CONTACT-ROLE --assume-role-policy-document file://CC-PUT-CONTACT-ROLE.json

【ロールにポリシーをアタッチ】
aws iam attach-role-policy --role-name CC-PUT-CONTACT-ROLE --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name CC-PUT-CONTACT-ROLE --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
aws iam attach-role-policy --role-name CC-PUT-CONTACT-ROLE --policy-arn arn:aws:iam::309956249298:policy/CC-PUT-CONTACT-POLICY

【関数登録】
aws lambda create-function --function-name CC-PUT-CONTACT --zip-file fileb://CC-PUT-CONTACT.zip --handler CC-PUT-CONTACT.lambda_handler --runtime python3.10 --role arn:aws:iam::309956249298:role/CC-PUT-CONTACT-ROLE

【レイヤー設定】
aws lambda update-function-configuration --function-name CC-PUT-CONTACT --layers "arn:aws:lambda:ap-northeast-1:309956249298:layer:CC-PYTHON-LAMBDA-LAYER:1"

【リソースベースのポリシー付与（connectインスタンス）】
aws lambda add-permission --function-name CC-PUT-CONTACT --action lambda:InvokeFunction --statement-id CC-PUT-CONTACT-PERMISSION --principal connect.amazonaws.com --source-arn arn:aws:connect:ap-northeast-1:309956249298:instance/866d554f-31fb-4c23-ba12-b348db2bd0ee

【コンソールから設定】
Lambda＞関数＞CC-CC-PUT-CONTACT＞設定＞一般設定＞編集
タイムアウト：30秒
↓ｓ
Lambda＞関数＞CC-CC-PUT-CONTACT＞設定＞VPC＞編集
VPC：CC-DEV-VPC
サブネット：CC-DEV-PRIVATE-SUBNET-A2, CC-DEV-PRIVATE-SUBNET-B2
セキュリティグループ：Lambda