from main import launch


def test_launch():
    start = "2023-01-01"
    end = "2023-02-01"

    result = launch(start, end)

    assert result
