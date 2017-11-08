# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:09:18 2017

@author: joseph.chen
"""
import time
import sys
import random

def random_pick(lst, prob):
    rand_num = random.random()
    acc_prob = 0
    for n in range(len(prob)):
        acc_prob += prob[n]
        if rand_num<=acc_prob:
            return lst[n]
    

class Config(object):
    def __init__(self):
        pass
    
    @staticmethod
    def get_prob_mode1():
        return {3: 0.2353, 4: 0.2309, 5: 0.2264, 6: 0.1937, 7: 0.0504, 8: 0.0312, 
                9: 0.0211,	10: 0.0110}
        
    @staticmethod
    def get_prob_mode2():
        return {3: 0.1660, 4: 0.1507, 5: 0.1457, 6: 0.1403, 7: 0.1365, 8: 0.1336, 
                9: 0.1255,	10: 0.0017}
        
    @staticmethod
    def get_odd_mode1():
        return {47: 0.6667, 71: 0.3333}
    
    @staticmethod
    def get_odd_mode2():
        return {59: 0.8, 89: 0.1333, 119: 0.0667}


class Roulette(object):
    def __init__(self):
        self.reel = list(range(1,37+1))
        self.output = None
        
    def set_mode(self, mode):
        """ Set mode of the game (update pay_table)
        param mode: str, normal/mode1/mode2
        """
        self.pay_table = {}
        if mode=="normal":
            for symbol in self.reel:
                self.pay_table[symbol] = 35
        else:
            if mode=="mode1":
                prob_symbol = Config.get_prob_mode1()
                prob_odd = Config.get_odd_mode1()
                lowest_odd = 32
            elif mode=="mode2":
                prob_symbol = Config.get_prob_mode2()
                prob_odd = Config.get_odd_mode2()
                lowest_odd = 29
            else:
                sys.exit("Mode must be either normal/mode1/mode2 !")
            
            num_symbols_mode1 = random_pick(list(prob_symbol.keys()), list(prob_symbol.values()))
            reel = self.reel[:]
            for n in range(num_symbols_mode1):
                symbol = random.choice(reel)
                reel.remove(symbol)
                self.pay_table[symbol] = random_pick(list(prob_odd.keys()), list(prob_odd.values()))
            for symbol in reel:
                self.pay_table[symbol] = lowest_odd
    
    def spin(self):
        """Instead of rotating the reel, we alternatively choose a output symbol
        from the reel.
        """
        self.output = random.choice(self.reel)
        
    def check_payment(self, choice):
        """Check the payment of a single bet
        param choice: int 1-37, the symbol a player chooses to bet
        return payment: the amount of money returning to player (including wager)
        """
        if self.output==choice:
            return self.pay_table[choice]+1
        else:
            return 0
    
    def play(self, mode, choice, Nround):
        """
        param choice: int 1-37, the choice player placing bet
        param Nround: int, number of rounds the player plays
        return total_wager: float, accumulated wager
        return total_payment: float, accumulated payment
        """
        total_wager = 0
        total_payment = 0
        n = 0
        while (n<Nround):
            n += 1
            self.set_mode(mode)
            self.spin()
            payment = self.check_payment(choice)
            total_wager += 1
            total_payment += payment
        return total_wager, total_payment
    
if __name__=="__main__":
    Nround = 100000000
    roulette = Roulette()
    tic = time.time()
    total_wager, total_payment = roulette.play("mode1", 1, Nround)
    toc = time.time()
    print("Elapsed time: {:.2f} seconds".format(toc-tic))
    print("Wager: {}, Payment: {}".format(total_wager, total_payment))
    print("RTP: {:.4f}".format(total_payment*1.0/total_wager))
