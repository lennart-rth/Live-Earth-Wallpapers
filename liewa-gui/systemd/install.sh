DIRPATH=$(echo $(pwd))
PYTHONPATH=$(which python3)

cat > liewa.service << EOL
[Unit]
Description=Very useful script
[Service]
Type=simple
ExecStart=$(which liewa)
EOL

cat > liewa.timer << EOL
[Unit]
Description=Run very useful script every 30 
[Timer]
OnBootSec=10
OnUnitActiveSec=30
AccuracySec=1ms
[Install]
WantedBy=timers.target
EOL

cp "liewa.service" ~/.config/systemd/user/
cp "liewa.timer" ~/.config/systemd/user/

systemctl --user enable liewa.timer
systemctl daemon-reload
systemctl --user start liewa.timerq
systemctl --user status liewa.service

# systemctl restart liewa