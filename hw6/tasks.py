import argparse
import asyncio
import logging
from time import perf_counter

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


async def file_replacement(base_path: AsyncPath, element_path: AsyncPath = None) -> None:
    """

    :param base_path: given directory
    :param element_path: current directory
    :return: None
    """
    logging.debug(f"Starting file replacement with args: {element_path}")
    file_name = normalize(element_path.stem)
    folder_name = EXTENSIONS.get(
        get_extensions(element_path.suffix[1:]), 'unknown'
    )
    folder_to = base_path.joinpath(folder_name)
    await folder_to.mkdir(exist_ok=True)

    if folder_name == 'archives':

        await aioshutil.unpack_archive(element_path, folder_to.joinpath(file_name))
        await element_path.unlink()  # To delete archive

    else:
        file_name += element_path.suffix
        await element_path.replace(folder_to.joinpath(file_name))

    logging.debug(f"replaced {element_path}")


def get_extensions(extension: str) -> tuple:
    """
    Is used to get tuple keys using one extension. \n
    :param extension: is file extensions
    """
    for key in EXTENSIONS:
        if extension.upper() in key:
            return key


async def get_folders(base_path: AsyncPath, current_path: AsyncPath = None) -> None:

    if current_path is None:
        current_path = base_path
        await asyncio.create_task(
            iterfolder(base_path=base_path, current_path=current_path)
        )

    async for element in current_path.iterdir():
        if await element.is_dir() and element not in EXTENSIONS.values():

            await asyncio.create_task(
                iterfolder(base_path=base_path, current_path=element)
            )
            await get_folders(base_path=base_path, current_path=element)


async def iterfolder(base_path: AsyncPath, current_path: AsyncPath = None):
    """
    Is used to iterate recursively with creating new coroutines for iterating each folder
    :param queue:
    :param base_path: base directory
    :param current_path: current directory path
    :return: None
    """
    start_time = perf_counter()  # For time measuring
    if current_path is None:
        current_path = base_path

    logging.debug(f"started with args: {current_path}")

    async for element in current_path.iterdir():

        if await element.is_file():
            await file_replacement(base_path=base_path, element_path=element)

    logging.debug(f'done with args: {current_path} in {perf_counter() - start_time}')


async def main():

    base_path = AsyncPath(source)

    logging.info('Getting folders...')
    await get_folders(base_path)
    logging.info('Folders got')

    logging.info('Removing empty folders...')
    await remove_empty_folders(base_path)
    logging.info('Empty folders removed')


async def remove_empty_folders(base_path: AsyncPath) -> None:
    """
    Is used to remove all empty folders
    :param base_path: given directory
    :return: None
    """
    async for element in base_path.iterdir():
        if element.name not in EXTENSIONS.values() and await element.is_dir():
            await aioshutil.rmtree(path=element, ignore_errors=True)


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(funcName)s %(message)s',
    )

    start_time = perf_counter()
    asyncio.run(main())
    logging.info(f"all sorting done in {perf_counter() - start_time}sec")
