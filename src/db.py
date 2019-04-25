import json

class DataBase(object):
    #Inits the database with a provided json
    def __init__(self, file):
        self.file = file
        with open(file, 'r+') as json_file:
            self.data = json.load(json_file)

    #Returns a name, a picture and a price for the provided codes (or None if not found)
    def fetch(self, code):
        if code in self.data.keys():
            return self.data[code]
        return ["", "", ""]

    #Saves the database
    def save(self):
        with open(self.file, 'w+') as json_file:
            json.dump(self.data, json_file, indent=2)

    #Add an element to the database
    def add(self, name, code, price, pic="imgs/products/Not_Found.png"):
        self.data[code] = [name, price, pic]
