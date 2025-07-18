import socket


def validate_ip_address(ip_address):
    """
   Validate an IP address.

    Args:
        ip_address (str): A string containing an IP address.

    Returns:
        str: The IP address if valid, None if invalid.
    """

    ip_valid = False
    ip_address = ip_address.strip() if ip_address else None
    if ip_address:
        try:
            socket.inet_aton(ip_address)
            ip_valid = True
        except socket.error:
            ip_valid = False

    return ip_address if ip_valid else None
