import random as rand

class Simulator():
    print("yeah")
    def __init__(self, mm_size = 2**32, pg_size = 2**20, cache_size = 2**23):

        
        while True:
            try:
                inpt = input("enter memory size. Must be power of 2 and a valid denomination (_bt, _kb, _mb, _gb)")
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
            print("------")
            num = format(int(rand.randint(0,self.mm_size)), '09b')
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
    test.generate()   

test()