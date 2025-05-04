#!/usr/bin/env bash
cd /root/GPSA
git pull origin main
systemctl restart gpsa
