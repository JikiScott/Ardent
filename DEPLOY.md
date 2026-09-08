# Ardent Update Deployment
## Production Host
Ardent is deployed on an Oracle Cloud Ubuntu VM and managed by systemd.

## Update Production

SSH into server and

```bash
cd ~/Ardent
git pull
sudo systemctl restart ardent
sudo systemct1 status ardent
journalctl -u ardent -n 50 --no-pager
```

## Self-Deploy

```bash
git add DEPLOY.md
git commit -m "[NOTE]"
git push
```