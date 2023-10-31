�yEC2 Instance Connect�z
1. VPC���G���h�|�C���g���G���h�|�C���g���쐬
���O�^�O�FEIC-ENDPOINT
�T�[�r�X�J�e�S���FEC2�C���X�^���X�ڑ��G���h�|�C���g
VPC�FCC-VPC
�Z�L�����e�B�O���[�v�FEIC
�T�u�l�b�g�FCC-PUBLIC-SUBNET-A

2. �R���\�[������ڑ�
EC2���C���X�^���X��CC-EC2-REDMINE���ڑ���EC2 Instance Connect�G���h�|�C���g���g�p���Đڑ�����
���[�U�[���Fec2-user
EC2 Instance Connect�G���h�|�C���g�FEIC-ENDPOINT

3. �R�}���h�v�����v�g����ڑ�
aws ec2-instance-connect ssh --instance-id ���C���X�^���XID --connection-type eice

�ydocker�Z�b�g�A�b�v�z
1. docker�̃C���X�g�[��
sudo yum update -y
sudo yum -y install docker
sudo systemctl start docker
sudo systemctl enable docker
docker --version

2. docker-compose�̃C���X�g�[��
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
sudo ln -s /usr/local/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose
docker-compose --version

�y���ރA�b�v���[�h�z
1. �R�}���h�v�����v�g������s
aws s3 mb s3://zukosha-setup
aws s3 cp ./upload s3://zukosha-setup --recursive

�y���ރ_�E�����[�h�z
1. EC2�Ŏ��s
aws s3 cp s3://zukosha-setup . --recursive

�yRedmine�R���e�i�N���z
��DockerHub�̃A�J�E���g�����O�Ɏ擾���Ă�������
1. �C���[�W�쐬����уR���e�i�N��
./setup.sh

2. �z�X�g���Redmine�ւ̐ڑ����m�F����B
curl http://localhost/

3. WEB�R���e�i�փ��O�C������
sudo docker exec -it con_web /bin/bash

4. �R���e�i���Redmine�ւ̐ڑ����m�F����B
curl http://localhost:3000/
exit

5. DB�R���e�i�փ��O�C������
sudo docker exec -it con_db /bin/bash

6. MySQL�N���ƕ����R�[�h���m�F����
mysql -uroot -pexample
show create database redmine;
exit

�y�g���u���V���[�e�B���O�z
���R���e�i�ւ̃t�@�C���R�s�[
sudo docker cp mail_renkei.sh con_web:/usr/src/redmine/mail_renkei.sh
sudo docker cp CON1:/var/spool/cron/crontabs/root /home/ec2-user/download/root

���R���e�i��~
sudo docker-compose down
�����R���e�i����~����Ȃ��ꍇ
�@sudo docker ps
�@sudo docker rm -f [CONTAINER ID]

���R���e�i��~���C���[�W�폜
sudo docker-compose down --rmi all
�����C���[�W���폜����Ȃ��ꍇ
�@sudo docker images
�@sudo docker rmi -f [IMAGE ID]

�����g�p�C���[�W�폜
sudo docker system prune -a --volumes
sudo docker system df

���z�[���f�B���N�g���̃f�[�^�폜
cd $HOME
sudo rm -r *