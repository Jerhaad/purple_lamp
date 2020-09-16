set +x
docker build -t purple --network host .
docker tag purple:latest purple:local 
