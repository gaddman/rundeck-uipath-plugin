#!/usr/bin/env python3
# Connect to UiPath API to manage jobs.

import logging
import os
import requests
import sys

# Read Rundeck info from environment variables
loglevel = os.environ.get("RD_JOB_LOGLEVEL")
release_key = os.environ.get("RD_CONFIG_RELEASEKEY")
folder = os.environ.get("RD_CONFIG_FOLDER")
orgId = os.environ.get("RD_CONFIG_ORGID")
robot = os.environ.get("RD_CONFIG_ROBOT")
machine = os.environ.get("RD_CONFIG_MACHINE")
arguments = os.environ.get("RD_CONFIG_ARGUMENTS", "{}")
base_url = os.environ.get("RD_CONFIG_URL")
username = os.environ.get("RD_CONFIG_USERNAME")
password = os.environ["RD_CONFIG_PASSWORD_STORAGE_PATH"]
tenancy = os.environ.get("RD_CONFIG_TENANCY")
proxy = os.environ.get("RD_CONFIG_PROXY")

if loglevel == "DEBUG":
  logging.basicConfig(format="%(levelname)s:  %(message)s", level=logging.DEBUG)
else:
  logging.basicConfig(format="%(message)s", level=logging.INFO)


class UiPath():
  def __init__(self, base_url: str, tenancy: str, username: str, password: str, proxy: str):
    self.base_url = base_url.rstrip("/")
    self.tenancy = tenancy

    self.session = requests.Session()
    self.session.timeout = 20
    self.session.headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
    }

    if proxy:
      self.session.proxies.update({"http": proxy.rstrip("/"), "https": proxy.rstrip("/")})
    url = self.base_url + "/api/Account/Authenticate"
    data = {
      "tenancyName": tenancy,
      "usernameOrEmailAddress": username,
      "password": password,
    }
    response = self.session.post(url, json=data)
    if response.ok:
      # Add token to auth header.
      token = response.json()["result"]
      self.session.headers["Authorization"] = f"Bearer {token}"
    else:
      logging.error(f"Response code: {response.status_code}")
      sys.exit(f"Failed to connect to {base_url} with provided credentials.")

  def startJob(self, release_key: str, robot: str, machine: str, arguments: str, folder: str=None, orgId: str=None):
    url = self.base_url + "/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"
    if folder:
      headers = {"X-UIPATH-FolderPath": folder}
    else:
      headers = {"X-UIPATH-OrganizationUnitId": orgId}
    data = {
      "startInfo": {
        "ReleaseKey": release_key,
        "JobsCount": 1,
        "JobPriority": "Normal",
        "Strategy": "ModernJobsCount",
        "ResumeOnSameContext": False,
        "RuntimeType": "Unattended",
        "InputArguments": arguments,
        "MachineRobots": [{
          "RobotUserName": robot,
          "MachineName": machine
        }]
      }
    }
    logging.debug(data)
    response = self.session.post(url, headers=headers, json=data)
    if not response.ok:
      logging.error(f"Response code: {response.status_code}")
      logging.error(response.text)
      sys.exit("Failed to start job")
    return response.json()

uipath = UiPath(base_url, tenancy, username, password, proxy)
response = uipath.startJob(release_key, robot, machine, arguments, folder, orgId)
logging.debug(response)