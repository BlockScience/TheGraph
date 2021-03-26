# BlockScience collaboration with TheGraph
Delegator Subsystem Model

## Model initially for verifying margin trading system specified in two jointly, related documents:
1.  [Preliminary Math Spec](https://hackmd.io/maG-kkCeRbKOcup5gfxSWg)
2.  [Mechanism Specification](https://hackmd.io/e2K_VzC-TFyC8MDjqHwczA)

## Ongoing work to assess validation of performance under varied ordering scenarios
## Model employs cadCAD simulation framework
```
                  ___________    ____
  ________ __ ___/ / ____/   |  / __ \
 / ___/ __` / __  / /   / /| | / / / /
/ /__/ /_/ / /_/ / /___/ ___ |/ /_/ /
\___/\__,_/\__,_/\____/_/  |_/_____/
by cadCAD                  ver. 0.4.23
======================================
       Complex Adaptive Dynamics       
       o       i        e
       m       d        s
       p       e        i
       u       d        g
       t                n
       e
       r
```
***cadCAD*** is a Python package that assists in the processes of designing, testing and validating complex systems 
through simulation, with support for Monte Carlo methods, A/B testing and parameter sweeping. 

# Getting Started


#### Change Log: [ver. 0.4.23](CHANGELOG.md)

[Previous Stable Release (No Longer Supported)](https://github.com/cadCAD-org/cadCAD/tree/b9cc6b2e4af15d6361d60d6ec059246ab8fbf6da)

## 0. Pre-installation Virtual Environments with [`venv`](https://docs.python.org/3/library/venv.html) (Optional):
If you wish to create an easy to use virtual environment to install cadCAD inside of, please use the built in `venv` package.

***Create** a virtual environment:*
```bash
$ python3 -m venv ~/cadcad
```

***Activate** an existing virtual environment:*
```bash
$ source ~/cadcad/bin/activate
(cadcad) $
```

***Deactivate** virtual environment:*
```bash
(cadcad) $ deactivate
$
```

## 1. Installation: 
Requires [>= Python 3.6](https://www.python.org/downloads/) 

**Option A: Install Using [pip](https://pypi.org/project/cadCAD/)** 
```bash
$ pip3 install cadCAD
```

### cadCAD Specification
Shows the relationship between state variables, mechanisms, actions, and when each is called and/or updated.
