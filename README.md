   vim-key-sound.py

   'vim-key-sound.py' is forked from

   ✘╹◡╹✘  音の鳴るエディタことVim
   http://r7kamura.hatenablog.com/entry/2012/10/09/155041

   ssig33.com 音が鳴るエディタ軽量化
   http://ssig33.com/text/音が鳴るエディタ軽量化

   [Requirements]
    to use 'vim-key-sound.py', you need

       portaudio
       pyaudio
       pyo
       vimproc

    Sorry, I verified this code only on Mac OS X Lion 10.7.5, python 2.7.3

   [to Use]

    set 'vks/tmp' in a directory you want and rewrite variable 'path' in vim-key-sound.py

       path = any_dir/you_set

    and add code in vimrc.vimrc to your .vimrc

   [Known Bugs & todo]

   1. There are only one sound set. some snd set will be added
   3. and more
