import csv

#A utility function which reads in a JSON file and converts it into
# a dictionary

# Three main things to note here
# 1. Unless I wanna get _real_ tricky with it, this means these structures are flat
#    which means all of the data I read is going to need to be flat too
# 2. Whenever I get around to figuring out how to create an exe out of the game
#    I gotta make sure those CSVs get into that executable too
# 2.5. That means I'll probably need to rewrite this logic to account for filename
#      fuckery that said packager does
# 3. Every value here is read as a string, which means I will need to provide some sort
#    of conversion keys to whatever calls this to translate values from string
#    into whatever they're actually supposed to be

def read_csv_to_dict(file_name):
    response = []
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        first_line = True
        for row in csv_reader:
            response.append(row.copy())
    return response

