【管理者ガイド】
https://docs.aws.amazon.com/ja_jp/workmail/latest/adminguide/what_is.html

【メールドメイン取得】
1. Route53＞ドメインの登録＞ドメインの検索＞zukosha-it.com＞チェックアウト＞管理者情報を入力
2. Route53＞リクエスト＞ステータスが「成功」になっていることを確認（※時間がかかるため翌日確認）
3. 管理者宛の確認メールのURLをクリックして登録情報の認証を完了させる
　 ※15日以内に認証しないとドメインが停止されてしまうので注意！！
4. DNS疎通確認
　 nslookup -type=NS zukosha-it.com
　 ※NSレコードが表示される

【組織の作成】
1. リージョン＞バージニア北部
2. Amazon WorkMail＞Organization＞Create organization
Email domain：「Existing Route 53 domain」
Route 53 hosted zone：「zukosha-it.com」
Alias：「zukosha-it」

【ドメインの検証】
Amazon WorkMail＞Organization＞zukosha-it＞Domains＞「zukosha-it.com」＞
「Update all in Route 53」を実行する。

【ユーザーの作成】
Amazon WorkMail＞Organizations＞zukosha-it＞Users＞Create User
User name：「support」
Display name：「サポート」
Email address：「support@zukosha-it.com」
Password：「Zks0155332200」
Repeat password：「Zks0155332200」

【メールフォルダ作成】
1. webメールにログインする。
https://zukosha-it.awsapps.com/mail
2. My Mail＞New folderから以下のメールボックスを作成する。
・「redmine_success」
・「redmine_failure」

【メール送信テスト】
1. 「support@zukosha-it.com」宛に添付ファイル付きのメールを送信する
2. webメールにログインする
https://zukosha-it.awsapps.com/mail
3. メールが受信できていることを確認する

