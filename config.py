"""
Config file
Configures project and default datasets and directory
"""


from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS_REPORTS = PROJECT_ROOT / "outputs" / "reports"
OUTPUTS_PLOTS = PROJECT_ROOT / "outputs" / "plots"
DATABASE_PATH = PROJECT_ROOT / "data" / "pipeline.db"


for directory in [DATA_RAW, DATA_PROCESSED, OUTPUTS_REPORTS, OUTPUTS_PLOTS]:
    directory.mkdir(parents=True, exist_ok=True)

#Default Dataset used. You can add or remove to your liking.
DEFAULT_DATASETS = {
    'titanic': 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv',
    'iris': 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
}

#Default cleaning parameters. Modify to your liking.
DEFAULT_CLEANING = {
    'remove_duplicates': True,
    'strip_columns': True,
    'handle_numeric_na': 'median',
    'handle_categorical_na': 'mode'
}