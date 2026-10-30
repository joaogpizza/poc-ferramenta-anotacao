import pytest
from logica_anotacao import formato_anotacao

def test_formato_anotacao_success():
    result = formato_anotacao("tumor", 100, 200)
    assert result["label"] == "tumor"
    assert result["coordinates"]["x"] == 100

def test_formato_anotacao_empty_label():
    with pytest.raises(ValueError):
        formato_anotacao("", 100, 200)