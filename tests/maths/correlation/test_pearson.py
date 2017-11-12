
import numpy as np
import pandas as pd
from pytest import approx
from sklearn.datasets import load_iris

from fastats.maths.correlation import pearson, pearson_matrix


def test_pearson_uwe_normal_hypervent():
    """
    This is a basic sanity test for the Pearson
    correlation function based on the example from
    UWE:
    http://learntech.uwe.ac.uk/da/Default.aspx?pageid=1442
    The correlation between normal and hypervent should
    be 0.966
    """
    normal = np.array([56, 56, 65, 65, 50, 25, 87, 44, 35])
    hypervent = np.array([87, 91, 85, 91, 75, 28, 122, 66, 58])

    result = pearson(normal, hypervent)
    assert result == approx(0.966194346491)

    data = np.stack([normal, hypervent]).T
    output = pearson_matrix(data)
    assert output.shape == (2, 2)
    assert output[0][0] == approx(1)
    assert output[0][1] == approx(0.966194346491)
    assert output[1][0] == approx(0.966194346491)
    assert output[1][1] == approx(1)


def test_pearson_stats_howto():
    """
    This is a basic sanity test for the Pearson
    correlation based on the example from:
    http://www.statisticshowto.com/how-to-compute-pearsons-correlation-coefficients/
    """
    age = np.array([43, 21, 25, 42, 57, 59])
    glucose = np.array([99, 65, 79, 75, 87, 81])

    result = pearson(age, glucose)
    assert result == approx(0.529808901890)

    data = np.stack([age, glucose]).T
    output = pearson_matrix(data)
    assert output.shape == (2, 2)
    assert output[0][0] == approx(1)
    assert output[0][1] == approx(0.529808901890)
    assert output[1][0] == approx(0.529808901890)
    assert output[1][1] == approx(1)


def test_pearson_nan_result():
    x = np.array([1, 2, 3, 4], dtype='float')
    y = np.array([2, 3, 4, 3], dtype='float')

    assert pearson(x, y) == approx(0.6324555320)
    data = np.stack([x, y]).T
    output = pearson_matrix(data)
    assert output.shape == (2, 2)
    assert output[0][0] == approx(1)
    assert output[0][1] == approx(0.6324555320)
    assert output[1][0] == approx(0.6324555320)
    assert output[1][1] == approx(1)

    x[0] = np.nan
    assert np.isnan(pearson(x, y))

    x[0] = 1.0
    y[0] = np.nan
    assert np.isnan(pearson(x, y))

    y[0] = 2.0
    assert pearson(x, y) == approx(0.6324555320)


def test_pearson_matrix():
    data = load_iris().data
    expected = pd.DataFrame(data).corr(method='pearson').values
    output = pearson_matrix(data)
    assert np.allclose(expected, output)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
