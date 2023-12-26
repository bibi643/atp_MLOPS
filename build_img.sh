echo "Image constructor"

cd /src/data_generation
docker image build . -t data_collection_image:latest
cd ../src/training
docker image build . -t model_training_image:latest
cd ../src/app
docker image build . -t api_image:latest