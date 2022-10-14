from pathlib import Path
import shutil
from typing import Union
from threading import Thread, RLock

from normalization import normalize
from logger import logged


FILES_EXTENSIONS = {
    ("JPEG", "PNG", "JPG", "SVG"): "images",
    ("AVI", "MP4", "MOV", "MKV"): "videos",
    ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"): "documents",
    ("MP3", "OGG", "WAV", "AMR"): "audio",
    ("ZIP", "GZ", "TAR"): "archives",
    "": 'unknown'
}

LOCK = RLock()


def create_folders(base_path: Path) -> None:
    """
    Is used to create desired folders according to categories
    :param base_path: path to be sorted
    :return: None
    """
    for folder_name in FILES_EXTENSIONS.values():
        folder_path = base_path.joinpath(folder_name)
        folder_path.mkdir(exist_ok=True)


def delete_folders(base_path: Path) -> None:
    """
    Is used to delete extra folders after sorting
    :param base_path: path to be sorted
    :return: None
    """
    for folder in base_path.iterdir():
        if folder.name not in FILES_EXTENSIONS.values() and folder.is_dir():
            shutil.rmtree(folder)


@logged
def file_replacement(lock: RLock, base_path: Path, file: Path) -> None:
    """
    This function is started in new thread
    :param lock: is used to lock thread until file will be replaced
    :param base_path: base directory path
    :param file: file path
    :return: None
    """
    lock.acquire()
    file_name = normalize(file.stem)  # Cyrillic -> latin
    folder_name = FILES_EXTENSIONS.get(
        get_extensions(file.suffix[1:]), 'unknown')
    folder_to = base_path.joinpath(folder_name)

    if folder_name == 'archives':
        shutil.unpack_archive(file, folder_to.joinpath(file_name))
        file.unlink()
    else:
        file_name += file.suffix
        file.replace(folder_to.joinpath(file_name))
    lock.release()


def get_extensions(extension: str) -> Union[tuple, str]:
    """
    Is used to get tuple keys using one extension
    :param extension: is file extensions
    """
    for key in FILES_EXTENSIONS:
        if extension.upper() in key:
            return key


@logged
def iterdir(base_path: Path, path: Path) -> None:
    """
    This function is starting new thread for iterating directory
    :param base_path: base directory
    :param path: current directory
    :return: None
    """
    for elem in path.iterdir():

        if elem.is_file():
            Thread(target=file_replacement, args=(LOCK, base_path, elem)).start()
        else:
            parse_folder(elem, base_path)


@logged
def parse_folder(path: Path, base_path: Path = None) -> None:
    """
    Is used to recursive parsing
    :param path: is current directory path
    :param base_path: given path entered by user
    :return: None
    """

    if base_path is None:
        base_path = path

    if path.is_dir():
        Thread(target=iterdir, args=(base_path, path)).start()


@logged
def sorter(user_input: list[str]) -> str:
    """
    Sorting files according to following folders\n
    images: JPEG, PNG, JPG, SVG\n
    videos: AVI, MP4, MOV, MKV\n
    documents: DOC, DOCX, TXT, PDF, XLSX, PPTX\n
    audio: MP3, OGG, WAV, AMR\n
    archives: ZIP, GZ, TAR\n
    :param user_input: path in OS which must be sorted
    :return:
    """
    if len(user_input) < 1:

        print("No path was given")
        user_path = ""

    else:
        user_path = ''.join(user_input)

    path = Path(user_path)
    if path.exists():
        if not path.is_file():
            create_folders(path)

        parse_folder(path)
    else:
        return f"{path.absolute()} does not exist"
    delete_folders(path)

    return f"Given path {path.absolute()} has been sorted"
