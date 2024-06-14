This [Rundeck](https://www.rundeck.com/) plugin adds a _workflow step_ to trigger a job in a [UiPath](https://www.uipath.com/) instance.

# Requirements
- Python 3

Tested in RHEL9 with Python3.11.

# Installation
Install in the usual way, eg following [Rundeck docs](https://docs.rundeck.com/docs/administration/configuration/plugins/installing.html).

Configure in your project or framework properties, eg:
```
framework.plugin.WorkflowStep.uipath-job-start.url = https://myUiPathServer
framework.plugin.WorkflowStep.uipath-job-start.tenancy = myTenancy
framework.plugin.WorkflowStep.uipath-job-start.username = myUiPathUser
framework.plugin.WorkflowStep.uipath-job-start.password_storage_path = keys/myUiPathPassword
```

Optionally a proxy may be set:
```
framework.plugin.WorkflowStep.uipath-job-start.proxy = https://myproxy:8080
```

## Troubleshooting
If your UiPath instance uses SSL and is signed using a CA not included in the Python bundle you may see `certificate verify failed: unable to get local issuer certificate` when trying to connect. If you have saved the CA to your operating system certs you may which to include that path for Python to access. On Linux edit the rundeck user's `.bashrc` file to include the following (example for Red Hat / CentOS):
```
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-bundle.crt
```

# Usage
Add as a step. You'll need to provide the following information:
- Release key
- Folder path or organization ID
- Robot user name
- Robot machine name
- Any input argments (optional)

# Contributing
Issues and pull requests welcome!