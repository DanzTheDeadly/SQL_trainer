from src.server import DBHttpServer
import yaml

if __name__ == '__main__':
    with open('config.yaml') as file:
        config = yaml.safe_load(file)
    server = DBHttpServer(config)
    try:
        server.run()
    except:
        server.stop()
        raise
