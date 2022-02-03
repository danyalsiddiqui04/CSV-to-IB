# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 23:27:30 2021

@author: Danyal
"""
from ibapi.client import EClient  # used to make connection to IB's API
from ibapi.wrapper import EWrapper  # python wrapper used to convert python code to low-level languages
from ibapi.contract import Contract  # used to make contract objects
from ibapi.order import Order  # used to make order objects
import threading  # used to run API connection on separate thread
import pandas as pd  # used for dataframe
import json
import time
import csv

# The API app which places orders and connects to IB
class IB_API_APP(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)  # initialize EClient to connect to IB
        self.order_df = pd.DataFrame(columns=["PermId", "ClientId", "OrderId", "Account", "Symbol", 
                                              "SecType", "Exchange", "Action", "OrderType","TotalQty", 
                                              "CashQty", "LmtPrice", "AuxPrice", "Status"])
        self.pos_df = pd.DataFrame(columns=["Account", "Symbol", "SecType", "Currency", "Position", "Avg cost"])
    
    # print error info in case of error
    def error(self, reqId, errorCode, errorString):
        if reqId == -1:
            messageType = "Message"
        else:
            messageType = "Error"
        print("{}: {} {} {}".format(messageType, reqId, errorCode, errorString))
    
    # get new orderId for next order
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)
    
    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)
        order_dict = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": orderId, 
                      "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty, 
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": orderState.status}
        order.contract = contract
        self.order_df = self.order_df.append(order_dict, ignore_index=True)
        self.order_df = self.order_df.drop_duplicates()
        
    def position(self, account, contract, position, avgCost):
        super().position(account, contract, position, avgCost)
        pos_dict = {"Account": account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Currency": contract.currency, "Position": position, "Avg cost": avgCost}
        self.pos_df = self.pos_df.append(pos_dict, ignore_index=True)

    def createContract(self, symbol, secType, currency, exchange):
        # create a contract object
        contract = Contract()
        contract.symbol = symbol
        contract.secType = secType
        contract.currency = currency
        contract.exchange = exchange
        return contract
    
    def mktOrder(self, account, action, quantity, tif, rth, triggerMethod, mgmtAlgo, ocaGroup, goodTime, autoCancel, orderId, parentId, orderRef):
        # create order object - this does not execute the order
        order = Order()
        order.account = account
        order.action = action
        order.orderType = "MKT"
        order.totalQuantity = quantity
        if orderRef:
            order.orderRef = orderRef
        if tif:
            order.tif = tif
        if rth:
            order.conditionsIgnoreRth = rth
        if triggerMethod and triggerMethod != "Default" and triggerMethod != "DEFAULT" and triggerMethod != "default":
            order.triggerMethod = triggerMethod
        if mgmtAlgo:
            order.usePriceMgmtAlgo = mgmtAlgo
        if ocaGroup:
            order.ocaGroup = ocaGroup
        if goodTime:
            order.goodAfterTime = goodTime
        if autoCancel:
            order.autoCancelDate = autoCancel
        # only transmit order once entire "family" is created
        if self.transmitOrder == False:
            order.transmit = False
        elif self.transmitOrder == True:
            order.transmit = True
        # check if order is a child order
        if parentId:
            print("Child order")
            order.parentId = self.childId
        return order
    
    def lmtOrder(self, account, action, quantity, tif, lmtPrice, rth, triggerMethod, mgmtAlgo, ocaGroup, goodTime, autoCancel, orderId, parentId, orderRef):
        # create order object - this does not execute the order
        order = Order()
        order.account = account
        order.action = action
        order.orderType = "LMT"
        order.totalQuantity = quantity
        order.lmtPrice = lmtPrice
        if orderRef:
            order.orderRef = orderRef
        if tif:
            order.tif = tif
        if rth:
            order.conditionsIgnoreRth = rth
        if triggerMethod and triggerMethod != "Default" and triggerMethod != "DEFAULT" and triggerMethod != "default":
            order.triggerMethod = triggerMethod
        if mgmtAlgo:
            order.usePriceMgmtAlgo = mgmtAlgo
        if ocaGroup:
            order.ocaGroup = ocaGroup
        if goodTime:
            order.goodAfterTime = goodTime
        if autoCancel:
            order.autoCancelDate = autoCancel
        # only transmit order once entire "family" is created
        if self.transmitOrder == False:
            order.transmit = False
        elif self.transmitOrder == True:
            order.transmit = True
        # check if order is a child order
        if parentId:
            print("Child order")
            order.parentId = self.childId
        return order
    
    def litOrder(self, account, action, quantity, tif, lmtPrice, auxPrice, rth, triggerMethod, mgmtAlgo, ocaGroup, goodTime, autoCancel, orderId, parentId, orderRef):
        # create order object - this does not execute the order
        order = Order()
        order.account = account
        order.action = action
        order.orderType = "LIT"
        order.totalQuantity = quantity
        order.lmtPrice = lmtPrice
        order.auxPrice = auxPrice
        if orderRef:
            order.orderRef = orderRef
        if tif:
            order.tif = tif
        if rth:
            order.conditionsIgnoreRth = rth
        if triggerMethod and triggerMethod != "Default" and triggerMethod != "DEFAULT" and triggerMethod != "default":
            order.triggerMethod = triggerMethod
        if mgmtAlgo:
            order.usePriceMgmtAlgo = mgmtAlgo
        if ocaGroup:
            order.ocaGroup = ocaGroup
        if goodTime:
            order.goodAfterTime = goodTime
        if autoCancel:
            order.autoCancelDate = autoCancel
        # only transmit order once entire "family" is created
        if self.transmitOrder == False:
            order.transmit = False
        elif self.transmitOrder == True:
            order.transmit = True
        # check if order is a child order
        if parentId:
            print("Child order")
            order.parentId = self.childId
        return order
    
    def familyOrders(self):
        # dealing with parent and child orders
        with open(self.filename, 'r') as csv_file:
            self.totalRows = 0
            csv_reader = csv.DictReader(csv_file)
            self.orderIdDict = {}
            self.childIdDict = {}
            self.parentIdList = []
            self.childIdList = []
            # get lists of parent/single and child orders, respectively
            for loc, row in enumerate(csv_reader):
                if row.get("OrderId"):
                    self.orderIdDict[row.get("OrderId")] = loc
                if row.get("ParentOrderId"):
                    self.childIdDict[row.get("ParentOrderId")] = loc
                self.totalRows += 1
            for item in self.orderIdDict:
                if item in self.childIdDict:
                    self.parentIdList.append(self.orderIdDict.get(item))
            for item in self.childIdDict:
                 self.childIdList.append(self.childIdDict.get(item))
    
    def checkRestrictions(self):
        restriction = False
        # setting limit for number of filled orders
        order_df = self.order_df
        currentFilled = 0
        currentOrders = 0
        statuses = order_df["Status"]
        if self.isOrderChecked:
            # check if number of orders exceeds limit
            for status in statuses:
                if status == "Submitted" or status == "submitted":
                    currentOrders += 1
            if currentOrders >= self.orderLimit:
                restriction = True
        if self.isFilledChecked:
            # check if number of filled orders exceeds limit
            for status in statuses:
                if status == "Filled" or status == "filled":
                    currentFilled += 1
            if currentFilled >= self.filledLimit:
                restriction = True
        return restriction
    
    def startSystem(self, file):
        localId = self.nextValidOrderId
        # where all orders and contracts will be made
        with open(file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            self.transmitOrder = True
            for loc, row in enumerate(csv_reader):
                print("Row #:", str(loc) + "/" + str(self.totalRows))
                action = row.get("Action")
                quantity = row.get("Quantity")
                symbol = row.get("Symbol")
                secType = row.get("SecType")
                exchange = row.get("Exchange")
                tif = row.get("TimeInForce")
                orderType = row.get("OrderType")
                currency = row.get("Currency")
                lmtPrice = row.get("LmtPrice")
                auxPrice = row.get("AuxPrice")
                account = row.get("Account")
                rth = row.get("Rth")
                triggerMethod = row.get("TriggerMethod")
                orderRef = row.get("OrderRef")
                mgmtAlgo = row.get("UsePriceMgmtAlgo")
                ocaGroup = row.get("OcaGroup")
                goodTime = row.get("GoodAfterTime")
                autoCancel = row.get("AutoCancelDate")
                orderId = row.get("OrderId")
                parentId = row.get("ParentOrderId")
                print("\n"+"Order", str(localId), orderId, "will be placed:", action, quantity, symbol, exchange)
                # check if currnet order is a parent order
                if loc in self.parentIdList:
                    self.transmitOrder = False
                    self.childId = localId
                # check if current order is final child order
                if loc in self.childIdList:
                    self.transmitOrder = True
                # create contract object for order
                contract = self.createContract(symbol, secType, currency, exchange)
                if orderType == "MKT":
                    # create order object for order
                    order = self.mktOrder(account, action, quantity, tif, rth, triggerMethod, mgmtAlgo, ocaGroup, goodTime, autoCancel, orderId, parentId, orderRef)
                elif orderType == "LMT":
                    # create order object for order
                    order = self.lmtOrder(account, action, quantity, tif, lmtPrice, rth, triggerMethod, mgmtAlgo, ocaGroup, goodTime, autoCancel, orderId, parentId, orderRef)
                elif orderType == "LIT":
                    # create order object for order
                    order = self.litOrder(account, action, quantity, tif, lmtPrice, auxPrice, rth, triggerMethod, mgmtAlgo, ocaGroup, goodTime, autoCancel, orderId, parentId, orderRef)
                # place the order based on the order and contract objects
                self.placeOrder(localId, contract, order)
                time.sleep(2)  # wait to ensure order is placed
                localId += 1  # increment orderId for next order
                # check if limitations have been reached
                self.restriction = self.checkRestrictions()
                if self.restriction or self.stopSystem:
                    self.reqGlobalCancel()
                    time.sleep(1)
                    break

    def startConnection(self):
        self.run()  # initiate connection with IB
        
    def setupConnection(self, ip, socket, client_id):
        # replace second argument in connect() with desired port
        self.connect(ip, socket, clientId=client_id)  # set up connection to IB
        # start a separate thread to run websocket connection
        con_thread = threading.Thread(target=self.startConnection, daemon=True)
        con_thread.start()
        time.sleep(1)

def stop():
    app.stopSystem = True

def system():
    global app
    with open("options.txt", "r") as options:
        for line in options:
            optionsDict = json.loads(line)
        port = optionsDict.get("port")
        isFilledChecked = optionsDict.get("isFilledChecked")
        filename = optionsDict.get("filename")
        filledLimit = optionsDict.get("filledLimit")
        orderLimit = optionsDict.get("orderLimit")
        isOrderChecked = optionsDict.get("isOrderChecked")
    # client id used to identify different systems on the same account
    client_id = 0
    ip = "127.0.0.1"
    # create the api app object
    app = IB_API_APP()
    # setup and start connection to IB
    app.setupConnection(ip, port, client_id)
    
    # program variables
    app.filledLimit = int(filledLimit)
    print(app.filledLimit)
    app.currentFilled = 0
    app.isFilledChecked = isFilledChecked
    app.filename = filename
    app.orderLimit = int(orderLimit)
    app.isOrderChecked = isOrderChecked
    app.stopSystem = False
    
    app.familyOrders()
    app.startSystem(filename)
    
    app.reqPositions()
    time.sleep(5)
    print(app.order_df, "\n")
    print(app.pos_df)