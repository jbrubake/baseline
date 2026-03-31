# Steps to Baseline

Download and run the bootstrap script:

```sh
$ wget https://raw.githubusercontent.com/jbrubake/baseline/refs/heads/master/bootstrap
$ sudo /bin/sh bootstrap
```

Run the initial playbook:

```sh
$ cd /opt/baseline
$ sudo -u ansible ansible-playbook playbooks/main.yaml
```
