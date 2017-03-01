#!/bin/sh

DEFAULT_SAVE_DIR='.'

host=$1
saveDir=${2:-$DEFAULT_SAVE_DIR}

mkdir -p $saveDir

caKeyPath="$saveDir"/ca.key
caCerPath="$saveDir"/ca.cer
serverKeyPath="$saveDir"/server.key
serverReqPath="$saveDir"/server.req
serverSerialPath="$saveDir"/server.serial
serverCerPath="$saveDir"/server.cer
serverHostPath="$saveDir"/host

# 根证书制作

## 创建制作根证书的私钥文件
openssl genrsa -out $caKeyPath 2048

## 创建根证书
openssl req -x509 -new -key $caKeyPath -out $caCerPath -days 730 -subj /CN="AppServer Custom $host"

# 创建自签名SSL证书

## 创建私钥 
openssl genrsa -out $serverKeyPath 2048

## 创建CSR
openssl req -new -out $serverReqPath -key $serverKeyPath -subj /CN=$host

# 用CSR去创建SSL证书
openssl x509 -req -in $serverReqPath -out $serverCerPath -CAkey $caKeyPath -CA $caCerPath -days 730 -CAcreateserial -CAserial $serverSerialPath
