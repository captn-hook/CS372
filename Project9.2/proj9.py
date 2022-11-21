import threading

ranges1 = [
    [1,5],
    [20,22]
]

#[15, 63]
#78

ranges2 = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]

#[165, 15, 825, 3927, 136]
#5068

def rangesum(rang, i, result):
    result[i] = sum(range(rang[0], rang[1] + 1))

def main(ranges):

    result = [0] * len(ranges)

    threads = []

    for i in range(len(ranges)):

        threads.append(threading.Thread(target=rangesum, args=(ranges[i], i, result)))

        threads[i].start()

    for i in threads:
        i.join()

    print(result)
    print(sum(result))

main(ranges1)
main(ranges2)

    