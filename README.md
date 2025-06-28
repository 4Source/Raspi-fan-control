# Setup
### 1. Clone the repository 
Clone the repository into ``/usr/local/bin``
```sh
cd /usr/local/bin
git clone https://github.com/4Source/Raspi-fan-control.git
```

### 2. Make Script executable
```sh
cd Raspi-fan-control
chmod +x fancontrol.py
```

### 3. Install requirements
```sh
pip install -r requirements.txt
```

### 3. Test the Script is working
```sh
py fancontrol.py --test
```
**Hint:** When the script is running the fan should turn for 10s and than stop again

### 4. Systemd Service auto run
Create a Systemd Unit ``/etc/systemd/system/fancontrol.service`` with the following content
```ini
[Unit]
Description=Script to control the fan depending on the CPU temperature

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/Raspi-fan-control/fancontrol.py
User=<your-user-name>
```
**Hint:** Make sure you replace ``<your-user-name>`` with your user name

Create a timer ``/etc/systemd/system/fancontrol.timer`` to let the script start ``5min`` after boot and than every ``10min`` to run again.
```ini
[Unit]
Description=Timer for fancontrol

[Timer]
OnBootSec=5min
OnUnitActiveSec=10min
Unit=fancontrol.service

[Install]
WantedBy=timers.target
```

### 5. Activate and run
```sh
sudo systemctl daemon-reload
sudo systemctl enable --now fancontrol.timer
```

### 6. Check the timer is running
```sh
systemctl status fancontrol.timer
```