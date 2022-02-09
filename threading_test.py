#from threading import Thread
#import tensorflow
import multiprocessing as mp
import time



def foo(row):
    sum = 0
    for i in row:
        sum += i
    print(sum)
    return sum

def collect_result(result):
    global results
    results.append(result)

if __name__ == '__main__':
    pool = mp.Pool()
    results = []

    thread_num = 2
    start_time = time.time()
    array = [[i for i in range(10000000)] for j in range(10)]
    # Add more threads here
    ranges = round(len(array) / thread_num)
    for row in array:
        pool.apply_async(foo, args=(row), callback=collect_result)

    # Join all the threads
    pool.close()
    pool.join()
    print(sum(results))

    print("--- %s seconds ---" % (time.time() - start_time))

