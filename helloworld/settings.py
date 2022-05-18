from pydantic import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = True
    project_name: str = "helloworld"
    api_v1_str: str = "/api/v1"
    log_level: str = 'INFO'
    mongodb_url: str = 'mongodb://127.0.0.1:27017/helloworld?auth213213Source=admin'


settings = AppSettings()

if settings.debug:
    print('=' * 20)
    for k, v in settings.dict().items():
        print(f'[system-config Config] {k} = {v}')
    print('=' * 20, flush=True)
