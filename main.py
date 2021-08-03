#!/usr/bin/python3.8

from src.server import DBHttpServer

if __name__ == '__main__':
    server = DBHttpServer()
    server.run()