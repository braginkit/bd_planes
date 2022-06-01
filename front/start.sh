#!/bin/bash
app="front"
docker build -t ${app} .
docker run -d -p 0.0.0.0:56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}\


