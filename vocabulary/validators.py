import re,json

def isurl(value):
    """
    Return whether or not given value is an URL.
    If the value is an URL, this function returns ``True``, otherwise ``False``.
    Examples::
        >>> isurl('http://foo.bar#com')
        True
        >>> isurl('http://foobar.c_o_m')
        False
    :param value: string to validate URL
    """
    # Regex patterns for validating URL is taken from
    # Django's URLValidator class

    ul = '\u00a1-\uffff'

    # IP patterns
    ipv4_re = r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'
    ipv6_re = r'\[[0-9a-f:\.]+\]'

    # Host patterns
    hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
    domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
    tld_re = r'\.(?!-)(?:[a-z' + ul + '-]{2,63}|xn--[a-z0-9]{1,59})(?<!-)\.?'  # may have a trailing dot
    host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'
    url = re.compile(r'^(ftp|tcp|rtmp|udp|wss?|https?)://(?:\S+(?::\S*)?@)?(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')(?::\d{2,5})?(?:[/?#][^\s]*)?\Z', re.IGNORECASE)

    if value == '' or len(value) >= 2083 or len(value) <= 3:
        return False
    return bool(url.match(value))