from zipfile import ZipFile, ZIP_DEFLATED
from os import path
import subprocess
from typing import List
import pathlib


def unzipFile(zip_file: str) -> str:
    """ Zipファイルを同一ディレクトリに解凍する
    Args:
        zip_file (str): zipファイル

    Raises:
        Exception: ファイルが存在しない

    Returns:
        str: 解凍ディレクトリ
    """
    if path.isfile(zip_file) is False:
        raise Exception(f'Not Exist zip file. zip_file={zip_file}')
    f_dir = path.dirname(zip_file)
    with ZipFile(zip_file, 'r') as unzip:
        unzip.extractall(f_dir)
    return f_dir


def zipFile(zip_file: str, source_files: List[str]) -> str:
    """ファイルをzip圧縮する

    Args:
        zip_file (str): 圧縮するzip
        source_files (List[str]): 圧縮対象ファイルリスト

    Returns:
        _type_: 圧縮するファイルパス
    """
    with ZipFile(zip_file, 'w', compression=ZIP_DEFLATED) as zf:
        for file in source_files:
            zf.write(file, path.basename(file))
    return zip_file


def wccount(filename) -> int:
    output = subprocess.check_output(
        ['wc', '-l', filename]).decode().split()[0]
    return int(output)


def change_extension(filename, extension) -> str:
    # ファイル名(拡張子除く)を得る
    st = pathlib.PurePath(filename).stem
    dirname = path.dirname(filename)
    return f'{dirname}/{st}.{extension}'
