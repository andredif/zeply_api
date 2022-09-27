#!/bin/sh
set -ue

DB_HOSTNAME=${DB_HOST:-db}
DB_PORT=${DB_HOST:-5432}


case "${1:-}" in
    -shell)
        echo "$0: ${1#-}"
        set -- python -m manage shell
        ;;

    -sh)
        echo "$0: ${1#-}"
        set -- /bin/sh
        ;;

    -wait_postgres)
        echo "$0: ${1#-}"
        echo -n "Waiting Postgres to launch on $DB_PORT "
        while ! nc -z "$DB_HOSTNAME" "$DB_PORT"; do
            sleep 1
            echo -n "."
        done
        set -- echo -e "\nPostgres launched"
        ;;

    -startserver)
        echo "$0: ${1#-} PORT:$PORT HOST:$HOST RESOURCES:$RESOURCES_PATH"
        uvicorn --port $PORT --host $HOST \
                --ssl-certfile ${RESOURCES_PATH}/etc/ssl/server.cer \
                --ssl-keyfile ${RESOURCES_PATH}/etc/ssl/server.key \
                --ssl-ca-certs ${RESOURCES_PATH}/etc/ssl/ca_path_info \
                app:app
        ;;

    -startserver-debug)
        echo "$0: ${1#-} PORT:$PORT HOST:$HOST"
        python -m debugpy --listen 0.0.0.0:5678 -m zeplyapi.main --port $PORT --host $HOST --debug
        ;;

    -start-service)
        echo "$0: ${1#-}"
        "$0" -wait_postgres
        "$0" -startserver-debug
esac
exec "$@"