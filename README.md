# Hydra &ndash; quite simple example

This example uses composition of configs, but not dynamic schemes, which is a bit more advanced.
I think this composition feature already makes it a bit nicer to use than GuildAI.

As always with Hydra
- you can put your flag values into YAML files
- all flags can be overridden on the commandline
- you can use _multirun_ to try out multiple values for the flags

## Table of contents

- [Structure of this repository](#structure-of-this-repository)
- [Example runs](#example-runs)

## Structure of this repository

```
.
├── LICENSE
├── README.md
├── conf
│   ├── data
│   │   ├── adult.yaml
│   │   └── cmnist.yaml
│   ├── hydra.yaml
│   ├── misc
│   │   └── default.yaml
│   └── model
│       ├── deep.yaml
│       └── shallow.yaml
├── run.py
└── utils.py

```

## Example runs

With defaults
```
$ python run.py
Using the adult dataset.
Starting W&B.
==========================
All args as dictionary:
{'data.dataset': <DS.adult: 1>, 'data.directory': './data', 'data.pcnt': 1.0, 'model.depth': 2, 'model.hidden_dims': 30, 'model.lr': 0.001, 'misc.output_dir': './experiments', 'misc.use_wandb': True}
```

Specify a set of flags (defined in `conf/model/deep.yaml`)
```
$ python run.py model=deep
Using the adult dataset.
Starting W&B.
==========================
All args as dictionary:
{'data.dataset': <DS.adult: 1>, 'data.directory': './data', 'data.pcnt': 1.0, 'model.depth': 100, 'model.hidden_dims': 30, 'model.lr': 0.0001, 'misc.output_dir': './experiments', 'misc.use_wandb': True}
```

Specify multiple sets of flags
```
$ python run.py model=deep data=cmnist
Using CMNIST.
Starting W&B.
==========================
All args as dictionary:
{'data.dataset': <DS.cmnist: 2>, 'data.directory': './data', 'data.pcnt': 1.0, 'model.depth': 100, 'model.hidden_dims': 30, 'model.lr': 0.0001, 'misc.output_dir': './experiments', 'misc.use_wandb': True}
```

Overriding a flag value
```
$ python run.py model=deep data=cmnist model.depth=42
Using CMNIST.
Starting W&B.
==========================
All args as dictionary:
{'data.dataset': <DS.cmnist: 2>, 'data.directory': './data', 'data.pcnt': 1.0, 'model.depth': 42, 'model.hidden_dims': 30, 'model.lr': 0.0001, 'misc.output_dir': './experiments', 'misc.use_wandb': True}
```

Multirun! (triggered by the `-m` argument)
```
$ python run.py -m model=deep data=cmnist model.depth=42,65
[2020-11-11 19:26:05,238][HYDRA] Launching 2 jobs locally
[2020-11-11 19:26:05,238][HYDRA] 	#0 : model=deep data=cmnist model.depth=42
Using CMNIST.
Starting W&B.
==========================
All args as dictionary:
{'data.dataset': <DS.cmnist: 2>, 'data.directory': './data', 'data.pcnt': 1.0, 'model.depth': 42, 'model.hidden_dims': 30, 'model.lr': 0.0001, 'misc.output_dir': './experiments', 'misc.use_wandb': True}
[2020-11-11 19:26:05,460][HYDRA] 	#1 : model=deep data=cmnist model.depth=65
Using CMNIST.
Starting W&B.
==========================
All args as dictionary:
{'data.dataset': <DS.cmnist: 2>, 'data.directory': './data', 'data.pcnt': 1.0, 'model.depth': 65, 'model.hidden_dims': 30, 'model.lr': 0.0001, 'misc.output_dir': './experiments', 'misc.use_wandb': True}
```
