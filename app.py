__author__ = 'Jakub Dubec'

from config import config
from dataset import FusionTable
from dataset import Database
from sensor import DHT
import os

config.read(os.path.dirname(os.path.abspath(__file__)) + "/config/config.ini")

#Database.Database().insert(DHT.DHT().get_data())
FusionTable.FusionTable().insert(DHT.DHT().get_data())

config.write(open(os.path.dirname(os.path.abspath(__file__)) + "/config/config.ini", "w+"))