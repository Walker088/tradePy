#!/usr/bin/env python3
from pprint import pprint
import pandas as pd
import numpy as np
import logging, logging.config

logging.config.fileConfig("../config/stg.conf")
log = logging.getLogger("root")

class MutexTurtle:
    def __init__(self, entryPoint, stopLoss, tkProfit):
        self.entryPoint = entryPoint
        self.stopLoss = stopLoss
        self.tkProfit = tkProfit

    # Entry point is 0.03 times of ma20
    # If current value over entryPoint then return true
    def checkEntPoint(self, cv, daykdf, entFactor=0.03):
        pass

    # Stop loss is 0.01 times of ma20
    # Return the stop loss value for process to check
    def getStpLoss(self, cst, daykdf, losFactor=0.01):
        pass

    # Take profit is 0.05 times of ma20
    # Return the take tkProfit for process to check
    def getTkProfit(self, cst, daykdf, proFactor=0.05):
        pass

    # While cv over tkProfit, update the stop loss to cv minus 0.01 times of ma20
    def updateStpLoss(self, cv, daykdf):
        pass

class KDstg:
    def __init__(self, entryPoint, stopLoss, tkProfit):
        self.entryPoint = entryPoint
        self.stopLoss = stopLoss
        self.tkProfit = tkProfit

class MACDstg:
    def __init__(self, entryPoint, stopLoss, tkProfit):
        self.entryPoint = entryPoint
        self.stopLoss = stopLoss
        self.tkProfit = tkProfit

class DMIstg:
    def __init__(self, entryPoint, stopLoss, tkProfit):
        self.entryPoint = entryPoint
        self.stopLoss = stopLoss
        self.tkProfit = tkProfit
