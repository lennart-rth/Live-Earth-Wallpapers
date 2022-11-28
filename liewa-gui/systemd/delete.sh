systemctl --user stop $1
systemctl --user disable $1
rm -r ~/.config/systemd/user
mkdir ~/.config/systemd/user
systemctl --user daemon-reload