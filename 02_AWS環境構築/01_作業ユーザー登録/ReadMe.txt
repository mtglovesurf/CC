【ユーザー作成】
1. IAM＞ユーザー＞ユーザーの作成
ユーザー名：zukosha-admin
許可のオプション：ユーザーをグループに追加
ユーザーグループ：admin

2. IAM＞ユーザー＞zukosha-admin＞セキュリティ認証情報＞コンソールのサインイン
コンソールアクセスを有効にする
有効化
自動生成されたパスワード
適用
.csvファイルをダウンロード

3. IAM＞ユーザー＞zukosha-admin＞セキュリティ認証情報＞多要素認証（MFA）
MFAデバイスの割り当て
デバイス名：※以下4つ分をそれぞれ登録する
　　　　　　Zukohsa-IT-1
　　　　　　Zukohsa-IT-2
　　　　　　Zukohsa-IT-3
　　　　　　Zukohsa-IT-4
MFAデバイス：Security Key
ユビキーを挿入する
セキュリティキー暗証番号（PIN）：0155-33-2200

4. IAM＞ユーザー＞zukosha-admin＞セキュリティ認証情報＞アクセスキー
アクセスキーを作成
ユースケース：コマンドラインインタフェース（CLI）
.csvファイルをダウンロード

【AWS CLI（ローカルの作業環境）】
1. AWS CLIをインストールする
https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html

2. アクセスキーを設定する
aws configure
　AWS Access Key ID：※アクセスキーCSV参照
　AWS Secret Access Key：※アクセスキーCSV参照
　Default region name：ap-northeast-1
　Default output format：json
aws configure list
aws sts get-caller-identity