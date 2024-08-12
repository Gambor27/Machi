from typing import List, Optional
from openai import OpenAI
import datetime
import locale

def filter_models(starts_with: Optional[List[str]] = ["gpt", "ft:gpt"], blacklist: Optional[List[str]] = ["instruct"]) -> List[tuple]:
    """
    Fetches and filters model names and creation dates from the OpenAI API based on specified criteria.
    
    Parameters:
        starts_with (List[str]): A list of prefixes to include models that start with any of them.
        blacklist (List[str]): A list of substrings to exclude models that contain any of them.
    
    Returns:
        List[tuple]: A list of filtered model tuples (model name, creation date) that meet the criteria.
    """
    client = OpenAI()
    try:
        model_obj = client.models.list()  # API call
    except Exception as err:
        raise ValueError(f"Model listing API call failed: {err}") from None
    
    model_list = sorted([(model.id, model.created) for model in model_obj.data], key=lambda x: x[0])

    def starts_with_any(model_tuple: tuple, starts_with_list: List[str]) -> bool:
        return any(model_tuple[0].startswith(prefix) for prefix in starts_with_list)

    def contains_blacklisted(model_tuple: tuple, blacklist: List[str]) -> bool:
        return any(blacklisted in model_tuple[0] for blacklisted in blacklist)

    filtered_models = [model for model in model_list
                       if starts_with_any(model, starts_with)
                       and not contains_blacklisted(model, blacklist)]

    return filtered_models

locale.setlocale(locale.LC_ALL, '')

default_filtered_models = filter_models(["ft:"])
print("-- All fine-tune models --")
if default_filtered_models:
    print("\n".join(f"{model[0]}, Created: {datetime.datetime.fromtimestamp(model[1]).strftime('%c')}" for model in default_filtered_models))
else:
    print("No models meeting criteria")

default_filtered_models = filter_models(["ft:gpt-3.5-turbo-0125"])
print("-- Fine-tune models compatible with Assistants --")
if default_filtered_models:
    print("\n".join(f"{model[0]}, Created: {datetime.datetime.fromtimestamp(model[1]).strftime('%c')}" for model in default_filtered_models))
else:
    print("No models meeting criteria")