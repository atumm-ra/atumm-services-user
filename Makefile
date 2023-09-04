# use the rest as arguments for targets
TARGET_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# ...and turn them into do-nothing targets
$(eval $(TARGET_ARGS):;@:)

COMPOSE=docker compose

help:		   		## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'




# local
format:
	@sh -c " \
		pdm run ssort src/atumm/**; \
		pdm run isort src/atumm/**; \
		pdm run black src/atumm/** \
	"

install:
	pdm sync

test:					## run tests
	STAGE=test pdm run pytest --capture=no -cov --cov-report html

testf:					## run test filtered by pattern
	STAGE=test pdm run pytest -k $(TARGET_ARGS)

new-svc:
	pdm run python atumm/core/entrypoints/cli/commands.py $(TARGET_ARGS)

new-rsc:			## create a new rest resource within a service (service_name, resource_name), ex: make new-resource user tokens
	pdm run python atumm/core/entrypoints/cli/commands.py create-rest-resource $(TARGET_ARGS)