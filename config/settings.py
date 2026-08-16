from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 默认基础配置类，可以从虚拟环境里读取相同名字的变量，且变量名字不区分大小写
    LLM_MODEL:str = "default"
    LLM_API_KEY:str = ""
    LLM_BASE_URL:str = ""
    TEMPERATURE:float=0.7

    class Config:
        env_file = ".env"

settings = Settings()