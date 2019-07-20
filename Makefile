##
# Generic Wielder
#

NOSE := nose2

all:
	@echo targets:
	@echo \* test -- trigger testing

.PHONY: test
test: setup_test
	${NOSE} --verbose --config ./test/nose2.cfg

.PHONY: setup_test 
setup_test: 
	mkdir ./test/task/


