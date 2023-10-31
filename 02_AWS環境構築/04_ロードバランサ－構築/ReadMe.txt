【ターゲットグループ】
EC2＞ターゲットグループ＞ターゲットグループの作成
ターゲットタイプの選択：インスタンス
ターゲットグループ名：CC-TARGET-REDMINE
プロトコル：HTTP
ポート：80
VPC：CC-VPC
保留中として以下を含める：CC-EC2-REDMINE

【ロードバランサ－】
EC2＞ロードバランサ－＞ロードバランサ－の作成
ロードバランサータイプ：Application Load Balancer
ロードバランサー名：CC-ALB-REDMINE
スキーム：インターネット向け
VPC：CC-VPC
マッピング：CC-PUBLIC-SUBNET-A, CC-PUBLIC-SUBNET-C
セキュリティグループ：ALB
リスナー：HTTP/80/CC-TARGET-REDMINE

【自己署名証明書】
1. EC2上で実行
openssl genrsa -out private.key
openssl req -new -key private.key -out server.csr
  ※「Common Name」にALBのDNS名を入力する。それ以外は空欄でOK。
openssl x509 -req -days 365 -in server.csr -signkey private.key -out server.crt

【ACMへの証明書インポート】
AWS Certificate Manager＞証明書＞証明書をインポート
証明書本文：※「server.crt」の内容を張り付ける
証明書のプライベートキー：※「private.key」の内容を張り付ける

【ロードバランサ－のHTTPS化】
EC2＞ロードバランサ－＞CC-ALB-REDMINE＞HTTP:80リスナー＞リスナーの編集
プロトコル：HTTPS
ポート：443
Certificate：自己証明書

※ターゲットグループのヘルスチェックが成功することを確認