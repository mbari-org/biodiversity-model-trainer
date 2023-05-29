import time

import click as click
from pathlib import Path

from bio import __version__
from bio.db.tator import init_api, download_data, find_project
from bio.logger import create_logger_file, info, err

# Default values
# The base directory is the same directory as this file
DEFAULT_BASE_DIR = Path(__file__).parent.as_posix()

DEFAULT_VERSION = 'Baseline'
DEFAULT_PROJECT = '901103-biodiversity'


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(
    __version__,
    '-V', '--version',
    message=f'%(prog)s, version %(version)s'
)
def cli():
    """
    Utilities to download data and train models for the 901103 BioDiversity Project.
    """
    pass


@cli.command(name="download", help='Download a dataset for training')
@click.option('--base-dir', default=DEFAULT_BASE_DIR, help='Base directory to save all data to.')
@click.option('--version', default=DEFAULT_VERSION, help='Dataset version to download.')
@click.option('--generator', default='vars-labelbot', help='Generator name, e.g. vars-labelbot or vars-annotation')
def download(base_dir: str, version: str, generator: str):
    create_logger_file(Path.cwd(), 'download')
    base_path = Path(base_dir)
    base_path.mkdir(exist_ok=True)

    # Connect to the database api
    api = init_api()

    # Find the project
    project = find_project(api, DEFAULT_PROJECT)
    info(f'Found project id: {project.name} for project {DEFAULT_PROJECT}')

    # Download a dataset by its version. The versioining isn't currently fully wired in, but included for future use.
    info(f'Downloading dataset {version}')
    data_path = base_path / version
    data_path.mkdir(exist_ok=True)
    download_data(api, project.id, version, generator, data_path)


if __name__ == '__main__':
    try:
        from dotenv import load_dotenv

        load_dotenv('.env')
        start_time = time.time()
        cli()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Done. Elapsed time: {elapsed_time}')
    except Exception as e:
        err(f'Exiting. Error: {e}')
        exit(-1)
