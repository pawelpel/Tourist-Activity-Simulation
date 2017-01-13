import requests
import random
import multiprocessing


def test():
    random.seed(random.random())
    how_long = random.randint(0, 4320)
    how_many_people = random.randint(0, 5000)
    whats_the_weather = random.choice(['rainy', 'sunny'])
    month = random.randint(1, 12)

    r = requests.post("http://127.0.0.1:8888", data={'how_long': how_long, 'how_many_people': how_many_people, 'month': month,
                                              'whats_the_weather': whats_the_weather})

    print(r.status_code, r.reason)


def main():
    if __name__ == '__main__':
        jobs = []
        for i in range(10):
            p = multiprocessing.Process(target=test)
            jobs.append(p)
            p.start()


if __name__ == '__main__':
    main()
