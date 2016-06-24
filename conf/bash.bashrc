################### system normal conf ######################
# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=10000
HISTFILESIZE=20000

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

###################### private conf ###########################
root="/home/`who am i | awk '{print $1}'`/work"

# java
export JAVA_HOME="$root/env/lang/jdk1.8"
export CLASSPATH=".:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar"

# to add in path
mylist=(
        "env/lang/jdk1.8/bin"
        "ide/SublimeText/sublime_text_3"
       )
len=${#mylist[@]}
for ((i=0; i<$len; i++))
do
    item="$root"/${mylist[$i]}
    if [[ -d "$item" ]]; then
        export PATH="$item:$PATH"
    fi
done
