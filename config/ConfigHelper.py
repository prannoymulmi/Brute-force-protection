import json
import os
from pathlib import Path
from typing import Dict


def get_config() -> Dict:
    # read config json file to get the values
    with open(str(Path(
            __file__).parent.parent) + os.sep + "config" + os.sep + "config.json",
              'r') as fp:
        return json.load(fp)
