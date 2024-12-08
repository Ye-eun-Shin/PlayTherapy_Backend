from typing import TypeVar, Type

from analyze.model.domain.prompt import Prompt

T = TypeVar("T")


class BaseLLMModel:

    def __init__(self, model_name: str, temperature: float):
        self.model_name = model_name
        self.temperature = temperature

    def run(
        self, system_prompt: str, prompt: Prompt, variables: dict, class_type: Type[T]
    ) -> T:
        return class_type()
