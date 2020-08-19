from concurrent.futures import ThreadPoolExecutor
import pickle
def test(number):
    return(f"Thread received  this {number}")



if __name__ == "__main__":
    x = pickle.loads(open('sus', 'rb'))
    print(type(x))