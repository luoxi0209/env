root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
user_home=~

sudo bash ./install/install_software.sh
python ./install/install_local_software.py $root

# bashrc
cd $user_home
ln -s -f $root/conf/bash.bashrc .bashrc
ln -s -f $root/ide/vim/vimrc .vimrc
ln -s -f $root/ide/vim/ .vim
