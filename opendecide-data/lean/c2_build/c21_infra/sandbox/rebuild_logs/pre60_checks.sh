for n in python node go sh; do echo "$n $(docker image inspect --format '{{.Id}}' od-sbx/$n:frozen)"; done
echo "tree hash: $(/usr/bin/python3 -I /opt/od-sbx/executor/od_sbx_launcher.py treehash /opt/od-sbx/executor)"
echo "containers: $(docker ps -aq | wc -l)"
echo "docker group: [$(getent group docker)]"
echo "var/lib/od-sbx files: $(ls -A /var/lib/od-sbx | wc -l)"
echo "driver/runtime: $(docker info --format '{{.Driver}} {{.DefaultRuntime}}')"
echo "stage mount: $(findmnt -no FSTYPE,TARGET,SIZE -T /srv/od-sbx/stage)"
sha256sum /tmp/sandbox/pins.env /opt/od-sbx/requirements.lock /etc/od-sbx/hostfw.nft /etc/docker/daemon.json
echo "home listing:"; ls -A /home/*/
