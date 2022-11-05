
# The following lines were added by compinstall

zstyle ':completion:*' completer _expand _complete _ignored _correct _approximate
zstyle :compinstall filename '/home/enpassant/.zshrc'

autoload -Uz compinit
autoload -Uz vcs_info
precmd () { vcs_info }
compinit

zstyle ':vcs_info:git:*' formats ' (%b)'
# End of lines added by compinstall
# Lines configured by zsh-newuser-install
HISTFILE=~/.zsh_history
HISTSIZE=500
SAVEHIST=250
unsetopt beep
bindkey -e
# End of lines configured by zsh-newuser-install

setopt prompt_subst

PS1='%~$vcs_info_msg_0_> '