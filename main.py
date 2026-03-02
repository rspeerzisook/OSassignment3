import random as rand
import math


class Simulator():    
    def __init__(self):

        self._mm_size = self.bigOlInput("memory")
        self._pg_size = self.bigOlInput("page")
        self._cache_size = self.bigOlInput("cache")
        #self._mapping = self.pick_config("mapping")
        #self._replacement = self.pick_policy("replacement")

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
    
        #self.mm_size = int(mm_size-1)
        #self._pg_size = int(pg_size-1)
        #self._cache_size = int(cache_size-1)
        #self._memory_config = None
        self._sample = 10

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
        self.addr_len = len(bin(self._mm_size)[2:])
        self.offset = len(bin(self._pg_size)[2:])
        self.cache_len = len(bin(self._cache_size)[2:]) 
        self.line = self.cache_len - self.offset
        self.tag = self.addr_len - self.line - self.offset
        self._cache = [None] * int((self._cache_size + 1) / (self._pg_size+1))
        
        print(self._cache)

    
    def pick_config(self, config):
        while True:
            try:
                inpt = input(f"Pick a {config} config: \nConfig 1, Direct Mapping. \nConfig 2, Fully Associative. \nConfig 3, k-way Associatvie Mapping") 
                print(inpt)
                print(type(inpt))
                if inpt not in [1, 2, 3]:
                    print("Pick a policy #")
                    continue
                if inpt == 2:
                    self._k = 1
                elif inpt == 3:
                    try:
                        self._k = input(f"Pick a k-value")
                        if type(self._k) is not int:
                            print("Not a valid k-value")
                            continue
                        break
                    except  ValueError:
                        print("BAD")
                break
            except ValueError:
                print("BAD")
        return inpt

    def pick_policy(self, policy):
        while True:
            try:
                inpt = input(f"Pick a {policy} policy: \nPolicy 1, Replacement policy cache collisions are resolved by overwriting.\n Policy 2, prioritize empty slots.\n Policy 3, prioritize the least recently used")
                if inpt not in [1, 2, 3]:
                    print("Pick a policy #")
                    continue
                break
            except ValueError:
                print("BAD")
        return inpt
    
    def full_replacement(self, address):
        pass

    def k_way_associative(self, ):
        pass
                
    def kway(self):
        for i in range(self._sample):
            num = format(int(rand.randint(0,self._mm_size)),'09b')

            _set_size = self._cache_size / 4

            k_len = len(format(int(4),'09b'))
            k_tag = self.addr_len - self.offset - k_len
            _set = int(num[k_tag:k_tag+k_len])

            



    def direct(self):

        for i in range(self._sample):
            print("------")
            num = format(int(rand.randint(0,self._mm_size)), '09b')
            print(num)
            _tag = int(num[0:self.tag],2)
            _line = int(num[self.tag:self.tag+self.line],2)


            print(f"tag: {_tag}")
            print(f"line: {_line}")

            if self._cache[_line] == None:
                self._cache[_line] = num
                print("NEW")
            elif self._cache[_line][0:self.tag] == num[0:self.tag]:
                print("HIT")
                print(f"cached tag: {self._cache[_line][0:self.tag]}")
                print(f"   new tag: {num[0:self.tag]}")
            else:
                print("MISS")
                print(f"cached tag: {self._cache[_line][0:self.tag]}")
                print(f"   new tag: {num[0:self.tag]}")
                self._cache


            # print(num)
            # print(tag)
            # print(line)
        print(self._cache)




            

            

    


def test():
    
    test = Simulator()
    test.preprocessing()
    #test.pick_policy()
    test.kway()   

test()