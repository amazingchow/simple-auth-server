.PHONY: check
check:
	@pyflakes auth_server.py
	@pyflakes blueprint_module/*.py
	@pyflakes concurrency_safe_shelve/*.py
	@pyflakes utils/*.py
	@pycodestyle auth_server.py --ignore=E402,E501
	@pycodestyle blueprint_module/*.py --ignore=E402,E501
	@pycodestyle concurrency_safe_shelve/*.py --ignore=E402,E501
	@pycodestyle utils/*.py --ignore=E402,E501

.PHONY: run_server_local
run_server_local:
	@export FLASK_APP=auth_server && export FLASK_ENV=development && flask run --host="0.0.0.0" --port=15555

.PHONY: run_serverd
run_serverd:
	@nohup `export FLASK_APP=auth_server && export FLASK_ENV=production && flask run --host="0.0.0.0" --port=15555 2>&1 | tee serverd.log` &
