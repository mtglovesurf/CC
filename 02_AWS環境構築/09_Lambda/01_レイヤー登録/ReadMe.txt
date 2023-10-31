【Redmineサーバログイン】
aws ec2-instance-connect ssh --instance-id i-057cbf09ed730c8d5 --connection-type eice

【requests/boto3ライブラリ取得】
mkdir python
sudo yum -y install pip
pip3 install -t ./python requests
pip3 install -t ./python boto3
zip -r layer.zip ./python 

【レイヤー作成】
aws lambda publish-layer-version --layer-name CC-PYTHON-LAMBDA-LAYER --license-info "MIT" --zip-file fileb://layer.zip --compatible-runtimes python3.10 python3.11 --compatible-architectures "arm64" "x86_64"
