import pytest

from vto_pipeline.util.text_utils import process_word_quantity


@pytest.mark.unit
def test_process_word_quantity():
    assert process_word_quantity(5) == 5
    assert process_word_quantity("5") == 5
    assert process_word_quantity("fünf") == 5
    assert process_word_quantity("dreimal") == 3

    with pytest.raises(ValueError):
        process_word_quantity("cheese")
