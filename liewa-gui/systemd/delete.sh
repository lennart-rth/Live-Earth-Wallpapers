systemctl stop $1
systemctl disable $1
rm -r ~/.config/systemd/user
mkdir ~/.config/systemd/user
systemctl daemon-reload
