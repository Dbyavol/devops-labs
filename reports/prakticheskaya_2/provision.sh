#!/bin/bash

VAGRANT_HOST_DIR=/mnt/host_machine

# Jenkins & Java
echo "Installing Java and Jenkins"
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null 2>&1
sudo apt-get update > /dev/null 2>&1
sudo apt-get -y install fontconfig openjdk-17-jre > /dev/null 2>&1
sudo apt-get -y install jenkins > /dev/null 2>&1

echo "Starting Jenkins service"
sudo systemctl enable jenkins
sudo systemctl start jenkins
sleep 1m

echo "Installing Jenkins plugins"
JENKINSPWD=$(sudo cat /var/lib/jenkins/secrets/initialAdminPassword)
sudo rm -f jenkins_cli.jar.*
wget -q http://localhost:8080/jnlpJars/jenkins-cli.jar
IFS=$'\n'
for line in $(cat $VAGRANT_HOST_DIR/jenkins-plugins.txt)
do
  if [[ "$line" ]]; then
    java -jar ./jenkins-cli.jar -auth admin:"$JENKINSPWD" -s http://localhost:8080 install-plugin "$line"
	sleep 1
  fi
done

echo "Restarting Jenkins"
java -jar ./jenkins-cli.jar -auth admin:"$JENKINSPWD" -s http://localhost:8080 safe-restart

echo "Setting up Jenkins admin user"
sudo mkdir -p /var/lib/jenkins/init.groovy.d
sudo cp -f $VAGRANT_HOST_DIR/createAdminUser.groovy /var/lib/jenkins/init.groovy.d/
sudo cp -f $VAGRANT_HOST_DIR/disable-plugin-install-wizard.groovy /var/lib/jenkins/init.groovy.d/
sudo chown -R jenkins:jenkins /var/lib/jenkins/init.groovy.d

echo "Restarting Jenkins service"
sudo systemctl restart jenkins
sleep 1m
sudo rm -rf /var/lib/jenkins/init.groovy.d
