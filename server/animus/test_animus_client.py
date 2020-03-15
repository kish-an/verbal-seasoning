from . import animus_py3 as animus
import logging

def test_version():
    verStr = animus.version()
    assert type(verStr) is str
    assert len(verStr) > 0