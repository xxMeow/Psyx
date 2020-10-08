# PsyxKU

- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [How to Update](#how-to-update)
- [Versions](#versions)

## Technology Stack

**Frontend** HTML / JavaScript / JQuery / CSS

**Backend** Nginx / Python3.8 / Flask / Gunicorn / MySQL

**System** Ubuntu20.04LTS / GIT / Supervisor / Fail2Ban

## Project Structure

- `[SYNC]` should be manually copy&paste to keep them same
- `[LINK]` has been linked to other place
- `[AUTO]` auto generated file

```
Psyx
├── config
│   ├── jail_ci.local   # [SYNC] Fail2Band Configuration
│   ├── nginx_ci.conf   # [SYNC] Nginx Configuration
│   ├── psyx.conf       # [LINK] Supervisor Configuration
│   └── service.ini     # Project Configuration File
├── html
│   ├── assets/...
│   ├── js/...
│   ├── css/...
│   ├── index.html      # Homepage
│   ├── admin.html      # Admin
│   ├── test.html       # Before Test
│   └── testing.html    # Testing
└── service
    ├── API.py          # Backend APIs
    ├── PsyxDB.py       # Project Configuration & DB Operations
    ├── ResetDB.sql     # DB Reset Script
    └── __pycache__/... # [AUTO]
```

## How to Update

- Update Code

    ```
    $ git pull # don't forget to do [git fetch] first
    ```

- Reload Service

    ```
    $ sudo supervisorctl reload
    ```

- (Always keep `[SYNC]` files being synced so that their changes can be tracked by Git)

## Versions

- ![release](https://img.shields.io/badge/release-v1.0-green.svg) 2020/10/08