from server.core.helpers import getNetworkIp


def test_get_network_address():
    address = getNetworkIp()
    assert isinstance(address, str)
    assert address == "127.0.0.1"
