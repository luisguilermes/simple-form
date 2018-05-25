#!/usr/bin/env bash

response=$(curl --write-out %{http_code} --silent --output /dev/null http://application:9090/v1/sugestoes)
echo $response