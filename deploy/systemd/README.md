# Prerequisites

- Linux machine with:
	- systemd
	- Docker must be running and the image must be available locally
	- image: service-health-monitor:local
	- outbound network access to the TARGET_URL 

# Installation

All required files can be cloned from https://github.com/HirokiHonto/service-health-monitor. 

Make sure to copy the service and timer files  (from repository root directory):

```
sudo cp deploy/systemd/service-health-monitor.service /etc/systemd/system/
sudo cp deploy/systemd/service-health-monitor.timer /etc/systemd/system/
sudo cp deploy/systemd/service-health-monitor.env.example /etc/service-health-monitor.env
```

*The final command is for **initial installation**. Running it again overwrites the machine’s configured target with the example value.*
# Configuration

Change the TARGET_URL in the installed service-health-monitor.env  as per your needs.

# Startup

The timer starts at boot and schedules the first check approximately one minute after boot. Subsequent checks are scheduled five minutes after the previous service activation..  Reload systemd, test the service once manually then enable the timer with these commands:

```
sudo systemctl daemon-reload
sudo systemctl start service-health-monitor.service
sudo journalctl -u service-health-monitor.service -n 20 --no-pager
```

If the latest run shows the intended URL, HTTP `200`, and successful completion, then run:

```
sudo systemctl enable --now service-health-monitor.timer
```
# Inspection 

Command to see the next scheduled run:

```
systemctl --no-pager list-timers service-health-monitor.timer
```

Command to check the last runs

```
sudo journalctl -u service-health-monitor.service --since "10 minutes ago" --no-pager
```


# Expected behavior

Each timer trigger starts the service, which creates a container to perform one check. The container exits afterward. For a successful `Type=oneshot` service, `inactive (dead)` is normal; the timer remains active.

Monitor exit codes:

- **`0`**: target is healthy.
- **`1`**: target is unhealthy or unreachable.