
PROJECT_ID = 
TOPIC_ID = 
SUBSCRIPTION_ID = 

CLOUD_RUN_REGION = us-central1
CERTS_FOLDER = $PWD/cert
CERTS_MOUNT = /cert
CERTS_FILE =  /cert/credentials.json

protos:
	python -m grpc_tools.protoc -I. --python_out=protocol/ event.proto

topic:
	gcloud pubsub topics create ${TOPIC_ID}

subscription:
	SERVICE_URL="$(shell gcloud run services describe pubsub-subscriber --region=${CLOUD_RUN_REGION} | grep URL | awk '{ print $$2 }')"; gcloud pubsub subscriptions \
		create ${SUBSCRIPTION_ID} --topic ${TOPIC_ID} --push-endpoint=$$SERVICE_URL

gcloud_build:
	gcloud builds submit --config=cloudbuild.yaml --substitutions=_TOPIC_ID=${TOPIC_ID},_PROJECT_ID=${PROJECT_ID} .

publisher_docker:
	docker run \
		-p 8000:8000 \
		-v ${CERTS_FOLDER}:${CERTS_MOUNT} \
		-e PORT=8000 -e PROJECT_ID=${PROJECT_ID} -e TOPIC_ID=${TOPIC_ID} -e GOOGLE_APPLICATION_CREDENTIALS=${CERTS_FILE} \
		publisher

publisher:
	gunicorn publisher.main:app

subscriber:
	gunicorn subscriber.main:app

deploy: protos gcloud_build

pubsub: topic subscription

.PHONY: publisher subscriber docker