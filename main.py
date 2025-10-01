from Team_Code.Model.model import create, read, update, delete

def main():
    create("Bolsa 1", 100, "transversal", "preto")
    
    produtos = read()  
    print("Produtos:", produtos)  

    update(1, "Bolsa 1.1", 125, "tote", "preto")

    delete(1)

if __name__ == "__main__":
    main()