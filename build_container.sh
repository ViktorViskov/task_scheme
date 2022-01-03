if [ "$1" ]
then
    echo "Delete old image and container"
    # delete exist image and container
    docker container stop task_scheme_container
    docker container rm task_scheme_container
    docker image rm task_scheme_image
fi
echo "Create new containers"
# build new image and run app
docker build -t task_scheme_image .
docker run -dit -p 9003:9003 --name task_scheme_container task_scheme_image
