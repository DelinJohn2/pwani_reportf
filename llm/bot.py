from config import load_anthropic_api_config, load_open_ai_api_config
from langchain.chat_models import init_chat_model
import os


def load_llm_anthorpic():
    config_files = load_anthropic_api_config()
    
   
    # os.environ["OPENAI_API_KEY"] = config_files["api_key"]
    
    
    llm = init_chat_model(
        model=config_files["model"],
        model_provider=config_files["provider"],
        api_key=config_files["api_key"],
         max_tokens=64000
    )
    return llm


def load_gpt_llm():
    config_files = load_open_ai_api_config()
    
    # os.environ["OPENAI_API_KEY"] = config_files["api_key"]
    
    llm = init_chat_model(
        model=config_files["model"],
        model_provider=config_files["provider"],
        api_key=config_files["api_key"],
        
    )
    return llm