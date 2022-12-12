# DIRPATH=$(echo $(pwd))
# PYTHONPATH=$(which python3)

# cat > liewa.service << EOL
# [Unit]
# Description=Liewa Service
# [Service]
# Type=simple
# ExecStart=$(which liewa)
# EOL

# cat > liewa.timer << EOL
# [Unit]
# Description=Liewa Timer
# [Timer]
# OnBootSec=10
# OnUnitActiveSec=30
# AccuracySec=1ms
# [Install]
# WantedBy=timers.target
# EOL

