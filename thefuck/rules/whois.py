# -*- encoding: utf-8 -*-
from six.moves.urllib.parse import urlparse


def match(command, settings):
    """
    What the `whois` command returns depends on the 'Whois server' it contacted
    and is not consistent through different servers. But there can be only two
    types of errors I can think of with `whois`:
        - `whois https://en.wikipedia.org/` → `whois en.wikipedia.org`;
        - `whois en.wikipedia.org` → `whois wikipedia.org`.
    So we match any `whois` command and then:
        - if there is a slash: keep only the FQDN;
        - if there is no slash but there is a point: removes the left-most
          subdomain.

    We cannot either remove all subdomains because we cannot know which part is
    the subdomains and which is the domain, consider:
        - www.google.fr → subdomain: www, domain: 'google.fr';
        - google.co.uk → subdomain: None, domain; 'google.co.uk'.
    """
    return 'whois' in command.script


def get_new_command(command, settings):
    url = command.script.split()[1]

    if '/' in command.script:
        return 'whois ' + urlparse(url).netloc
    elif '.' in command.script:
        return 'whois ' + '.'.join(urlparse(url).path.split('.')[1:])
