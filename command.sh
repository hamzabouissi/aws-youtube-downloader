docker run --name es01 --net elastic -p 9200:9200 -p 9300:9300 -e "http.publish_host=35.171.163.235" -e "http.host=0.0.0.0" \
    -it docker.elastic.co/elasticsearch/elasticsearch:8.4.1

docker exec -it es02 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
