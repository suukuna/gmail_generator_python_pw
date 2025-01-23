import asyncio
import time
import csv
import json

from fake_useragent import FakeUserAgent

from playwright.async_api import async_playwright, expect
import logging
from unidecode import unidecode
import random

import utils
import settings

first_names = [
    "Adrien", "Agnès", "Alexandre", "Alice", "Amélie", "André", "Anne", "Antoine", "Arthur", "Aurore",
    "Aurélie", "Baptiste", "Basile", "Benoît", "Bernard", "Brigitte", "Camille", "Caroline", "Cédric", "Céline",
    "Charles", "Charlotte", "Chloé", "Claire", "Clément", "Clotilde", "Constance", "Corinne", "Damien", "Daniel",
    "David", "Denis", "Diane", "Dominique", "Edith", "Edmond", "Edouard", "Eléonore", "Elisabeth", "Elodie",
    "Eloïse", "Emile", "Emilie", "Emma", "Estelle", "Etienne", "Eugène", "Eulalie", "Eve", "Félix",
    "Fernand", "Florence", "François", "Françoise", "Frédéric", "Gabriel", "Gabrielle", "Gaspard", "Geneviève", "Georges",
    "Germaine", "Gérard", "Gilbert", "Gisèle", "Guillaume", "Gustave", "Hélène", "Henri", "Hortense", "Hugo",
    "Inès", "Irène", "Jacqueline", "Jacques", "Jean", "Jeanne", "Jérôme", "Jocelyne", "Joséphine", "Jules",
    "Juliette", "Julien", "Justine", "Laetitia", "Laurent", "Laurence", "Léa", "Léon", "Léonie", "Léopold",
    "Louis", "Louise", "Lucas", "Lucie", "Madeleine", "Manon", "Marc", "Margaux", "Marguerite", "Marie",
    "Marine", "Marion", "Marthe", "Martin", "Mathilde", "Matthieu", "Maurice", "Maxime", "Mélanie", "Michel",
    "Monique", "Nathalie", "Nicolas", "Noémie", "Odette", "Odile", "Olivier", "Pascal", "Pascale", "Paul",
    "Paule", "Perrine", "Philippe", "Pierre", "Raphaël", "Raymond", "Rémi", "René", "Roberte", "Roger",
    "Roland", "Rosalie", "Roxane", "Sébastien", "Simone", "Solange", "Sophie", "Stéphane", "Suzanne", "Théodore",
    "Théophile", "Thérèse", "Thomas", "Valérie", "Victor", "Victorine", "Vincent", "Yannick", "Yvette", "Yvonne",
    "Zoé", "Adèle", "Albert", "Alexis", "Alphonse", "Anastasie", "Anatole", "Angèle", "Annick", "Armand",
    "Arnold", "Aude", "Audrey", "Auguste", "Augustin", "Aurélien", "Axel", "Béatrice", "Benoîte", "Blandine",
    "Bruno", "Cécile", "César", "Christelle", "Christian", "Christiane", "Christophe", "Cindy", "Clémence", "Colette",
    "Coralie", "Cyril", "Danièle", "Delphine", "Denise", "Didier", "Dieudonné", "Dominica", "Edgar", "Elian",
    "Elisa", "Emilien", "Emmanuelle", "Esmée", "Estève", "Eudes", "Eugénie", "Fabien", "Fabienne", "Ferdinand",
    "Flavie", "Francine", "Gaston", "Géraldine", "Gilberte", "Gregory", "Guenièvre", "Gustave", "Hector", "Hippolyte",
    "Huguette", "Hyacinthe", "Isabelle", "Jacinthe", "Jean-Baptiste", "Joël", "José", "Jude", "Laure", "Lazare",
    "Lorette", "Ludivine", "Marcel", "Marcellin", "Marianne", "Mathéo", "Maurine", "Mélanie", "Mireille", "Myriam",
    "Nadège", "Nathanaël", "Norbert", "Océane", "Patrice", "Patricia", "Paul-Henri", "Philippine", "Quentin", "Rachel",
    "Raphaëlle", "Raymonde", "Régine", "Rolande", "Roseline", "Sabine", "Sandrine", "Serge", "Sibylle", "Sylvain",
    "Sylvie", "Tanguy", "Thibault", "Urbain", "Valérie", "Victoire", "Violette", "Wilfrid", "Xavier", "Yann"
]
last_names = [
    "Leroy", "Moreau", "Bernard", "Dubois", "Durand", "Lefebvre", "Mercier", "Dupont", "Fournier", "Lambert",
    "Fontaine", "Rousseau", "Vincent", "Muller", "Lefèvre", "Faure", "André", "Gauthier", "Garcia", "Perrin",
    "Robin", "Clément", "Morin", "Nicolas", "Henry", "Roussel", "Mathieu", "Garnier", "Chevalier", "François",
    "Legrand", "Gérard", "Boyer", "Gautier", "Roche", "Roy", "Noel", "Meyer", "Lucas", "Gomez",
    "Martinez", "Caron", "Da Silva", "Lemoine", "Philippe", "Bourgeois", "Pierre", "Renard", "Girard", "Brun",
    "Gaillard", "Barbier", "Arnaud", "Martins", "Rodriguez", "Picard", "Roger", "Schmitt", "Colin", "Vidal",
    "Dupuis", "Pires", "Renaud", "Renault", "Klein", "Coulon", "Grondin", "Leclerc", "Pires", "Marchand",
    "Dufour", "Blanchard", "Gillet", "Chevallier", "Fernandez", "David", "Bouquet", "Gilles", "Fischer", "Roy",
    "Besson", "Lemoine", "Delorme", "Carpentier", "Dumas", "Marin", "Gosselin", "Mallet", "Blondel", "Adam",
    "Durant", "Laporte", "Boutin", "Lacombe", "Navarro", "Langlois", "Deschamps", "Schneider", "Pasquier", "Renaud",
    "Beaufort", "Bellamy", "Benoit", "Boisson", "Bouchard", "Bouchet", "Boulanger", "Boutet", "Bouvier", "Brasseur",
    "Brunet", "Chapelle", "Charbonnier", "Charpentier", "Charron", "Chartier", "Chastain", "Chauveau", "Chauvin", "Cléroux",
    "Cloutier", "Comtois", "Cormier", "Couture", "Dallaire", "Danis", "Daubigny", "Daumier", "Delacroix", "Delaunay",
    "Delhomme", "Delmas", "Demers", "Deniau", "Desrosiers", "Devaux", "Drouin", "Duchemin", "Duclos", "Dufresne",
    "Duguay", "Dumais", "Dumont", "Duplessis", "Dupré", "Durand", "Faubert", "Faucher", "Féraud", "Ferrand",
    "Fleury", "Forest", "Fortin", "Foucher", "Gadbois", "Gagné", "Garneau", "Gascon", "Gauthier", "Genest",
    "Gendron", "Gérin", "Gervais", "Gilbert", "Giraud", "Godin", "Goulet", "Gravel", "Gros", "Guay",
    "Guibert", "Guignard", "Guillot", "Hamelin", "Hardy", "Hébert", "Houde", "Huot", "Jolicoeur", "Jolivet",
    "Joly", "Joncas", "Joubert", "Jubinville", "Lachance", "Laferriere", "Lafontaine", "Lafrenière", "Lagarde", "Lamarche",
    "Lamothe", "Landry", "Langlais", "Lapointe", "Laroche", "Larochelle", "Larose", "Latour", "Lauzon", "Laviolette",
    "Lemoine", "Leroux", "Lessard", "Letellier", "Lussier", "Maillet", "Marchand", "Marquis", "Martel", "Michaud",
    "Montpetit", "Morin", "Nadeau", "Nolet", "Normand", "Paquet", "Parent", "Pellerin", "Pelletier", "Perreault",
    "Pilon", "Poitras", "Poulin", "Provost", "Quenneville", "Racine", "Rancourt", "Raymond", "Renaud", "Rioux"
]

gmail_first_name = random.choice(first_names)
gmail_last_name = random.choice(last_names)

user_number = random.randint(100, 1000)

normalized_first_name = unidecode(gmail_first_name).lower()
normalized_last_name = unidecode(gmail_last_name).lower()

username = f'{normalized_first_name}{normalized_last_name}{user_number}'
password = 'passwd'

birth_day = str(random.randint(1, 28))
birth_month = str(random.randint(1, 12))
year_of_birth = str(random.randint(1980, 2005))

gender_title = str(random.randint(1, 2))

# etu funkciu i spisok nado budet nahuy otsuda, oni lishnyaya

full_gmail_username = f'{username}@gmial.com'
data = [full_gmail_username]  # --> poka chto tak, no tut cherez zapyatuyu budut stoyat cookies


async def data_to_csv():
    with open('data.csv', 'w', newline='') as d:
        writer = csv.writer(d)
        writer.writerow(data)


async def fill_data():
    async with async_playwright() as p:
        if asyncio.iscoroutinefunction(utils.format_proxy):
            proxy = await utils.format_proxy(settings.PROXY)
        else:
            proxy = utils.format_proxy(settings.PROXY)

        if not proxy:
            raise ValueError("Proxy is not correctly formatted or returned None")

        browser = await p.chromium.launch(
            headless=False,
            proxy=proxy,
            slow_mo=settings.SLOW_MO,
            args=['--disable-blink-features=AutomationControlled']
        )

        user_agent = FakeUserAgent().random

        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()

        try:
            await page.goto(
                'https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp'
            )

            await page.locator('#firstName').fill(gmail_first_name)
            await page.locator('#lastName').fill(gmail_last_name)
            await page.click('.VfPpkd-RLmnJb')

            await page.locator('#day').fill(birth_day)
            await page.locator('#month').select_option(birth_month)
            await page.locator('#year').fill(year_of_birth)

            await page.locator('#gender').select_option(gender_title)
            await page.click('.VfPpkd-RLmnJb')

            await page.click('#selectionc3')

            await page.locator('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input').fill(username)
            await page.click('.VfPpkd-RLmnJb')

            await page.locator('//*[@id="passwd"]/div[1]/div/div[1]/input').fill(password)
            await page.locator('//*[@id="confirm-passwd"]/div[1]/div/div[1]/input').fill(password)
            await page.click('.VfPpkd-RLmnJb')

            cookies = await context.cookies()
            cookies_json = json.dumps(cookies)
            data.append(cookies_json)
            await data_to_csv()

            await browser.close()

        except Exception as err:
            print(f'Failed to create account: {err}')

        time.sleep(9999999)


    asyncio.run(data_to_csv())

