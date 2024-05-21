# Ollama connector plugin

Allows for LLM completions choosing the model and its parameters

## Install manually

### Make sure requirements are installed in python environment set for nvim

`vim.g.python3_host_prog = '/path/to/your/env'`

### Moving the plugin

cp main.py ~/.config/nvim/rplugin/python3

### Updating in nvim

`:UpdateRemotePlugins`

#### You could also make an binding to do it faster

vim.api.nvim_set_keymap('n', '<leader>pu', ':UpdateRemotePlugins<CR>', { noremap = true, silent = true })
