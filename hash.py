def majuscules(text):
    return text.upper()

def minuscules(text):
    return text.lower()

def test_majuscules():
    assert majuscules('ABcdEfghi') == 'ABCDEFGHI'

def test_minuscules():
    assert minuscules('ABJDsdfh') == 'abjdsfgh'