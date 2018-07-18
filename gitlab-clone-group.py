#!/usr/bin/env python3
import logging
import sys
import argparse
import os 
import requests

class GitLabException(Exception):
  def __init__(self, code, msg):
    self.code = code
    self.msg = msg

  def __repr__(self):
    return "{} - {}".format(self.code, self.msg)

def setup_logger():
  logger.setLevel(logging.INFO)
  handler = logging.StreamHandler()
  formatter = logging.Formatter("%(asctime)s : %(message)s", "%Y-%m-%d %H:%M:%S")
  handler.setFormatter(formatter)
  logger.addHandler(handler)

def check_dest(dir):
  if os.path.isdir(dir) and os.listdir(dir) == []:
    return dir
  else:
    msg = "{} is not a valid directory. You must supply an existing, empty directory".format(dir)
    raise argparse.ArgumentTypeError(msg)

def generate_parser():
  parser = argparse.ArgumentParser(description="Download all projects from a GitLab group to a specified location")
  parser.add_argument('--gitlab-fqdn', required=True,
                      help="FQDN of the GitLab instance")
  parser.add_argument('--group', required=True,
                      help="GitLab group to clone from")
  parser.add_argument('--token', required=True,
                      help="GitLab Personal Access Token")
  parser.add_argument('--dry-run', action='store_true',
                      help="Test script without modifying the filesystem")
  parser.add_argument('dest', type=check_dest,
                      help="Directory to store clones in. Must be empty")
  return parser

def get_projects_for_group(gitlab_fqdn, group, token):
  projects = list()

  # GitLab exposes pagination via the Link header. Loop through until we have all the data
  url = "https://{}/api/v4/groups/{}/projects?simple=true&private_token={}".format(gitlab_fqdn, group, token)
  while True:
    res = requests.get(url)
    logger.debug("Downloading next page from {}".format(res.url))
    
    if not res.ok:
      raise GitLabException(res.response_code, res.text)
    
    projects.extend(res.json())
    
    if url == res.links['last']['url']:
        break
    else:
      url = res.links['next']['url']
  return projects

def main():
  setup_logger()
  parser = generate_parser()
  args = parser.parse_args()

  try:
    projects = get_projects_for_group(args.gitlab_fqdn, args.group, args.token)
  except GitLabException as err:
    logger.info(err)
    return 1

  logger.info("{} Projects retreived from GitLab API".format(len(projects)))  
  logger.info("Running git against all repos")

  logger.info("Storing repos in {}".format(args.dest))
  os.chdir(args.dest)
  for project in projects:
    if not args.dry_run:
      os.system("git clone {}".format(project['ssh_url_to_repo']))
    else:
      logger.info("git clone {}".format(project['ssh_url_to_repo']))

  logger.info("Cloning complete. Bye!")
  return 0

if __name__ == '__main__':
  logger = logging.getLogger()
  sys.exit(main())