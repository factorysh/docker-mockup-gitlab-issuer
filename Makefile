docker-image:
	docker build \
		-t mockup-gitlab-issuer \
		--build-arg uid=`id -u` \
		.

push:
	git push git@github.com:factorysh/docker-mockup-gitlab-issuer.git master
