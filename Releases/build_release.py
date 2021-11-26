import config
import os
import logging
import release
import shutil
import subprocess
import tempfile


def make_7zip_archive(release_name: str, version: str, root_dir: os.PathLike,
                      release_dir: os.PathLike) -> os.PathLike:
    archive_name = "{} {}.7z".format(release_name, version)
    # Remove whitespaces from archive name because GitHub doesn't like them
    archive_name = "_".join(archive_name.split())
    src = os.path.join(root_dir, "*")
    dst = os.path.join(release_dir, archive_name)
    if os.path.isfile(dst):
        os.remove(dst)
    cmd = ["7z", "a", "-m0=LZMA2:d64m:fb64", "-ms=4g", "-mmt=12", "-mx=9",
           dst, src]
    sp = subprocess.run(cmd, stdout=subprocess.DEVNULL)
    sp.check_returncode()


def copy_and_check_plugins(src: os.PathLike, dst: os.PathLike, version: str):
    plugins = release.find_plugins(src)
    plugins_full_path = [os.path.join(src, plugin) for plugin in plugins]
    release.check_version(plugins_full_path, version)
    for plugin in plugins:
        src_path = os.path.join(src, plugin)
        dst_path = os.path.join(dst, plugin)
        shutil.copy2(src_path, dst_path)
        modgroups = "{}.modgroups".format(os.path.splitext(plugin)[0])
        src_path = os.path.join(src, modgroups)
        dst_path = os.path.join(dst, modgroups)
        shutil.copy2(src_path, dst_path)


def build_oldrim_1k(release_name: str, version: str):
    with tempfile.TemporaryDirectory() as dir_temp:
        src = os.path.join(config.DIR_REPO, "Meshes - Oldrim")
        dst = os.path.join(dir_temp, "Meshes")
        shutil.copytree(src, dst)
        src = os.path.join(config.DIR_REPO, "Textures - 1K")
        dst = os.path.join(dir_temp, "Textures")
        shutil.copytree(src, dst)
        dir_plugin = os.path.join(config.DIR_REPO, "Plugin - Oldrim")
        bsa_name = release.find_bsa_name(dir_plugin)
        src = dir_temp
        dst = os.path.join(dir_temp, bsa_name)
        release.build_bsa(src, dst, config.BSARCH, "tes5", True)
        copy_and_check_plugins(dir_plugin, dir_temp, version)
        dir_release = os.path.join(config.DIR_REPO, "Releases", "Oldrim")
        make_7zip_archive(release_name, version, dir_temp, dir_release)


def build_oldrim_2k(release_name: str, version: str):
    with tempfile.TemporaryDirectory() as dir_temp:
        src = os.path.join(config.DIR_REPO, "Meshes - Oldrim")
        dst = os.path.join(dir_temp, "Meshes")
        shutil.copytree(src, dst)
        src = os.path.join(config.DIR_REPO, "Textures - 2K")
        dst = os.path.join(dir_temp, "Textures")
        shutil.copytree(src, dst)
        dir_plugin = os.path.join(config.DIR_REPO, "Plugin - Oldrim")
        bsa_name = release.find_bsa_name(dir_plugin)
        src = dir_temp
        dst = os.path.join(dir_temp, bsa_name)
        release.build_bsa(src, dst, config.BSARCH, "tes5", True)
        copy_and_check_plugins(dir_plugin, dir_temp, version)
        dir_release = os.path.join(config.DIR_REPO, "Releases", "Oldrim")
        make_7zip_archive(release_name, version, dir_temp, dir_release)


def build_sse_1k(release_name: str, version: str):
    with tempfile.TemporaryDirectory() as dir_temp:
        src = os.path.join(config.DIR_REPO, "Meshes - SSE")
        dst = os.path.join(dir_temp, "Meshes")
        shutil.copytree(src, dst)
        src = os.path.join(config.DIR_REPO, "Textures - 1K")
        dst = os.path.join(dir_temp, "Textures")
        shutil.copytree(src, dst)
        dir_plugin = os.path.join(config.DIR_REPO, "Plugin - SSE")
        bsa_name = release.find_bsa_name(dir_plugin)
        src = dir_temp
        dst = os.path.join(dir_temp, bsa_name)
        release.build_bsa(src, dst, config.BSARCH, "sse", True)
        copy_and_check_plugins(dir_plugin, dir_temp, version)
        dir_release = os.path.join(config.DIR_REPO, "Releases", "SSE")
        make_7zip_archive(release_name, version, dir_temp, dir_release)


def build_sse_2k(release_name: str, version: str):
    with tempfile.TemporaryDirectory() as dir_temp:
        src = os.path.join(config.DIR_REPO, "Meshes - SSE")
        dst = os.path.join(dir_temp, "Meshes")
        shutil.copytree(src, dst)
        src = os.path.join(config.DIR_REPO, "Textures - 2K")
        dst = os.path.join(dir_temp, "Textures")
        shutil.copytree(src, dst)
        dir_plugin = os.path.join(config.DIR_REPO, "Plugin - SSE")
        bsa_name = release.find_bsa_name(dir_plugin)
        src = dir_temp
        dst = os.path.join(dir_temp, bsa_name)
        release.build_bsa(src, dst, config.BSARCH, "sse", True)
        copy_and_check_plugins(dir_plugin, dir_temp, version)
        dir_release = os.path.join(config.DIR_REPO, "Releases", "SSE")
        make_7zip_archive(release_name, version, dir_temp, dir_release)


logger = logging.getLogger(release.__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler = logging.FileHandler("{}.log".format(release.__name__), "w")
handler.setFormatter(formatter)
logger.addHandler(handler)
try:
    build_oldrim_1k("{} 1K".format(config.MOD_NAME), config.MOD_VERSION)
    build_oldrim_2k("{} 2K".format(config.MOD_NAME), config.MOD_VERSION)
    build_sse_1k("{} 1K".format(config.MOD_NAME), config.MOD_VERSION)
    build_sse_2k("{} 2K".format(config.MOD_NAME), config.MOD_VERSION)
    logger.info("Succesfully built release archives for {} v{}".
                format(config.MOD_NAME, config.MOD_VERSION))
except Exception as error:
    logger.exception(error)
