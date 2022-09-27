from fastapi import Request
from fastapi.responses import JSONResponse


class GenericException(Exception):
    msg = "Generic Error"
    code = 500

    def __init__(self, message: str = None, code: int = None):
        if message:
            self.msg = message
        if code:
            self.code = code

    def __str__(self) -> str:
        return f"[{self.code}] - {self.msg}"


class NotFoundException(GenericException):
    msg = "Not found"
    code = 404

    def __init__(self, element : str = None):
        if element:
            self.element = element
            self.msg = f"{element} Not found"


class AlreadyExistsException(GenericException):
    msg = "Object with provided key already exists"
    code = 409

    def __init__(self, element : str = None):
        if element:
            self.element = element
            self.msg = f"{element} with provided key already exists"


class AlreadyPerformedException(GenericException):
    msg = "Request already satisfied for object with provided key"
    code = 409

    def __init__(self, element):
        self.element = element
        self.msg = f"Request already satisfied for {element} with provided key"


class ForbiddenException(GenericException):
    msg = "You must provide a valid token to access this URL"
    code = 403

    def __init__(self, access_key_type="API Key"):
        self.access_key_type = access_key_type
        self.msg = f"You must provide a valid {access_key_type} to access this URL"


async def unicorn_exception_handler(
    request: Request, exc: GenericException
):
    return JSONResponse(
        status_code=exc.code,
        content={ "message": exc.msg },
    )


async def unknown_exception_handler(
    request: Request, exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={ "message": str(exc) },
    )


async def not_found_exception_handler(
    request: Request, exc: NotFoundException
):
    return JSONResponse(
        status_code=exc.code,
        content={ "message": exc.msg },
    )


async def already_exists_exception_handler(
    request: Request, exc: AlreadyExistsException
):
    return JSONResponse(
        status_code=exc.code,
        content={ "message": exc.msg },
    )


async def already_performed_exception_handler(
    request: Request, exc: AlreadyPerformedException
):
    return JSONResponse(
        status_code=exc.code,
        content={ "message": exc.msg },
    )


async def forbidden_exception_handler(
    request: Request, exc: ForbiddenException
):
    return JSONResponse(
        status_code=exc.code,
        content={ "message": exc.msg },
    )