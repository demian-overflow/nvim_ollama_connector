import httpx
from httpx import Timeout
import pynvim
from pynvim.api import Nvim
from llama_index.llms.ollama import Ollama


@pynvim.plugin
class OllamaConnector(object):
    def __init__(self, nvim):
        self.nvim: Nvim = nvim
        self.default_ollama_model = Ollama(model="llama3:latest", request_timeout=500.0)
        self.default_ollama_model_name = "llama3:latest"

    @pynvim.function("OllamaShowAvailableModels", sync=True)
    def show_available_models(self, _):
        with httpx.Client(
            timeout=Timeout(self.default_ollama_model.request_timeout)
        ) as client:
            response = client.get(
                url=f"{self.default_ollama_model.base_url}/api/tags",
            )
            response.raise_for_status()
            raw = response.json()
            models_names = [model["name"] for model in raw["models"]]
            self.nvim.out_write("\n".join(models_names))

    @pynvim.function("OllamaGenerate", sync=True)
    def generate(self, args):
        format = None
        system_prompt_text = None
        model_name = None
        # Pynvim passes a list of arguments to the function, so we need to unpack them
        prompt_text = args[0]
        if len(args) > 1:
            model_name = args[1]
        if len(args) > 2:
            system_prompt_text = args[2]
        if len(args) > 3:
            format = args[3]
        if model_name and (model_name != self.default_ollama_model_name):
            self.default_ollama_model = Ollama(model=model_name, request_timeout=500.0)
            self.default_ollama_model_name = model_name
        # Since defaults may vary for each model, we need to check for the presence of each argument
        if not format and not system_prompt_text:
            response = self.default_ollama_model.complete(
                prompt_text,
            )
            return response.text
        if format and not system_prompt_text:
            response = self.default_ollama_model.complete(
                prompt_text,
                format=format,
            )
            return response.text
        if not format and system_prompt_text:
            response = self.default_ollama_model.complete(
                prompt_text,
                system_prompt_text=system_prompt_text,
            )
            return response.text
        response = self.default_ollama_model.complete(
            prompt_text,
            format=format,
            system_prompt_text=system_prompt_text,
        )
        return response.text
