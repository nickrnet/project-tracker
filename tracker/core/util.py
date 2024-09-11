import socket


def validate_ip_address(ip_address):
    """
    Get the sournce IP address of the request.

    Args:
        request (HTTPRequest): An HTTPRequest object.

    Returns:
        str: A string representation of the IP address.
    """

    if ip_address:
        try:
            socket.inet_aton(ip_address)
            ip_valid = True
        except socket.error:
            ip_valid = False

    return ip_address if ip_valid else None
