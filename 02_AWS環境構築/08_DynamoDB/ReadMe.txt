【事前準備】
・作業端末にAWSのCLIをインストールしてください
・作業端末にAWSユーザー（管理者または開発者）のCLIアクセスキーを設定してください
・作業端末に各jsonファイルをコピーしてください

【テーブル作成】
aws dynamodb create-table --cli-input-json file://CONTACT.json
aws dynamodb describe-table --table-name CONTACT

【アイテム追加テスト】
aws dynamodb put-item --cli-input-json file://CONTACT_put_item.json
aws dynamodb get-item --cli-input-json file://CONTACT_get_item.json
aws dynamodb delete-item --cli-input-json file://CONTACT_get_item.json
aws dynamodb scan --table-name CONTACT

【テーブル削除】
aws dynamodb delete-table --table-name CONTACT
