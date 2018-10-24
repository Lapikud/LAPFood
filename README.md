# LAPFood
Ultimate repository to parse menus around campus!

## How to change branches

When we develop this code we want to setup 3 different branches:
  * develop (purpose of this branch is to write code that is shit and brakes a lot)
  * testing (purpose of this branch is to test our code that kinda works and fix bugs)
  * master  (purpose of this branch is to have code run in live environment)

to create a new branch write `git checkout -b branchname`.

to change branches write `git checkout branchname`.

for example `git checkout develop`

## How to start backend server for personal testing



This program is meant to be started with python3

`python wsgi.py` then access the site at http://localhost:5000

If you have python2 and python3 then write

`python3 wsgi.py`