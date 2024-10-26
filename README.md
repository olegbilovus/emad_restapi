# RestAPI for the EMAD course.

It includes:

- A docker image
- A CI to build and push the image on ghrc
- IaC with OpenTofu for Azure to build and run the infrastructure

## How to run the infrastructure in local

Install Git and Docker

Copy and paste the following commands in your terminal.

You may need to press enter to run the commands and press again enter to run the `docker compose up` command.

**Wait till the container *mongodb_setup* exits.**

```bash
git clone https://github.com/olegbilovus/minio_pictograms.git
git clone https://github.com/olegbilovus/emad_restapi.git
git clone https://github.com/olegbilovus/emad_images.git
cd minio_pictograms
docker build -t minio_pictograms .
cd ../emad_images
docker build -t emad_images .
cd ../emad_restapi
docker build -t emad_restapi .
docker compose up
```
