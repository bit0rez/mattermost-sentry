REGISTRY ?= localhost:5000
PROJECT ?= mattermost-sentry
VERSION ?= latest

all: $(PROJECT)

$(PROJECT):
	@docker build --rm -t $(REGISTRY)/$(PROJECT):$(VERSION) .

clean:
	@docker rmi $(REGISTRY)/$(PROJECT):$(VERSION)

push:
	@docker push $(REGISTRY)/$(PROJECT):$(VERSION)

