import argparse
import asyncio
import logging
from time import perf_counter
from typing import Union

from aiopath import AsyncPath
import aioshutil

from normalization import normalize


EXTENSIONS = {
    ("JPEG", "PNG", "JPG", "SVG"): "images",
    ("AVI", "MP4", "MOV", "MKV"): "videos",
    ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"): "documents",
    ("MP3", "OGG", "WAV", "AMR"): "audio",
    ("ZIP", "GZ", "TAR"): "archives",
    "": 'unknown'
}

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("--source", "-s", help="Source folder", required=True)

args = vars(parser.parse_args())

source = args.get("source")


async def create_folders(base_path: AsyncPath) -> None:
    """
    Creating folders according to types. \n
    :param base_path: given directory
    :return: None
    """
    [await base_path.joinpath(folder).mkdir(exist_ok=True) for folder in EXTENSIONS.values()]
    logging.debug('folders created')


def get_extensions(extension: str) -> Union[tuple, str]:
    """
    Is used to get tuple keys using one extension. \n
    :param extension: is file extensions
    """
    for key in EXTENSIONS:
        if extension.upper() in key:
            return key


async def file_replacement(base_path: AsyncPath, element_path: AsyncPath = None) -> None:
    """

    :param base_path: given directory
    :param element_path: current directory
    :return: None
    """
    # logging.debug(f"Starting file replacement with args: {element_path}")
    file_name = normalize(element_path.stem)
    folder_name = EXTENSIONS.get(
        get_extensions(element_path.suffix[1:]), 'unknown'
    )
    folder_to = base_path.joinpath(folder_name)
    # logging.debug(f"replacing {element_path}")
    if folder_name == 'archives':

        await aioshutil.unpack_archive(element_path, folder_to.joinpath(file_name))
        await element_path.unlink()  # To delete archive

    else:
        file_name += element_path.suffix
        await element_path.replace(folder_to.joinpath(file_name))
    # logging.debug(f"replaced {element_path}")


async def iterfolder(base_path: AsyncPath, current_path: AsyncPath = None):
    """
    Is used to iterate recursively with creating new coroutines for iterating each folder
    :param base_path: base directory
    :param current_path: current directory path
    :return: None
    """
    start_time = perf_counter()  # For time measuring

    if current_path is None:
        current_path: AsyncPath = base_path

    logging.debug(f"started with args: {current_path}")

    async for element in current_path.iterdir():

        if await element.is_file():
            replace_task = asyncio.create_task(file_replacement(base_path=base_path, element_path=element))
            tasks.add(replace_task)
            await replace_task
            replace_task.add_done_callback(tasks.discard)
        else:

            if element.name not in EXTENSIONS.values():  # To do not iterate over existing base folders
                iter_task = asyncio.create_task(iterfolder(base_path=base_path, current_path=element))
                tasks.add(iter_task)
                await iter_task
                iter_task.add_done_callback(tasks.discard)

    else:

        if current_path != base_path:  # To delete empty folder when tail reached
            try:
                await current_path.rmdir()
                logging.debug(f"Empty folder {current_path} deleted")
            except OSError as e:
                logging.error(e)
        logging.debug(f"done with args: {current_path} in {perf_counter() - start_time}secs")


async def main(base_path: AsyncPath):
    await create_folders(base_path=base_path)  # To create folders before sorting
    await asyncio.gather(*tasks)  # Start folder sorting operation


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(funcName)s %(message)s',
    )

    base_path = AsyncPath(source)
    tasks = set()
    tasks.add(iterfolder(base_path=base_path))
    start_time = perf_counter()
    asyncio.run(main(base_path), debug=True)
    logging.debug(f"Done in {perf_counter() - start_time}sec")
