from direct.distributed.PyDatagram import PyDatagram
import pytest
from direct.distributed.PyDatagramIterator import PyDatagramIterator


# def test_datagram_minimal():
#     text = "Just Some string"

#     datagram = PyDatagram()
#     datagram.addString(text)

#     iterator = PyDatagramIterator(datagram)
#     assert iterator.getString() == text
