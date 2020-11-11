"""Entry point."""
from dataclasses import dataclass
from enum import Enum

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, OmegaConf

from utils import flatten


DS = Enum("DS", ["adult", "cmnist"])  # use Enum instead of Literal

# We split the configuration into multiple subconfigs which you expect to configure separately.
# So, for example, for one dataset configuration, you might try out several model configurations.
# You have to decide which division of configs makes sense.
# Each dataclass here gets its own config files.
@dataclass
class DatasetConfig:
    dataset: DS = MISSING  # `MISSING` is a special value indicating it has to be specified in yaml
    directory: str = "./data"  # you can also specify defaults here, but do it only sparingly
    pcnt: float = 1.0


@dataclass
class ModelConfig:
    depth: int = MISSING
    hidden_dims: int = MISSING
    lr: float = MISSING


@dataclass
class MiscConfig:  # flags that didn't fit in any of the other categories
    output_dir: str = MISSING
    seed: int = MISSING
    use_wandb: bool = MISSING


# ====================================== base config schema =======================================
@dataclass
class Config:  # base config schema
    data: DatasetConfig = MISSING  # put config files for this into `conf/data/`
    model: ModelConfig = MISSING  # put config files for this into `conf/model/`
    misc: MiscConfig = MISSING  # put config files for this into `conf/other/`


# register `Config` to be the schema for the main config
cs = ConfigStore.instance()
cs.store(name="hydra", node=Config)  # we register the schema for the file "hydra.yaml"


@hydra.main(config_name="hydra", config_path="conf")  # specify "hydra.yaml" as the main config file
def main(cfg: Config) -> None:
    """Main function."""
    data_cfg = cfg.data
    if data_cfg.dataset == DS.adult:
        print("Using the adult dataset.")
    elif data_cfg.dataset == DS.cmnist:
        print("Using CMNIST.")

    if cfg.misc.use_wandb:
        print("Starting W&B.")

    args_as_dict = flatten(OmegaConf.to_container(cfg, resolve=True))  # convert to dictionary
    print("==========================\nAll args as dictionary:")
    print(args_as_dict)


if __name__ == "__main__":
    main()
