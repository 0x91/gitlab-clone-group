# GitLab Group Clone

This is a small script to clone all directories from a GitLab group (that you have access to).

This script requires the `requests` library to be installed in your Python environment.
```
usage: gitlab-clone-group.py [-h] --gitlab-fqdn GITLAB_FQDN --group GROUP
                             --token TOKEN [--dry-run]
                             dest

Download all projects from a GitLab group to a specified location

positional arguments:
  dest                  Directory to store clones in. Must be empty

optional arguments:
  -h, --help            show this help message and exit
  --gitlab-fqdn GITLAB_FQDN
                        FQDN of the GitLab instance
  --group GROUP         GitLab group to clone from
  --token TOKEN         GitLab Personal Access Token
  --dry-run             Test script without modifying the filesystem
```
