import click
import sys
from client.client import Client
from server.server import Server
from constants import *
import time

@click.group()
def cli():
    pass

@cli.command()
def server():
    try:
        server = Server(ADDRESS)
        server.setDaemon(True)
        server.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        server.server.close()
        sys.exit(0)

@click.argument('name')
@click.option('--speak', is_flag=True)
@cli.command()
def client(name, speak):
    try:
        if not speak:
            speak= False
        client = Client(name, ADDRESS, speak)
        client.setDaemon(True)
        client.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        client.conn.close()
        sys.exit(0)

@cli.command()
def test():
    pass