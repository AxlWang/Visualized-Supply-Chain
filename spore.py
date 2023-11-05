import random


class Spore(object):

    def __init__(self, startsoh, store_id, scope, rank):
        self.spaceX = random.randint(50, 1100)
        self.spaceY = random.randint(50, 600)
        self.daily_soh = []
        self.soh = startsoh
        self.store_id = store_id
        self.daily_soh.append(self.soh)
        self.neighbors = {}
        self.trace = {}
        self.scope = scope
        self.rank = rank
        self.in_transit = 0
        self.sales = []

    def consume(self, qty):
        if self.soh >= qty:
            self.soh -= qty
        else:
            self.soh = 0

    def absorb(self, qty):
        self.soh += qty

    def record_sales(self, qty):
        self.sales.append(qty)





