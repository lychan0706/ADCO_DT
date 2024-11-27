from gensim.models.word2vec import Word2Vec
import pandas as pd

sim_model = Word2Vec.load("datas\\w2v_model.bin")

def sim_model(text : str) -> float:
    model = sim_model
    sim : float
    return sim

def remove_spaces():
    with open("ADCO\\adco_data_words.csv", 'r', encoding= "UTF-8") as rfile:
        content = rfile.read()
    with open("ADCO\\adco_data_words.csv", 'w', encoding= "UTF-8") as wfile:
        new_content = ""
        for char in content:
            if char != ' ':
                new_content += char
        wfile.write(new_content)

def main() -> None:
    content : str = ''
    sim : float = sim_model(text = content)
    print(sim)

def test():
    print(sim_model)
    
if (__name__ == "__main__"):
    # main()
    test()