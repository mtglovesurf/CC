【Redmineセットアップ】
1. adminでログインして初期パスワードを変更する
https://cc-dev-elb-1341769929.ap-northeast-1.elb.amazonaws.com/login
アカウント：admin
初期パスワード：admin
変更後パスワード：Zks0155332200

2. APIの有効化
管理＞設定＞API
「RESTによるWebサービスを有効にする」にチェックを付ける

3. API連携用のロールを作成する
管理＞ロールと権限＞新しいロール
名称：APIロール
権限（チケットトラッキング）：チケットの閲覧、チケットの追加、チケットの編集、コメントの追加
チケットトラッキング：「すべてのトラッカー」すべてにチェックをつける

4. APIユーザーを追加する
管理＞ユーザー＞新しいユーザー
ログインID：api-user
名：API
性：ユーザー
メールアドレス：api-user@example.net
言語：Japanese（日本語）
パスワード：password

5. プロジェクトを追加する
管理＞プロジェクト＞新しいプロジェクト
プロジェクト名：問い合せ管理
プロジェクト識別子：support
公開：チェックを外す
モジュール：チケットトラッキング、ファイル、wiki

6. APIユーザーをプロジェクトに追加する
管理＞プロジェクト＞「問い合せ管理」＞メンバー＞新しいメンバー
「APIユーザー」を選択し、「APIロール」のロールで登録する。

7. チケットのステータスを登録する
管理＞チケットのステータス＞新しいステータス
・新規
・進行中
・解決
・差し戻し
・終了（「終了したチケット」にチェック）
・却下（「終了したチケット」にチェック）

8. チケットの優先度を登録する
管理＞選択肢の値＞新しい値
・通常（「有効」「デフォルト値」にチェック）
・緊急（「有効」にチェック）

9. トラッカーを作成する
名称：「問い合せ」
デフォルトのステータス：「新規」
プロジェクト：「問い合せ管理」にチェック

10. カスタムフィールドを作成する
管理＞カスタムフィールド＞新しいカスタムフィールド＞チケット＞顧客電話番号
管理＞カスタムフィールド＞新しいカスタムフィールド＞チケット＞顧客名

【APIアクセスキーのパラメータストア登録】
1. APIアクセスキーの確認
Redmineサイト＞api-userでログイン＞個人設定＞APIアクセスキー＞表示
2. APIアクセスキーの登録
aws ssm put-parameter --type String --name "/redmine/api/key" --value "※APIアクセスキー" --overwrite

【サーバーIPのパラメータストア登録】
1. RedmineサーバーのIP確認
aws ec2-instance-connect ssh --instance-id ※インスタンスID --connection-type eice
ifconfig
2. RedminサーバーのIP登録
aws ssm put-parameter --type String --name "/redmine/api/url" --value "※RedmineサーバーのIP" --overwrite

【API連携テスト】
1. Redmineサーバーにログイン
aws ec2-instance-connect ssh --instance-id ※インスタンスID --connection-type eice

2. チケット登録テスト
vi issue-test.json
{
    "issue": {
        "project_id": "support",
        "subject": "test1",
        "description": "new-ticket"
    }
}
curl -X POST -H "Content-Type: application/json" -H "X-Redmine-API-Key: ※APIアクセスキー" -d @issue-test.json http://※RedmineサーバーのIP/issues.json
※チケットが発行されていることを確認する

3. チケット更新テスト
vi update-test.json
{
    "issue": {
        "notes": "update-ticket"
    }
}
curl -X PUT -H "Content-Type: application/json" -H "X-Redmine-API-Key: ※APIアクセスキー" -d @update-test.json http://※RedmineサーバーのIP/issues/※チケット番号.json
※チケットが更新されていることを確認する

【メール連携テスト】
1. Redmineコンテナにログイン
aws ec2-instance-connect ssh --instance-id ※インスタンスID --connection-type eice
sudo docker exec -it con_web /bin/bash

2. cronを有効にし、メール連携ジョブを登録する。
service cron start
crontab -e
--------------------------------------------------------------------------------------------------
SHELL=/bin/sh
BUNDLE_APP_CONFIG=/usr/local/bundle
GEM_HOME=/usr/local/bundle
PATH=/usr/local/bundle/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
* *	* * *	/usr/src/redmine/mail_renkei.sh >> /usr/src/redmine/log/mail_renkei.log 2>&1
--------------------------------------------------------------------------------------------------

3. support@zukosha-it.comにメールを送る
※１分後にチケットが発行されていることを確認する

