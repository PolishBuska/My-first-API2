import pytest
from app.calculations import add, multiply,subtract,divide

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 100, 107),
    (123, 2, 125)
])
def test_add(num1,num2,expected): # naming of a function matters it should be test_something
    print("testing add function")
    assert add(num1, num2) == expected



