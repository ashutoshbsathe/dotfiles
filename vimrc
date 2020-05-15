" .vimrc
" Kanged from https://dougblack.io/words/a-good-vimrc.html

set nocompatible "__ VI compatible mode is disabled so that VIM things work

set tabstop=4 "__ VIM will enter 4 spaces when reading <TAB> character
set softtabstop=4 "__ VIM will enter 4 spaces when editing
set expandtab "__ VIM will expand tabs to spaces
set autoindent 
set number
set showcmd
set cursorline
filetype indent on
set wildmenu
set lazyredraw "__ for faster macros
set showmatch "__ highlight matching [], {}, ()
set incsearch "__ modern searching - search as you are typing the word
set hlsearch "__ highlight the matching things
set foldenable
set foldmethod=indent "__ mostly tailored for python. use `:help foldmethod` for other options
"__ move actual lines vertically as opposed to moving to wrapped around parts
nnoremap j gj 
nnoremap k gk
inoremap <C-L> <Esc>
