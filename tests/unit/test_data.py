from coser.common.services.CoserService import CoserService
from coser.common.configuration.config import load_config

def test_read_data_csv():
    config=load_config()
    service=CoserService(config.get("coser-service"))
    df=service.get_dataset_from_local()
    print(df.head())
    print(df.columns)
    assert not df.empty


def test_read_dataset():
    config=load_config()
    service=CoserService(config.get("coser-service"))
    dataset=service.get_dataset_from_hf()
    print(dataset)
    assert dataset