【ポリシー作成】
aws iam create-policy --policy-name CC-PUT-TRANSCRIPT-POLICY --policy-document file://CC-PUT-TRANSCRIPT-POLICY.json

【ポリシー更新（※変更時）】
aws iam create-policy-version --policy-arn arn:aws:iam::309956249298:policy/CC-PUT-TRANSCRIPT-POLICY --policy-document file://CC-PUT-TRANSCRIPT-POLICY.json --set-as-default

【ロール作成】
aws iam create-role --role-name CC-PUT-TRANSCRIPT-ROLE --assume-role-policy-document file://CC-PUT-TRANSCRIPT-ROLE.json

【ロールにポリシーをアタッチ】
aws iam attach-role-policy --role-name CC-PUT-TRANSCRIPT-ROLE --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name CC-PUT-TRANSCRIPT-ROLE --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
aws iam attach-role-policy --role-name CC-PUT-TRANSCRIPT-ROLE --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam attach-role-policy --role-name CC-PUT-TRANSCRIPT-ROLE --policy-arn arn:aws:iam::309956249298:policy/CC-PUT-TRANSCRIPT-POLICY

【関数登録】
aws lambda create-function --function-name CC-PUT-TRANSCRIPT --zip-file fileb://CC-PUT-TRANSCRIPT.zip --handler CC-PUT-TRANSCRIPT.lambda_handler --runtime python3.10 --role arn:aws:iam::309956249298:role/CC-PUT-TRANSCRIPT-ROLE

【レイヤー設定】
aws lambda update-function-configuration --function-name CC-PUT-TRANSCRIPT --layers "arn:aws:lambda:ap-northeast-1:309956249298:layer:CC-PYTHON-LAMBDA-LAYER:1"

【コンソールから設定】
Lambda＞関数＞CC-PUT-TRANSCRIPT＞トリガーを追加
ソース：S3
Bucket：arn:aws:s3:::amazon-connect-92d7de397f7e
Suffix：.json
↓
Lambda＞関数＞CC-CC-PUT-TRANSCRIPT＞設定＞一般設定＞編集
タイムアウト：30秒
↓
Lambda＞関数＞CC-CC-PUT-TRANSCRIPT＞設定＞VPC＞編集
VPC：CC-DEV-VPC
サブネット：CC-DEV-PRIVATE-SUBNET-A2, CC-DEV-PRIVATE-SUBNET-B2
セキュリティグループ：Lambda
