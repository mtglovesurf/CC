【EC2 Instance Connect】
1. VPC＞エンドポイント＞エンドポイントを作成
名前タグ：EIC-ENDPOINT
サービスカテゴリ：EC2インスタンス接続エンドポイント
VPC：CC-VPC
セキュリティグループ：EIC
サブネット：CC-PUBLIC-SUBNET-A

2. コンソールから接続
EC2＞インスタンス＞CC-EC2-REDMINE＞接続＞EC2 Instance Connectエンドポイントを使用して接続する
ユーザー名：ec2-user
EC2 Instance Connectエンドポイント：EIC-ENDPOINT

3. コマンドプロンプトから接続
aws ec2-instance-connect ssh --instance-id ※インスタンスID --connection-type eice

【dockerセットアップ】
1. dockerのインストール
sudo yum update -y
sudo yum -y install docker
sudo systemctl start docker
sudo systemctl enable docker
docker --version

2. docker-composeのインストール
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
sudo ln -s /usr/local/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose
docker-compose --version

【資材アップロード】
1. コマンドプロンプトから実行
aws s3 mb s3://zukosha-setup
aws s3 cp ./upload s3://zukosha-setup --recursive

【資材ダウンロード】
1. EC2で実行
aws s3 cp s3://zukosha-setup . --recursive

【Redmineコンテナ起動】
※DockerHubのアカウントを事前に取得してください
1. イメージ作成およびコンテナ起動
./setup.sh

2. ホスト上でRedmineへの接続を確認する。
curl http://localhost/

3. WEBコンテナへログインする
sudo docker exec -it con_web /bin/bash

4. コンテナ上でRedmineへの接続を確認する。
curl http://localhost:3000/
exit

5. DBコンテナへログインする
sudo docker exec -it con_db /bin/bash

6. MySQL起動と文字コードを確認する
mysql -uroot -pexample
show create database redmine;
exit

【トラブルシューティング】
★コンテナへのファイルコピー
sudo docker cp mail_renkei.sh con_web:/usr/src/redmine/mail_renkei.sh
sudo docker cp CON1:/var/spool/cron/crontabs/root /home/ec2-user/download/root

★コンテナ停止
sudo docker-compose down
∟※コンテナが停止されない場合
　sudo docker ps
　sudo docker rm -f [CONTAINER ID]

★コンテナ停止＆イメージ削除
sudo docker-compose down --rmi all
∟※イメージが削除されない場合
　sudo docker images
　sudo docker rmi -f [IMAGE ID]

★未使用イメージ削除
sudo docker system prune -a --volumes
sudo docker system df

★ホームディレクトリのデータ削除
cd $HOME
sudo rm -r *