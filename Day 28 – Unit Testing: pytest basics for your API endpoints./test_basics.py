def add(a,b):
    return a+b
def test_add():
    result=add(2,3)
    assert result==5
    print("Test Passed!")
def test_add_negative():
    result=add(-1,1)
    assert result==0
    print("Test Passed -ve Number!")