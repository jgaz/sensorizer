import logging

from analysis.changepoint import remove_small_splits


class TestChangepoint:

    def test_remove_small_splits(self):
        splits = [1, 3, 5, 8, 15, 20, 30]
        result = remove_small_splits(0.9, splits)
        assert len(result) == 5
        assert result[0][0] == (3, 5)

        splits = [1, 100]
        result = remove_small_splits(0.9, splits)
        assert len(result) == 1
        assert result[0][0] == (1, 100)

        splits = list(range(12))
        result = remove_small_splits(0.89, splits)
        assert len(result) == 10
        logging.error(result)

