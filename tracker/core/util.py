

def validate_ip_address(ip_address):
    """
   Validate an IP address.

    Args:
        ip_address (str): A string containing an IP address.

    Returns:
        str: The IP address if valid, None if invalid.
    """

    import socket

    ip_valid = False
    ip_address = ip_address.strip() if ip_address else None
    if ip_address:
        try:
            socket.inet_aton(ip_address)
            ip_valid = True
        except socket.error:
            ip_valid = False

    return ip_address if ip_valid else None


def timed_function(func):
    """
    Decorator to time a function's execution duration.

    Args:
        func (function): The function to be timed.

    Returns:
        function: The wrapped function with timing.
    """
    import time
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Function '{func.__name__}' executed in {duration:.4f} seconds.")
        return result

    return wrapper
