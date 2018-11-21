# Pur Beurre a Terminal AP using OpenFoodFacts Data
# !/usr/bin/env python3
# # coding: utf-8


from src import run_selector


def main():
    selector = run_selector.SelectSubstitute()
    while 1:
        user_answer = str.lower(
            input("\nPurBeurre vous permet de trouver une alternative plus saine à un produit alimentaire \n"
                  "Rechercher un produit (R)\n"
                  "Consulter l'historique de vos recherches (H)\n"
                  "Quitter (Q)"))
        if user_answer == "r":
            selector.selection()
        elif user_answer == "h":
            selector.show_historic()
        elif user_answer == "q":
            selector.cnx.close()
            break
        else:
            print("Veuillez entrer R, H ou Q")


if __name__ == '__main__':
    main()
