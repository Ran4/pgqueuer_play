.phony: sender receiver install uninstall postgres psql

sender:
	. .venv/bin/activate && python3 src/main.py sender

receiver:
	. .venv/bin/activate && python3 src/main.py receiver

install:
	. .venv/bin/activate && \
		python -m PgQueuer install \
		--pg-host localhost --pg-port 9432 --pg-user postgres --pg-password mysecretpassword \
		--pg-database pgqueuerdb

uninstall:
	. .venv/bin/activate && \
		python -m PgQueuer uninstall \
		--pg-host localhost --pg-port 9432 --pg-user postgres --pg-password mysecretpassword \
		--pg-database pgqueuerdb

postgres:
	docker compose run --service-ports postgres-db

psql:
	PGPASSWORD=mysecretpassword psql -U postgres -h localhost -p 9432 -d pgqueuerdb
