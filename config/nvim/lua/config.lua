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
    },
    {
        'ms-jpq/coq.artifacts',
        branch = 'artifacts',
    },
    -- Can also potentially use https://github.com/ms-jpq/coq.thirdparty
    'folke/which-key.nvim',
})

require("mason").setup()

local lsp = require('lspconfig')
local coq = require('coq')
lsp.pyright.setup(coq.lsp_ensure_capabilities({}))
lsp.clangd.setup(coq.lsp_ensure_capabilities({}))
lsp.ltex.setup(coq.lsp_ensure_capabilities({}))
lsp.awk_ls.setup(coq.lsp_ensure_capabilities({}))
lsp.bashls.setup(coq.lsp_ensure_capabilities({}))
