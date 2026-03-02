import random as rand
import math
import matplotlib.pyplot as plt
import time


class Simulator():    
    def __init__(self):

        self._mm_size = self.bigOlInput("memory")
        self._pg_size = self.bigOlInput("page")
        self._cache_size = self.bigOlInput("cache")
        self.preprocessing()
        self.hits = 0
        self.misses = 0
        self._mapping = self.pick_config()
        if self._mapping == "2":
            self._k = 1
            self._replacement = self.pick_policy()
        elif self._mapping == "3":
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
        self.trace = open("traceFile.txt","w")
        self.trace.write("New File\n")
        self.trace.close()
        self.trace = open("traceFile.txt","a")
        self.trace.write(f"Memory Size: {self._mm_size+1}\nPage Size: {self._pg_size+1}\nCache Size: {self._cache_size+1}\nMapping: {self._mapping}\n")
        

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
                if inpt not in ('1', '2', '3'):
                    print("Pick a config #")
                    continue
                break
            except ValueError:
                print("BAD")
        return inpt
    
    def set_k(self):
        while True:
            try:
                inpt = int(input("Set K"))
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
                inpt = input(f"Pick a policy: \nPolicy 1, prioritize empty slots.\n Policy 2, prioritize least used.\n Policy 3, prioritize the least recently used")
                if inpt not in ('1', '2', '3'):
                    print("Pick a policy #")
                    continue
                break
            except ValueError:
                print("BAD")
        return inpt
                
    def kway(self):
        # Iterate through the sample to generate the number of hits/misses
        for k in range(self._sample):
            self.trace.write("------\n")
            num = format(int(rand.randint(0,self._mm_size)),f'0{self.addr_len}b')
            self.trace.write(f"New Address:      {num}\n")
            _set_size = int((self._cache_size+1) / self._k / (self._pg_size+1)) # Returns the set size in terms of the number of pages

            k_len = len(bin(self._k-1)[2:])
            k_tag = self.addr_len - self.offset - k_len
            _set = int(num[k_tag:k_tag+k_len],2)
            #print(f"k_len: {k_len}")
            #print(k_tag)
            #print(_set_size)
            #print(_set)
            ishit = False
            index = 0
            for i in range(_set):
                index += _set_size
            for x in range(_set_size):
                self.trace.write(f"Compared Address: {self._cache[index+x]}\n")
                if self._cache[index+x] == None:
                    continue
                if self._cache[index+x][0:k_tag] == num[0:k_tag]:
                    self.trace.write("TAG HIT\n")
                    self.hits += 1
                    ishit = True
                    break

                else:
                    self.trace.write("Not hit\n")
            if ishit:
                break
            self.trace.write("MISS\n")
            self.misses += 1
            #if empty replacement policy
            for x in range(_set_size):
                if self._cache[index+x] == None:
                    self._cache[index+x] = num
                    break
        self.trace.write(f"Hits: {self.hits}\n")
        self.trace.write(f"Misses: {self.misses}\n")
        print(self._cache)
                
                    
            



    def direct(self):

        for i in range(self._sample):
            self.trace.write("------\n")
            num = format(int(rand.randint(0,self._mm_size)), f'0{self.addr_len}b')
            self.trace.write(f"New Address:      {num}\n")
            _tag = int(num[0:self.tag],2)
            _line = int(num[self.tag:self.tag+self.line],2)


            #print(f"tag: {_tag}")
            #print(f"line: {_line}")

            if self._cache[_line] == None:
                self._cache[_line] = num
                self.trace.write("NEW\n")
            elif self._cache[_line][0:self.tag] == num[0:self.tag]:
                self.hits +=1                
                self.trace.write(f"cached tag: {self._cache[_line][0:self.tag]}\n")
                self.trace.write("HIT\n")
                #self.trace.write(f"   new tag: {num[0:self.tag]}\n")
            else:
                self.misses += 1
                self.trace.write(f"cached tag: {self._cache[_line][0:self.tag]}\n")
                self.trace.write("MISS\n")
                #self.trace.write(f"   new tag: {num[0:self.tag]}\n")
                self._cache[_line] = num


            # print(num)
            # print(tag)
            # print(line)
        print(self._cache)

    def main(self):
        if self._mapping == "1":
            self.direct()
        elif self._mapping == "2" and self._config == "1": # Fully Associative, Prioritize Empty
            self.kway()
        elif self._mapping == "3" and self._config == "1": # K-Way Set Associative, Prioritize Empty
            self.kway()
        elif self._mapping == "2" and self._config == "2": # Fully Associative, Prioritize Least Used
            self.kway()
        elif self._mapping == "3" and self._config == "2": # K-Way Set Associative, Prioritize Least Used
            self.kway()
        elif self._mapping == "2" and self._config == "1": # Fully Associative, Prioritize Empty
            self.kway()
        elif self._mapping == "3" and self._config == "1": # Fully Associative, Prioritize Least Recently Used
                    self.kway()
        
        


def continuous_ticker(interval=1):
    """Prints a 'tick' continuously."""
    elapsed_time = 0
    test = Simulator()
    hits = []
    misses = []
    time_data = []
    plt.ion()
    try:
        while True:
            test.kway()
            hits.append(test.hits)
            misses.append(test.misses)
            time_data.append(elapsed_time)
            print(f"Tick: {elapsed_time}, Hit/Miss Ratio: {test.hits / test.misses}")
            plt.clf()
            plt.figure(figsize=(10, 5))
            plt.plot(time_data, hits, label='Hits', color='green')
            plt.plot(time_data, misses, label='Misses', color='red')
            plt.title('Hits vs Misses Over Time')
            plt.xlabel('Hits and Misses')
            plt.ylabel('Time in Seconds')
            plt.legend()
            plt.grid(True)
            plt.show()
            elapsed_time += 2
            time.sleep(interval) # ticks every interval seconds
    except KeyboardInterrupt: # ctrl c
        print("\nTicker stopped.")
        test.trace.close()
        plt.ioff()

# Start the ticker
if __name__ == "__main__":
    continuous_ticker(2) # Ticks every 2 seconds


# def test():
#     test = Simulator()
#     #test.pick_policy()
#     test.kway()   

# # test()