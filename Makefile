docker-image:
	docker build \
		-t mockup-gitlab-issuer \
		--build-arg uid=`id -u` \
		.

