"vim-sound-key
function Vks()
    "#!/usr/bin/env python
    try
        call vimproc#system_bg("python " . $HOME . "/dev/vim-key-sound/vim-key-sound.py " .getline('.')[col('.')-2])
    catch
    endtry
endfunction
command! Vks call Vks()
autocmd CursorMovedI * : call Vks()
