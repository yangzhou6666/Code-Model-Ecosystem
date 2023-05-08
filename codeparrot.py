'''play with codeparrot model'''
from tqdm import tqdm
from datasets import load_dataset
import os
from tqdm import tqdm
import logging
import hashlib

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_and_save_data(data_name, cache_dir=None, data_dir=None, split='train'):
    logger.info("Downloading/Reusing data {} from {}".format(data_name, cache_dir))

    if data_dir:
        ds = load_dataset(data_name, split=split, cache_dir=cache_dir)
    else:
        ds = load_dataset(data_name, data_dir=data_dir, split=split, cache_dir=cache_dir)

    return ds


if __name__ == '__main__':
    cache_dir = "./.data_cache" # Set your own cache directory here

    download_and_save_data(
        data_name="codeparrot/codeparrot-clean",
        cache_dir=cache_dir,
        split="train",
    )

    download_and_save_data(
        data_name="transformersbook/codeparrot",
        cache_dir=cache_dir,
        split="train",
    )
