import random as rand
import math
import matplotlib as plt
import time


class Simulator():    
    def __init__(self):

        self._mm_size = self.bigOlInput("memory")
        self._pg_size = self.bigOlInput("page")
        self._cache_size = self.bigOlInput("cache")
        self.preprocessing()
        self._hits = 0
        self._misses = 0
        self._mapping = self.pick_config()
        if self._mapping != 1:
            self._k = self.set_k()
            self._replacement = self.pick_policy()


        while True:
            try:
                samp = int(input("sample size: "))
                if samp < 1:
                    print("Must be above 0")
                    continue
                break
            except ValueError:
                print("BAD")
        self._sample = samp

        self._set_size = self._mm_size

    def bigOlInput(self,thing):
        sizes = {"bt":0, "kb":1, "mb":2, "gb":3}
        while True:
            try:
                inpt = input(f"enter {thing} size. Must be power of 2 and a valid denomination (_bt, _kb, _mb, _gb)")
                val = int(inpt[0:-2])
                denom = inpt[-2:]
                print(val)
                print(denom)
                if (val & (val -1)) != 0:
                    print("must be power of 2")
                    continue
                if denom not in ('gb','mb','kb','bt'):
                    print("use _bt, _kb, _mb, _gb")
                    continue
                break
            except ValueError:
                print("BAD")
        digit1 = sizes[denom]
        digit2 = int(math.log(val,2))
        digit = int(str(digit1) + str(digit2))
        bigolsiize = int(2**digit) -1
        return bigolsiize


    def preprocessing(self):
        self.addr_len = len(bin(self._mm_size)[2:]) # Length of the Binary representation
        self.offset = len(bin(self._pg_size)[2:])
        self.cache_len = len(bin(self._cache_size)[2:]) 
        self.line = self.cache_len - self.offset
        self.tag = self.addr_len - self.line - self.offset
        self._cache = [None] * int((self._cache_size + 1) / (self._pg_size+1))
        
        print(self._cache)

    
    def pick_config(self):
        while True:
            try:
                inpt = input(f"Pick a config: \nConfig 1, Direct Mapping. \nConfig 2, Fully Associative. \nConfig 3, k-way Associative Mapping") 
                print(inpt)
                print(type(inpt))
                if inpt not in [1, 2, 3]:
                    print("Pick a policy #")
                    continue
                
                
                break
            except ValueError:
                print("BAD")
        return inpt
    
    def set_k(self):
        while True:
            try:
                inpt = input("Set K")
                if (inpt & (inpt -1)) != 0:
                    print("must be power of 2")
                    continue
                break
            except ValueError:
                print("BAD")
        return inpt
            

    def pick_policy(self):
        while True:
            try:
                inpt = input(f"Pick a policy: \nPolicy 1, replacement policy cache collisions are resolved by overwriting.\n Policy 2, prioritize empty slots.\n Policy 3, prioritize the least recently used")
                if inpt not in [1, 2, 3]:
                    print("Pick a policy #")
                    continue
                break
            except ValueError:
                print("BAD")
        return inpt
    
    def full_replacement(self, address):
        pass

    def k_way_associative(self):
        # Iterate through the sample to generate the number of hits/misses
        for k in range(self._sample):
            
            num = format(int(rand.randint(0,self._mm_size)),f'0{self.addr_len}b')
            print(num)
            _set_size = int((self._cache_size+1) / self._k / (self._pg_size+1)) # Returns the set size in terms of the number of pages

            k_len = len(bin(self._k-1)[2:])
            k_tag = self.addr_len - self.offset - k_len
            _set = int(num[k_tag:k_tag+k_len],2)
            print(f"k_len: {k_len}")
            print(k_tag)
            print(_set_size)
            print(_set)
            ishit = False
            index = 0
            for i in range(_set):
                index += _set_size
            for x in range(_set_size):
                if self._cache[index+x] == None:
                    continue
                if self._cache[index+x][0:k_tag] == num[0:k_tag]:
                    print("TAG HIT")
                    ishit = True
                    break

                else:
                    print("Not hit")
            if ishit:
                break
            for x in range(_set_size):
                if self._cache[index+x] == None:
                    self._cache[index+x] = num
                    break
        print(self._cache)
                
    def kway(self):
        # Iterate through the sample to generate the number of hits/misses
        for k in range(self._sample):
            self._k = 4
            num = format(int(rand.randint(0,self._mm_size)),f'0{self.addr_len}b')
            print(num)
            _set_size = int((self._cache_size+1) / self._k / (self._pg_size+1)) # Returns the set size in terms of the number of pages

            k_len = len(bin(self._k-1)[2:])
            k_tag = self.addr_len - self.offset - k_len
            _set = int(num[k_tag:k_tag+k_len],2)
            print(f"k_len: {k_len}")
            print(k_tag)
            print(_set_size)
            print(_set)
            ishit = False
            index = 0
            for i in range(_set):
                index += _set_size
            for x in range(_set_size):
                if self._cache[index+x] == None:
                    continue
                if self._cache[index+x][0:k_tag] == num[0:k_tag]:
                    print("TAG HIT")
                    ishit = True
                    break

                else:
                    print("Not hit")
            if ishit:
                break

            #if empty replacement policy
            for x in range(_set_size):
                if self._cache[index+x] == None:
                    self._cache[index+x] = num
                    break
        print(self._cache)
                
                    
            



    def direct(self):

        for i in range(self._sample):
            print("------")
            num = format(int(rand.randint(0,self._mm_size)), f'0{self.addr_len}b')
            print(num)
            _tag = int(num[0:self.tag],2)
            _line = int(num[self.tag:self.tag+self.line],2)


            print(f"tag: {_tag}")
            print(f"line: {_line}")

            if self._cache[_line] == None:
                self._cache[_line] = num
                print("NEW")
            elif self._cache[_line][0:self.tag] == num[0:self.tag]:
                self._hits
                print("HIT")
                print(f"cached tag: {self._cache[_line][0:self.tag]}")
                print(f"   new tag: {num[0:self.tag]}")
            else:
                print("MISS")
                print(f"cached tag: {self._cache[_line][0:self.tag]}")
                print(f"   new tag: {num[0:self.tag]}")
                self._cache[_line] = num


            # print(num)
            # print(tag)
            # print(line)
        print(self._cache)

    def main(self):
        pass
        if self._mapping == 1 or self._replacement == 1:
            self.direct()
        


def continuous_ticker(interval=1):
    """Prints a 'tick' continuously."""
    elapsed_time = 0
    test = Simulator()
    try:
        while True:
            test.kway()
            elapsed_time += 2
            print(f"Tick: {elapsed_time}")
            time.sleep(interval) # ticks every interval seconds
    except KeyboardInterrupt: # ctrl c
        print("\nTicker stopped.")

# Start the ticker
if __name__ == "__main__":
    continuous_ticker(2) # Ticks every 2 seconds




def test():
    test = Simulator()
    #test.pick_policy()
    test.kway()   

# test()