import config
import os
import logging
import release
import shutil
import tempfile


def build_dev(release_name: str, version: str):
    with tempfile.TemporaryDirectory() as dir_temp:
        src = os.path.join(config.DIR_REPO, "Meshes - Oldrim")
        dst = os.path.join(dir_temp, "Meshes")
        shutil.copytree(src, dst)
        src = os.path.join(config.DIR_REPO, "Textures - 1K")
        dst = os.path.join(dir_temp, "Textures")
        shutil.copytree(src, dst)
        src = os.path.join(config.DIR_REPO, "Plugin - Oldrim")
        dst = dir_temp
        shutil.copytree(src, dst, dirs_exist_ok=True)
        dir_release = os.path.join(config.DIR_REPO, "Releases", "Development")
        release.make_archive(release_name, version, dir_temp, dir_release)


logger = logging.getLogger(release.__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler = logging.FileHandler("{}.log".format(release.__name__), "w")
handler.setFormatter(formatter)
logger.addHandler(handler)
try:
    build_dev(config.MOD_NAME, config.MOD_VERSION)
except Exception as error:
    logger.exception(error)
