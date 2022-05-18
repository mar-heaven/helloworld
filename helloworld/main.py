from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from helloworld.api.api_v1.api import api_router
from helloworld.settings import settings
from helloworld.middleware import start_up, shutdown


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
        openapi_url="/api/v1/openapi.json",
        default_response_class=ORJSONResponse
    )
    application.include_router(api_router, prefix=settings.api_v1_str)
    application.add_event_handler("startup", start_up)
    application.add_event_handler("shutdown", shutdown)
    return application


app = get_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
