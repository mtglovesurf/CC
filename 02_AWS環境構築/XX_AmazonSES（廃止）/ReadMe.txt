※ ガイドライン
https://docs.aws.amazon.com/ses/latest/dg/receiving-email.html

1. ドメインを取得する
Route53＞ドメインの登録＞ドメインの検索＞チェックアウト＞管理者情報を入力
Route53＞リクエスト＞ステータスが「成功」になっていることを確認（※時間がかかるので翌日確認）

2. ドメイン検証（DKIM設定）
Amazon SES＞検証済みID＞IDの作成＞ドメイン＞IDの作成
ドメイン：「zukosha-it.com」
※DKIMが有効化されDKIM用のCNAMEレコードがドメインに登録される
※Route53＞ホストゾーン＞DKIM用のCNAMEレコードが登録されていること

3. MXレコード登録
Route53＞ホストゾーン＞zukosha-it.com＞レコードを作成
レコード名：zukosha-it.com（※サブドメイン空欄）
レコードタイプ：MX
値：10 inbound-smtp.ap-northeast-1.amazonaws.com
※東京リージョンのメール受信エンドポイント
参考：https://docs.aws.amazon.com/ja_jp/general/latest/gr/ses.html

5. バケット作成
S3＞バケット作成＞amazon-ses-zukosha
バケットポリシーに以下を入力
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowSESPuts",
            "Effect": "Allow",
            "Principal": {
                "Service": "ses.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::amazon-ses-zukosha/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:ses:ap-northeast-1:309956249298:receipt-rule-set/CC-RECEIVE-MAIL-RULESET:receipt-rule/CC-RECEIVE-MAIL-RULE1",
                    "AWS:SourceAccount": "309956249298"
                }
            }
        }
    ]
}

6. 受信ルールセット作成
Amazon SES＞Eメール受信＞受信ルールセット＞ルールセットの作成
ルールセット名：CC-RECEIVE-MAIL-RULESET

7. 受信ルール作成
Amazon SES＞Eメール受信＞CC-RECEIVE-MAIL-RULE＞ルールの作成
ルール名：CC-RECEIVE-MAIL-RULE1
スパムとウイルススキャン：有効化
新しい受信者条件の追加：support@zukosha-it.com
アクションの追加：Amazon S3バケットに配信
S3バケット；amazon-ses-zukosha

8. 受信ルールセット有効化
Amazon SES＞Eメール受信＞CC-RECEIVE-MAIL-RULESET＞有効として設定



