ENV ?= dev
PROCESSOR_PATH ?= lib/processor
BROKER_PATH ?= lib/broker

include environments/${ENV}


define create_bucket
	gsutil ls \
	-b gs://$(1) \
	|| \
	gsutil mb \
	-l ${REGION} \
	gs://$(1)
endef

define create_service_account
	gcloud iam service-accounts describe $(1)@${PROJECT}.iam.gserviceaccount.com \
	|| \
	gcloud iam service-accounts create $(1) \
    --description "$(2)" \
    --display-name "$(1)"
endef

define service_account_add_role
	gcloud projects add-iam-policy-binding $(1) \
	  --member serviceAccount:$(2)@$(1).iam.gserviceaccount.com \
	  --role roles/$(3)
endef

define create_service_account_credentials
	gcloud iam service-accounts keys create ./secrets/$(1) \
  		--iam-account $(2)
endef

define docker_build
	docker build --rm -t $(1) -f $(2) $(3)
endef

define docker_push
	docker tag $(1) $(2)
	docker push $(2)
endef

define deploy_cloud_run
	gcloud beta run deploy $(1) \
	 --image $(2) \
	 --platform=managed \
	 --region=europe-west1 \
	 --service-account=$(3)\
	 --allow-unauthenticated \
	 --memory $(5) \
	 $(4)
endef

define create_topic
	gcloud pubsub topics describe $(1) \
	|| \
	gcloud pubsub topics create $(1)
endef

define create_push_sub
	gcloud pubsub subscriptions describe $(1) \
	|| \
	gcloud pubsub subscriptions create \
	  --topic=$(2) \
	  --push-endpoint=$(3) \
	  --ack-deadline=600 \
	  $(1)
endef

define create_pull_sub
	gcloud pubsub subscriptions describe $(1) \
	|| \
	gcloud pubsub subscriptions create \
	  --topic=$(2)\
	  --ack-deadline=600 \
	  $(1)
endef

######################################
## CREDENTIALS
.PHONY: create_service_account
create_service_account:
	$(call create_service_account,$(SERVICE_ACCOUNT_ID),generic dev account)

.PHONY: get_gcp_credentials
get_gcp_credentials:
	$(call create_service_account_credentials,$(SERVICE_ACCOUNT_JSON),$(SERVICE_ACCOUNT))

.PHONY: give_admin_role
give_admin_role:
	$(call service_account_add_role,$(PROJECT),$(SERVICE_ACCOUNT_ID),admin)

.PHONY: setup_creds
setup_creds:create_service_account give_admin_role get_gcp_credentials

######################################
## STORAGE
.PHONY: create_data_bucket
create_data_bucket:
	$(call create_bucket,$(DATA_BUCKET))


######################################
## CLOUD RUN
.PHONY: build_broker_container
build_broker_container:
	$(call docker_build,${BROKER_CONTAINER},${BROKER_PATH}/Dockerfile,.)

.PHONY: push_broker_container
push_broker_container: build_broker_container
	$(call docker_push,${BROKER_CONTAINER},${BROKER_GCR_PATH})

.PHONY: deploy_broker
deploy_broker: push_broker_container
	$(call deploy_cloud_run,${BROKER_SERVICE},${BROKER_GCR_PATH},${SERVICE_ACCOUNT},--update-env-vars ENV=${ENV}, ${BROKER_MEMORY})


######################################
## PUB/SUB
.PHONY: create_broker_topic
create_broker_topic:
	$(call create_topic,${BROKER_TOPIC})

.PHONY: create_broker_sub
create_broker_sub: create_broker_topic
	$(call create_push_sub,${BROKER_SUB},${BROKER_TOPIC},${PROCESSOR_ENDPOINT})

.PHONY: create_buffer_topic
create_buffer_topic:
	$(call create_topic,${TASKS_BUFFER_TOPIC})

.PHONY: create_buffer_sub
create_buffer_sub: create_buffer_topic
	$(call create_pull_sub,${TASKS_BUFFER_SUB},${TASKS_BUFFER_TOPIC})


#####################################
## DATASTORE
.PHONY: delete_jobs
delete_jobs:
	python -c """from lib.cloud_utils.datastore import Datastore; Datastore.instance().delete_entities('Job', {})"""

.PHONY: delete_tasks
delete_tasks:
	python -c """from lib.cloud_utils.datastore import Datastore; Datastore.instance().delete_entities('Task', {})"""

.PHONY: delete_entities
delete_entities: delete_jobs delete_tasks


#####################################
## FUNCTIONS
.PHONY: deploy_function
deploy_function:
	python bin/function_deployer.py


#####################################
## RUN
.PHONY: misc_automation
misc_automation:
	python bin/misc_automation.py

.PHONY: deploy
deploy: misc_automation deploy_broker deploy_function

.PHONY: run
run: delete_entities
	python bin/end_to_end.py
