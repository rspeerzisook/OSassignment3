import random as rand

class Simulator():
    print("yeah")
    def __init__(self, mm_size = 512, pg_size = 4, cache_size = 32):
    
        self.mm_size = int(mm_size-1)
        self._pg_size = int(pg_size-1)
        self._cache_size = int(cache_size-1)
        #self._memory_config = None
        self._sample = 10

        self._set_size = self._mm_size

    
    @property
    def mm_size(self):
        return self._mm_size
    
    @mm_size.setter
    def mm_size(self, new_mm_size):
        if type(new_mm_size) != int and type(new_mm_size) != float:
            raise TypeError("Enter a valid size for the main memory")
        elif new_mm_size%2 == 0:
            raise ValueError("Please enter a power of 2")
        self._mm_size = new_mm_size

    def preprocessing(self):
        self.addr_len = len(bin(self._mm_size)[2:])
        self.offset = len(bin(self._pg_size)[2:])
        self.cache_len = len(bin(self._cache_size)[2:]) 
        self.line = self.cache_len - self.offset
        self.tag = self.addr_len - self.line - self.offset
        self._cache = [None] * int((self._cache_size + 1) / (self._pg_size+1))
        
        print(self._cache)

    
    def pick_config(self):
        pass

    def generate(self):
        for i in range(self._sample):
            num = bin(rand.randint(0,self.mm_size))[2:]

            self._cache[i] = int(num)
            print(f"{self._cache[0]:09d}")

            

            

    


def test():
    test = Simulator()
    test.preprocessing()
    test.generate()   

test()