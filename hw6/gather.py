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
    Is used to replacing files from current folder according to file extension.
    :param base_path: given directory
    :param element_path: current directory
    :return: None
    """
    file_name = normalize(element_path.stem)
    folder_name = EXTENSIONS.get(
        get_extensions(element_path.suffix[1:]), 'unknown'
    )
    folder_to = base_path.joinpath(folder_name)
    await folder_to.mkdir(exist_ok=True)

    if folder_name == 'archives':

        try:
            await aioshutil.unpack_archive(element_path, folder_to.joinpath(file_name))
            await element_path.unlink()  # To delete archive
        except OSError as e:
            logging.error(e)

    else:
        file_name += element_path.suffix
        await element_path.replace(folder_to.joinpath(file_name))


def get_extensions(extension: str) -> tuple:
    """
    Is used to get tuple keys using one extension. \n
    :param extension: is file extensions
    """
    for key in EXTENSIONS:
        if extension.upper() in key:
            return key


async def get_folders(base_path: AsyncPath, current_path: AsyncPath = None) -> None:
    """
    Is used to get all folders which must be traversed. \n
    :param base_path: base directory
    :param current_path: current directory
    :return: None
    """
    if current_path is None:
        current_path = base_path
        folders.append(current_path)

    async for element in current_path.iterdir():

        if await element.is_dir() and element not in EXTENSIONS.values():
            folders.append(element)
            await get_folders(base_path=base_path, current_path=element)


async def iterfolder(base_path: AsyncPath, current_path: AsyncPath) -> None:
    """
    Is used to traverse directory. \n
    :param base_path: base directory
    :param current_path: current directory path
    :return: None
    """
    start_time = perf_counter()  # For time measuring
    logging.debug(f"started with args: {current_path}")

    async for element in current_path.iterdir():

        if await element.is_file():
            await file_replacement(base_path=base_path, element_path=element)

    logging.debug(f'done with args: {current_path} in {perf_counter() - start_time}')


async def main() -> None:
    """
    Main loop function. \n
    :return: None
    """
    base_path = AsyncPath(source)

    logging.info('Getting folders...')
    await get_folders(base_path)
    logging.info('Folders got.')

    logging.info(f'Sorting {base_path} ...')
    tasks = [iterfolder(base_path=base_path, current_path=folder) for folder in folders]
    await asyncio.gather(*tasks)

    logging.info('Removing empty folders...')
    await remove_empty_folders(base_path)
    logging.info('Empty folders removed.')


async def remove_empty_folders(base_path: AsyncPath) -> None:
    """
    Is used to remove all empty folders
    :param base_path: given directory
    :return: None
    """
    async for element in base_path.iterdir():
        if element.name not in EXTENSIONS.values() and await element.is_dir():
            await aioshutil.rmtree(element)


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(funcName)s %(message)s',
    )

    folders = []
    start_time = perf_counter()
    asyncio.run(main())
    logging.info(f"Sorted done in {perf_counter() - start_time}sec")
