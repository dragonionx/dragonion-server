import sys

from dragonion_server.utils.onion import Onion
from dragonion_server.utils.generated_auth.db import AuthFile
from dragonion_server.utils.config.db import services

from rich import print


def integrate_onion(port: int, name: str) -> Onion:
    onion = Onion()

    try:
        onion.connect()
        onion.write_onion_service(name, port)
    finally:
        if not onion.connected_to_tor:
            onion.cleanup()
            sys.exit(1)
    
    print(f'[green]Available on[/] '
          f'{(onion_host := onion.start_onion_service(name))}.onion')
    
    auth = AuthFile(name)
    auth['host'] = f'{onion_host}.onion'
    auth['auth'] = onion.auth_string
    print(f'To connect to server just share [green]{auth.filename}[/] file')
    print(f'Or use [#ff901b]service id[/] and [#564ec3]auth string[/]: \n'
          f'[#ff901b]{onion_host}[/] \n'
          f'[#564ec3]{services[name].client_auth_priv_key}[/]')
    
    return onion