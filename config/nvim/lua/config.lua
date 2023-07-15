-- https://www.reddit.com/r/neovim/comments/11d1wjm/lazy_vs_packer
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable",
        lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

vim.g.mapleader = " " -- Make sure to set `mapleader` before lazy so your mappings are correct
vim.g.localmapleader = " "

require('lazy').setup({
    {
        "williamboman/mason.nvim",
        build = ":MasonUpdate", -- :MasonUpdate updates registry contents
        opts = {
            ensure_installed = {
                'pyright',
                'clangd',
                'ltex-ls',
                'awk-languge-server',
                'bash-language-server',
            }
        }
    },
    'neovim/nvim-lspconfig',
    {
        'ms-jpq/coq_nvim',
        branch = 'coq',
        build = ':COQDeps',
    },
    {
        'ms-jpq/coq.artifacts',
        branch = 'artifacts',
    }, -- Can also potentially use https://github.com/ms-jpq/coq.thirdparty
    'ryanoasis/vim-devicons',
    'preservim/nerdtree',
    {
        'nvim-telescope/telescope.nvim',
        branch = '0.1.x',
        dependencies = { 'nvim-lua/plenary.nvim' }
    },
    'NvChad/nvim-colorizer.lua',
    'sunjon/shade.nvim',
    'navarasu/onedark.nvim',
    {
        'nvim-treesitter/nvim-treesitter',
        build = ':TSUpdate',
        opts = {
            ensure_installed = {
                'c',
                'cpp',
                'cuda',
                'dot',
                'lua',
                'vim',
                'python',
                'bash',
                'git_config',
                'git_rebase',
                'gitattributes',
                'gitcommit',
                'gitignore',
                'glsl',
            }
        }
    },
    'folke/which-key.nvim',
})

-- Mason
require("mason").setup()

-- Language server + coq
local lsp = require('lspconfig')
local coq = require('coq')
lsp.pyright.setup(coq.lsp_ensure_capabilities({}))
lsp.clangd.setup(coq.lsp_ensure_capabilities({}))
lsp.ltex.setup(coq.lsp_ensure_capabilities({}))
lsp.awk_ls.setup(coq.lsp_ensure_capabilities({}))
lsp.bashls.setup(coq.lsp_ensure_capabilities({}))

-- NERDTree
vim.keymap.set('n', '<leader>n', ':NERDTreeFocus<CR>')
vim.keymap.set('n', '<C-n>', ':NERDTree<CR>')
vim.keymap.set('n', '<C-t>', ':NERDTreeToggle<CR>')
vim.keymap.set('n', '<C-f>', ':NERDTreeFind<CR>')

-- Telescope
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, {})
vim.keymap.set('n', '<leader>fg', builtin.live_grep, {})
vim.keymap.set('n', '<leader>fb', builtin.buffers, {})
vim.keymap.set('n', '<leader>fh', builtin.help_tags, {})

-- Colorize
-- TODO: Is this really correct?
require('colorizer').setup()

-- Shade
require('shade').setup({
    overlay_opacity = 50,
    opacity_step = 1,
    keys = {
        brightness_up = '<C-Up>',
        brightness_down = '<C-Down>',
        toggle = '<leader>s',
    }
})

-- Onedark
require('onedark').setup({
    style = 'darker'
})
require('onedark').load()

-- Treesitter
require('nvim-treesitter.configs').setup({
    ensure_installed = {
        'c',
        'cpp',
        'cuda',
        'dot',
        'lua',
        'vim',
        'python',
        'bash',
        'git_config',
        'git_rebase',
        'gitattributes',
        'gitcommit',
        'gitignore',
        'glsl',
    },
    auto_install = true,
    highlight = {
        enable = true,
        additional_vim_regex_highlighting = false,
    }
})
