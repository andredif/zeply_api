import argparse
import os
from fastapi import FastAPI

from . import exceptions as custom_exceptions, routers

app = FastAPI()

app.include_router(routers.api_router, prefix="/api")


app.add_exception_handler(
    Exception, custom_exceptions.unknown_exception_handler)
app.add_exception_handler(
    custom_exceptions.GenericException,
    custom_exceptions.unicorn_exception_handler)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--debug",
    action='store_true',
    default=False,
    help=(
        "Provide debug mode. "
        "Example --debug', default=False"
    )
)
parser.add_argument(
    "-host",
    "--host",
    default="0.0.0.0",
    help=(
        "Provide server host. "
        "Example --host=192.168.10.4', default='0.0.0.0'"
    )
)
parser.add_argument(
    "-p",
    "--port",
    default="8000",
    help=(
        "Provide server port. "
        "Example --port=5678', default='8000'"
    )
)


if __name__ == "__main__":
    import uvicorn
    options = parser.parse_args()

    uvicorn.run(
        "zeplyapi.main:app", host=options.host, port=int(options.port),
        reload=options.debug, log_config=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logging.json'))
