# Jenkisns安装

> 下面针对的是ubuntu的安装

## LTS Release
> LTS (Long-Term Support) releases are chosen every 12 weeks from the stream of regular releases as the stable release for that time period.

- add the key:```wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -```
- add  entry in your /etc/apt/sources.list: ```deb https://pkg.jenkins.io/debian-stable binary/```
- Update  local package index, then  install Jenkins:
```
sudo apt-get update
sudo apt-get install jenkins
```

## Weekly Release
> A new release is produced weekly to deliver bug fixes and features to users and plugin developers.

- add the key:```wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -```
- add  entry in your /etc/apt/sources.list: ```deb https://pkg.jenkins.io/debian binary/```
- Update  local package index, then  install Jenkins:
```
sudo apt-get update
sudo apt-get install jenkins
```
