import pynvim
from pynvim.api import Nvim
from llama_index.llms.ollama import Ollama


@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim: Nvim = nvim
        self.default_ollama_model = Ollama(model="llama3:latest", request_timeout=500.0)

    @pynvim.function("TestFunction", sync=True)
    def testfunction(self, args):
        return 3

    @pynvim.command("OllamaShowAvailableModels", nargs="*", range="")
    def show_available_models(self):
        response = self.default_ollama_model.get_available_models()
        self.nvim.current.buffer.append(response.text)

    @pynvim.command("TestOllama", nargs="*", range="")
    def test_ollama(self, args, range):
        response = self.default_ollama_model.complete(
            "Write a random piece of code",
            format="json",
            system="Showcase your coding skills!",
        )
        lines = response.text.split("\n")
        self.nvim.current.buffer.append(lines)

    @pynvim.command("TestCommand", nargs="*", range="")
    def testcommand(self, args, range):
        self.nvim.current.line = "Command with args: {}, range: {}".format(args, range)

    @pynvim.autocmd("BufEnter", pattern="*.py", eval='expand("<afile>")', sync=True)
    def on_bufenter(self, filename):
        self.nvim.out_write("testplugin is in " + filename + "\n")
