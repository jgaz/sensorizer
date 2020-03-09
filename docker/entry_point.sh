#!/bin/bash
printenv | ../deploy/create_environment.py >> /root/.profile
chmod 600 /root/.profile
supervisord -n
