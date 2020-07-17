# coding: utf-8

# Importation of the different module
import sqlite3
import os
import json
import time

# Variable for time the script
debut = time.time()

# Variable for the main boucle
i = 1
i_max = 20

# Variable for the category
count = 0
list_category = []
i_category = 0
name_category = ['hamburgers', 'viennoiseries', 'bonbons', 'mueslis', 'pizzas']

# Main Boucle
while i <= i_max:

    # API request
    os.system("curl -X GET https://fr-en.openfoodfacts.org/category/{}/{}.json --output fichier.json".format(
        name_category[i_category], str(i)))

    # Open the file from API
    try:
        json_data = open('fichier.json')
        data = json.load(json_data)

    except UnicodeDecodeError:
        try:
            json_data.close()
            os.remove('fichier.json')
        except FileNotFoundError:
            pass

    except FileNotFoundError:
        try:
            json_data.close()
            os.remove('fichier.json')
        except FileNotFoundError:
            pass

    # Insert the file from API in variable
    try:
        exterieur = data['products']

        # Boucle for each page of the product in the JSON file
        k = 0
        try:
            while k <= 19:

                bibliotheque = exterieur[k]

                # For each product, enter all this caract in differents variables
                product_name = bibliotheque['product_name_fr']
                product_generic_name = name_category[i_category]
                product_nutriscore = bibliotheque['nutrition_grade_fr']
                product_stores = bibliotheque['stores']
                product_link = bibliotheque['ingredients_text_fr']

                # Catch the fake data of Open Food Facts
                if product_stores != '' and product_name != '':

                    # Modification of wrong caracter for the SQL file
                    h = 0
                    while h < len(product_name):
                        if product_name[h] == "'" or product_name[h] == '"' or product_name[h] == ';':
                            product_name = product_name[:h] + \
                                "," + product_name[h + 1:]
                        h += 1
                    h = 0
                    while h < len(product_stores):
                        if product_stores[h] == "'" or product_stores[h] == '"' or product_stores[h] == ';':
                            product_stores = product_stores[:h] + \
                                "," + product_stores[h + 1:]
                        h += 1
                    h = 0
                    while h < len(product_link):
                        if product_link[h] == "'" or product_link[h] == '"' or product_link[h] == ';':
                            product_link = product_link[:h] + \
                                "," + product_link[h + 1:]
                        h += 1

                    # Make or Open the SQL file
                    fichier = open("test.sql", "a")

                    number = str(i_category + 1)

                    # Creation of new category in the SQL file
                    if product_generic_name not in list_category:
                        fichier.write("INSERT INTO category\nVALUES (" + number + ", '" +
                                      product_generic_name + "');\n\n")

                        list_category.append(product_generic_name)

                    j = 0
                    while j < len(list_category):
                        if product_generic_name == list_category[j]:
                            product_number_category = j + 1
                        j += 1

                    # Insertion of nutriscore with Int()
                    product_nutriscore_number = ''

                    if product_nutriscore == 'a':
                        product_nutriscore_number = '1'
                    elif product_nutriscore == 'b':
                        product_nutriscore_number = '2'
                    elif product_nutriscore == 'c':
                        product_nutriscore_number = '3'
                    elif product_nutriscore == 'd':
                        product_nutriscore_number = '4'
                    else:
                        product_nutriscore_number = '5'

                    # Census of all item listed in the SQL file
                    count += 1
                    # Creation of new product in the SQL file
                    fichier.write("INSERT INTO product\nVALUES (" + str(count) + ", " +
                                  str(product_number_category) + ", '" +
                                  product_name + "', '" +
                                  product_link + "', '" +
                                  product_stores + "', " +
                                  product_nutriscore_number + ", 'False', NULL);\n\n")

                k += 1

        except IndexError:
            pass

        try:
            fichier.close()
        except NameError:
            pass

    except KeyError:
        pass
    except NameError:
        pass

    json_data.close()

    try:
        os.remove('fichier.json')
    except FileNotFoundError:
        pass

    # Modification of the boucle for each category
    if i == i_max:
        i_category += 1
        i = 0

    # Break the boucle after each category
    if i_category >= len(name_category):
        break

    i += 1

# Information at the end of the script
print("Nombre de référence recencée(s) : " + str(count))
print(time.time() - debut)


connection = sqlite3.connect("OpenFoodFacts.db")

cursor = connection.cursor()

# Open the file for create the table of database
my_file = open("Database_MySQL_for_script_python_for_db_file.sql", "r")
all_my_file = my_file.read()

count = 0

# Decomposite the file in multi-query sql
for i in enumerate(all_my_file):
    if i[1] == ";":

        sql_command = all_my_file[count:i[0] + 1]

        count = i[0] + 1

        print(sql_command)

        cursor.execute(sql_command)

my_file.close()

# Open the file create in the begin of the script
my_file = open("test.sql", "r")
all_my_file = my_file.read()

print(type(all_my_file))
count = 0

# Decomposite the file in multi-query sql
for i in enumerate(all_my_file):
    if i[1] == ";":

        sql_command = all_my_file[count:i[0] + 1]

        print(sql_command)

        count = i[0] + 1

        cursor.execute(sql_command)

# Close properly the different file
my_file.close()

connection.close()

# Delete the useless file
os.remove('test.sql')
