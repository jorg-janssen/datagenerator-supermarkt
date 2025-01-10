
import json
import random
import datetime
import py2sql
from dateutil.relativedelta import relativedelta

AANTAL_JAREN = 2

def __main__():

    # importeer voorbeelddata

    # files met json-objecten
    bron_producten = open('datafiles/producten.json', 'r', encoding='UTF-8')
    json_producten = json.loads(bron_producten.read())
    bron_plaatsen = open('datafiles/plaatsen.json', 'r', encoding='UTF-8')
    plaatsen = json.loads(bron_plaatsen.read())
    bron_achternamen = open ('datafiles/lastnames.json', 'r', encoding='UTF-8')
    achternamen = json.load(bron_achternamen)

    # maak lijst voor geboortedata
    geboortedata = []
    geboortedata_weights = []
    datum = datetime.date.today() - relativedelta(years=80)
    while datum < datetime.date.today() - relativedelta(years=15):
        geboortedata.append(datum)
        geboortedata_weights.append(round(40/(abs(2024-datum.year-48)+1)))
        datum = datum + datetime.timedelta(days=1)

    # declareer arrays voor records
    filialen = []
    klanten = []
    producten = []
    bonnen = []   
    bonregels = [] 

    # zet eerste nummers
    filiaalnr = 100    
    klantnr = 24125
    bonnr = 13254
    productnr = 1459239

    # maak producten list en maak weight-list
    producten_weights = []
    for json_product in json_producten:
        producten_weights.append(json_product['kans'])        
        productnr = productnr + random.randint(1,10)
        product = {}
        product["productnr"] = productnr
        product["omschrijving"] = json_product["omschrijving"]
        product["merk"] = json_product["merk"]
        product["prijs_excl"] = json_product["prijs"]
        product["btw_perc"] = json_product["btw_perc"]
        producten.append(product)

    plaatsen_weights = []
    for plaats in plaatsen:
        plaatsen_weights.append(plaats["inwoners"])

    # MAAK FILIALEN
    for plaats in random.choices(plaatsen, plaatsen_weights, k=5):
        # maak een aantal filialen gebaseerd op inwoneraantal
        for x in range(1, 1+random.randint(int(plaats["inwoners"]/300000), 1+int(plaats["inwoners"]/200000))):
            filiaal = {}
            filiaalnr = filiaalnr + 1
            print(filiaalnr)
            filiaal["filiaalnr"] = filiaalnr
            filiaal["plaats"] = plaats["plaats"]
            filiaal["provincie"] = plaats["provincie"]
            filiaal["land"] = "Nederland"
            filialen.append(filiaal)

            # MAAK BONNEN voor dit filiaal

            #begin ergens in de afgelopen x jaar
            datum = datetime.date.today() - datetime.timedelta(days=random.randrange(100, AANTAL_JAREN*365))
            while datum < datetime.date.today():
                datum = datum + datetime.timedelta(days=random.choices((1,2,3), weights=(100,2,1), k=1)[0])
                if datum.weekday != 6 or random.randint(1,100) < 2:  # meestal niet op zondag
                    for b in range(1, random.randint(50,150)):  # 1+datum.weekday()):
                        bon = {}
                        bonnr = bonnr + random.randint(1,10)
                        bon["bonnr"] = bonnr
                        bon["datum_tijd"] = str(datum) + " " + str(random.randint(8,20)) + ":" + str(random.randint(0,59))
                        bon["filiaal"] = filiaalnr
                        bon["kassanr"] = random.choices(range(1,20), weights=range(20,1,-1), k=1)[0]
                        bonnen.append(bon)

                        # MAAK KLANT OF PAK BESTAANDE KLANT VOOR DEZE BON
                        if len(klanten) < 100 or random.randint(1,3) > 2:
                            #maak nieuwe klant
                            klant = {}
                            klantnr = klantnr + random.randint(1,4)
                            klant["klantnr"] = klantnr
                            klant["achternaam"] = random.choice(achternamen)
                            klant["woonplaats"] = filiaal["plaats"]
                            klant["geboortedatum"] = random.choices(geboortedata, geboortedata_weights, k=1)[0]
                            klanten.append(klant)
                            bon["klant"] = klant["klantnr"]
                        else:
                            if random.randint(1,2) > 1:
                                # neem bestaande klant
                                klant = random.choice(klanten)
                                bon["klant"] = klant["klantnr"]
                            else:
                                # helemaal geen klant
                                bon["klant"] = None

                        # MAAK BONREGELS voor deze bon
                        regelnr = 0
                        for br in range(1,random.choices(range(1,11), weights=range(11,1,-1), k=1)[0]):
                            regelnr = regelnr + 1
                            bonregel = {}
                            bonregel["bon"] = bonnr
                            bonregel["regelnr"] = regelnr
                            product = random.choices(producten, weights=producten_weights, k=1)[0]
                            bonregel["product"] = product["productnr"]
                            bonregel["aantal"] = random.choices(range(1,20), weights=range(20,1,-1), k=1)[0]                            
                            bonregel["prijs_excl"] = product["prijs_excl"]*random.randrange(8,11)*0.1
                            bonregel["btw_perc"] = product["btw_perc"] 

                            bonregels.append(bonregel)

                 

       

    # GENEREER INSERTS
    file = open("inserts.sql", "w", encoding = 'UTF-8')
    file.write("SET NOCOUNT ON\ngo\n") 

    print ("Filiaal:", py2sql.list2sql2file('Filiaal', filialen, file))
    print ("Klant:", py2sql.list2sql2file('Klant', klanten, file)) 
    print ("Product:", py2sql.list2sql2file('Product', producten, file)) 
    print ("Bon:", py2sql.list2sql2file('Bon', bonnen, file)) 
    print ("Bonregel:", py2sql.list2sql2file('Bonregel', bonregels, file)) 
    
    file.close()   
  


__main__()

