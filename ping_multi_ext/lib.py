import argparse
import shlex
import ping_multi_ext # version
import ipaddress

def statistics_list():
    return ['Last', 'Loss%', 'Avg', 'Min', 'Max', 'StDev', 'RX_cnt', 'TX_cnt', 'XX_cnt']

def generate_hosts_cidr(cidr):
    try:
        network_object = ipaddress.ip_network(cidr)
        if isinstance(network_object, ipaddress.IPv6Network):
            print('ping_multi: -g works only with IPv4 addresses')
            exit()
        host_addresses = [ str(ip_address) for ip_address in network_object.hosts() ]
    except Exception as e:
        print(e)
        exit()

    return host_addresses

def argv_parser_base(prog_desc):
    parser = argparse.ArgumentParser(
        description=prog_desc
    )

    vstr = '{} {} | {}'.format(
        '%(prog)s', ping_multi_ext.version,
        'https://github.com/famzah/ping-multi-ext'
    )
    parser.add_argument('--version', action='version', version=vstr)

    dval = 0
    parser.add_argument('--hosts-max-width', type=int, default=dval,
        help=f'maximum width of the hosts column; default={dval}')

    parser.add_argument('-g,--generate', dest='cidr',
        help=f'Generate a target list from supplied cidr')

    dval = statistics_list()[0]
    parser.add_argument('-s,--stat', dest='stats_show_initially', choices=statistics_list(),
        default=dval,
        help=f'statistic to display initially; default={dval}')

    return parser

def remove_ssh_user(host):
    parts = host.split('@', 2)
    
    if len(parts) == 3:
        parts.pop(1)

    return '@'.join(parts)

def compose_ping_cmd(host, cmd_args):
    parts = host.split('@', 1)

    ping_cmd = 'ping -O -W {} -i {} {}'.format(
        shlex.quote(str(cmd_args['wait'])),
        shlex.quote(str(cmd_args['interval'])),
        shlex.quote(parts[0])
    )

    if len(parts) > 1:
        return 'ssh -o BatchMode=yes {} {}'.format(
            shlex.quote(parts[1]),
            shlex.quote(ping_cmd)
        )
    else:
        return ping_cmd
