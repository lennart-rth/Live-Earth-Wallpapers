systemctl --user stop $1
systemctl --user disable $1
rm -r ~/.config/systemd/user
mkdir ~/.config/systemd/user
systemctl --user daemon-reload

# systemctl stop $1
# systemctl disable $1
# rm -r /etc/systemd/system/
# mkdir /etc/systemd/system/
# systemctl daemon-reload