import numpy as np
from numpy import dot
from numpy.linalg import norm

def cossim(A : np.array, B : np.array) -> np.float64:
    return dot(A, B) / (norm(A) * norm(B))

def doc_sim(text : str) -> float:
    pass

def main() -> None:
    
    arr1 : np.array = np.array([1, 2, 3, 4])
    arr2 : np.array = np.array([1, 3, 4, 6])
    sim = cossim(arr1, arr2)

    print(f"{sim = }, type = {type(sim)}")

def foo():
    with open("ADCO\\adco_data_words.csv", 'r', encoding= "UTF-8") as rfile:
        content = rfile.read()
    with open("ADCO\\adco_data_words.csv", 'w', encoding= "UTF-8") as wfile:
        new_content = ""
        for char in content:
            if char != ' ':
                new_content += char
        wfile.write(new_content)

if (__name__ == "__main__"):
    # main()