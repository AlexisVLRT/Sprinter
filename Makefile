ENV ?= dev
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
	gcloud beta run deploy $(1)\
	 --image $(2) \
	 --platform=managed \
	 --region=europe-west1 \
	 --service-account=$(3)\
	 --allow-unauthenticated \
	 $(4)
endef

######################################
# Credentials
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

.PHONY: build_processor_container
build_processor_container:
	$(call docker_build,${PROCESSOR_CONTAINER},${PROCESSOR_PATH}/Dockerfile,.)

.PHONY: push_processor_container
push_processor_container: build_processor_container
	$(call docker_push,${PROCESSOR_CONTAINER},${PROCESSOR_GCR_PATH})

.PHONY: deploy_processor
deploy_processor: push_processor_container
	$(call deploy_cloud_run,${PROCESSOR_SERVICE},${PROCESSOR_GCR_PATH},${SERVICE_ACCOUNT},--update-env-vars ENV=${ENV})


######################################
## PUB/SUB
.PHONY: create_topic
create_topic:
	gcloud pubsub topics create ${BROKER_TOPIC}

.PHONY: create_sub
create_sub:
	gcloud pubsub subscriptions create \
	  --topic=${BROKER_TOPIC}\
	  --push-endpoint=https://processor-dev-7juntucg4q-ew.a.run.app \
	  --ack-deadline=90 \
	  ${BROKER_SUB}
