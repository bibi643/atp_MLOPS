# ATP_MLOPS
MLops project with DataScientest based on ATP matches.


#Dockerisation

-Image api:

Using the terminal go to folder api and run:
docker image build . -t api_image:latest

-Data collection image

Using the terminal, go to the folder Data_collection and run:
docker image build . -t data_collection_image:latest


-Model training image

Using the terminal, go to the folder Model_training folder and run:
docker image build . -t model_training_image:latest




-Docker compose run

go to the folder codes where you can se the following folders: api, data_collection, File_Data_volume, docker-compose....etc
run

docker-compse up


in the browzer open localhost:8000/docs 


you can see the api.

when you finished you can run the next line in the terminal.

docker-compose down 


