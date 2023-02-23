import logging

log = logging.getLogger()
log.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler('./data/logs.log')
file_handler.setFormatter(formatter)

log.addHandler(stream_handler)
log.addHandler(file_handler)