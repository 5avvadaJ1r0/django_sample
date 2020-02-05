#!/bin/zsh


mysql_container_id=`docker ps|grep mysql|cut -d ' ' -f1|sort|uniq`

if -z mysql_container_id; then
  docker stop $(docker ps -q)
else
  docker stop $(docker ps -q|grep -v ${mysql_container_id})
fi

mysql_container_id=`docker ps -a|grep mysql|cut -d ' ' -f1|sort|uniq`

if -z mysql_container_id; then
  docker rm $(docker ps -q -a)
else
 docker rm $(docker ps -q -a|grep -v ${mysql_container_id})
fi

mysql_image_id=`docker images|grep mysql|cut -b 41-51|sort|uniq`

if -z mysql_image_id; then
  docker rmi $(docker images -q)
else
 docker rmi $(docker images -q|grep -v ${mysql_image_id})
fi

docker-compose up
