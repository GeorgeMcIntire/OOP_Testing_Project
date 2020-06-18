from collections import defaultdict
from time import time
#import sys
import argparse

class Distance:
    __metrics = ["euclidean", "cosine", "manhattan"]
    
    all_distances = defaultdict(list)
    
    
    def __init__(self, metric, *args):
        if metric not in self.__metrics:
            raise KeyError("Select one of the following distance metrics {0}, {1}, {2}".format(*self.__metrics))
            
        if not args:
            raise ValueError("No values supplied")
        
        for arg in args:
            if type(arg) != int and type(arg) !=float:
                raise ValueError("One or more of the args is not a number")
            
        self.metric = metric
        self.nums = list(args)
        self.distance = 0
        self.distance_called = False
        self.__metric_functions = {"euclidean":self.euclidean_distance(), 
                                            "cosine":self.cosine_distance(), 
                                            "manhattan":self.manhattan_distance()}
    
    def timer(func):
        def wrapper(self):
            ts = time()
            distance = func(self)
            te = time()
            self.time = te - ts
            return distance
        return wrapper
    
    @timer
    def distance_calculator(self):
        self.distance_called = True
        self.distance = self.__metric_functions[self.metric]
        self.__class__.all_distances[self.metric].append(self.distance)
        return round(self.distance, 3)
    

    def has_distance(self):
        return self.distance_called
    
            
    def euclidean_distance(self, *args):
        if args:
            input_numbers = args
        else:
            input_numbers = self.nums
                
        squares = map(lambda x:x**2, input_numbers)
        sum_of_squares = sum(squares)
        return sum_of_squares**.5
    
    def manhattan_distance(self, *args):
        if args:
            input_numbers = args
        else:
            input_numbers = self.nums
                
        return sum(map(lambda x:abs(x), input_numbers))
    
    def cosine_distance(self, *args):
        if args:
            input_numbers = list(args)
        else:
            input_numbers = self.nums
        
        cosine_partner = input_numbers[:]
        cosine_partner[-1] = 0
        dot_prod = sum(map(lambda x,y: x*y, input_numbers, cosine_partner))
        
        norma = self.euclidean_distance()
        normb = self.euclidean_distance(*cosine_partner)
        
        cos = dot_prod/(norma*normb)
        return cos
    
    @classmethod
    def total_distances(cls):
        """Returns the sums of all three types of distances"""
        return {key: sum(values) for key, values in cls.all_distances.items() }
    
    
    def concatenate(self, other):
        if self.metric != other.metric:
            raise TypeError("Cannot add distances of different metrics")
        return Distance(self.metric, *self.nums, *other.nums)
    
    def __str__(self):
        
        return "The {} distance for the set of numbers {} is {}".format(self.metric,self.nums, round(self.distance, 3))
    
    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.nums)
    
    
    def __add__(self, other):
        if self.metric != other.metric:
            raise TypeError("Cannot add distances of different metrics")
            
        if not self.distance_called or not other.distance_called:
            raise ValueError("One or both Distance objects have not fitted a distance")
                
        return self.distance + other.distance
    
    def __sub__(self, other):
        if self.metric != other.metric:
            raise TypeError("Cannot subtract distances of different metrics")
            
        if not self.distance_called or not other.distance_called:
            raise ValueError("One or both Distance objects have not fitted a distance")
                
        return self.distance - other.distance
    
    def __eq__(self, other):
        if self.metric != other.metric:
            raise TypeError("Cannot subtract distances of different metrics")
            
        if not self.distance_called or not other.distance_called:
            raise ValueError("One or both Distance objects have not fitted a distance")
        
        return self.distance == other.distance
    
    
    def __gt__(self, other):
        if self.metric != other.metric:
            raise TypeError("Cannot subtract distances of different metrics")
            
        if not self.distance_called or not other.distance_called:
            raise ValueError("One or both Distance objects have not fitted a distance")
        if self.metric != "cosine":
            return self.distance > other.distance
        else:
            return self.distance < other.distance
            
    def __lt__(self, other):
        if self.metric != other.metric:
            raise TypeError("Cannot subtract distances of different metrics") 
            
        if not self.distance_called or not other.distance_called:
            raise ValueError("One or both Distance objects have not fitted a distance") 
            
        if self.metric != "cosine":
            return self.distance < other.distance
        else:
            return self.distance > other.distance
    
    def __ge__(self, other):
        if self.metric != other.metric:
            raise TypeError("Cannot subtract distances of different metrics") 
        if not self.distance_called or not other.distance_called:
            raise ValueError("One or both Distance objects have not fitted a distance")   
        if self.metric != "cosine":
            return self.distance >= other.distance
        else:
            return self.distance <= other.distance
    
    def __le__(self, other):
        if self.metric != other.metric:
            raise TypeError("Cannot subtract distances of different metrics")  
        if not self.distance_called or not other.distance_called:
            raise ValueError("One or both Distance objects have not fitted a distance")  
        if self.metric != "cosine":
            return self.distance <= other.distance
        else:
            return self.distance >= other.distance


def convert_input_numbers(value):    
    number = float(value)
    return number
    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--metric", type = str, help = "Choose the desired distance metric", required = True)
    parser.add_argument("-n", "--numbers", nargs = "+", type = convert_input_numbers, help = "Pass in the numbers for which you wish to calculate distance", required = True)
    args = parser.parse_args()
    return args 
    




if __name__ == "__main__":
    args = get_args()
    do = Distance(args.metric, *args.numbers)
    dist = do.distance_calculator()
    print(do)