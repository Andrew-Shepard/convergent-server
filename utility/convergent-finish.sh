#/bin/bash
set -euo pipefail
exec s6-svscanctl -t /var/run/s6/services
