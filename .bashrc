# ~/.bashrc
#

parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

export VISUAL=nano

if [ -n "$RANGER_LEVEL"]; then export PS1="\w"; fi

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
PS1='\w $(parse_git_branch)> '
