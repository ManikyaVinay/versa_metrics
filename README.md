# versa_metrics
Automation to collect Versa metrics

# Creating Package

- Install [fpm](http://fpm.readthedocs.io/en/latest/installing.html)
- Clone `versa_metrics` source repository
- Create debian package with following command
```
fpm  -t deb -s dir -n versa-metrics --deb-init startup/deb/vnf-metrics -v 1.1 src/versa_metrics/=/opt/versa_metrics/
```

# Installation
## apt
```
apt-get install versa-metrics
```
## dpkg
```
dpkg -i versa-metrics
```
