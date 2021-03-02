# Function to process numbers from 1 to 999
# can receive singular label and plural label (singular for number 1, plural for the rest)
# supress_value is a boolean that defines if the number has to be printed in singular labels
# example: supress_value = True -> singular_label = mil -> number = 1
# Printed value will be "mil" instead of the expected "um mil"
def processNumber(number, numbers_dict, label_singular, label_plural, supress_value):
    # Calculate number_as_integer and len_number for the rest of the process
    number_as_integer = int(number)
    len_number = len(number)
    
    # Check if the received number is already defined in the dictionary and doesn't need extra processing
    # Example: number = 100 -> printed value will be "cem" + label
    if (number_as_integer in numbers_dict):
        # Special treatment for 1 values, using singular label and the possibility to supress value
        if (number_as_integer == 1):
            if (supress_value):
                print(label_singular, end = "")
            else:
                print(numbers_dict[number_as_integer] + " " + label_singular, end="")
        # Print number + label
        else:
            print(numbers_dict[number_as_integer] + " " + label_plural, end="")

        # Return because number doesn't need extra processing
        return

    # Define isfirstnumber to print "e" between values
    isfirstnumber = True

    # If number has 3 figures
    if (len_number >= 3):
        # calculate value for centena -> Example: 356
        # First figure is 3, so we have to write "trezentos"
        centena = int(number[len_number - 3]) * 100

        # Special treamente por "centenas" with 1 value
        # We have to write "cento" instead of "cem"
        if (centena == 100):
            print("cento", end = "")
            isfirstnumber = False
        # Ignore centenas with 0 value, they don't matter
        elif (centena != 0):
            print(numbers_dict[centena], end = "")
            isfirstnumber = False

    # If number has 2 or more figures
    if (len_number >= 2):
        # We have to check if the number with 2 figures is already defined in dict
        # Example: 913 -> 13 is defined in dict and has to be written as "treze"
        if (int(number[len_number - 2:]) in numbers_dict):
            # Only print "e" if another number has already been written
            if (not isfirstnumber):
                print(" e ", end="")
            # Print number defined in dict and return, processing in finished
            print(numbers_dict[int(number[1:])] + " " + label_plural, end="")
            return

        # calculate value for dezena -> Example: 56
        # First figure is 5, so we have to write "cinquenta"
        dezena = int(number[len_number - 2]) * 10

        # Ignore dezenas with 0 value
        if (dezena != 0):
            # Only print "e" if another number has already been written
            if (not isfirstnumber):
                print(" e ", end="")
            else:
                isfirstnumber = False
            print(numbers_dict[dezena], end = "")

    # If number has 1 or more figures
    if (len_number >= 1):
        # calculate value for unidade -> Example: 356
        # last figure is 6, so we have to write "seis"
        unidade = int(number[len_number - 1])

        # Ignore unidades with 0 value
        if (unidade != 0):
            # Only print "e" if another number has already been written
            if (not isfirstnumber):
                print(" e ", end="")
            print(numbers_dict[unidade], end = "")

    # Print label in the end of number processing
    print(" " + label_plural, end="")


# Define all base values for numbers
numbers_dict =  {
    1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco",
    6: "seis", 7: "sete", 8: "oito", 9: "nove",
    10: "dez", 11: "onze", 12: "doze", 13: "treze", 14: "catorze", 15: "quinze",
    16: "dezesseis", 17: "dezessete", 18: "dezoito", 19: "dezenove",
    20: "vinte", 30: "trinta", 40: "quarenta", 50: "cinquenta",
    60: "sessenta", 70: "setenta", 80: "oitenta", 90: "noventa",
    100: "cem", 200: "duzentos", 300: "trezentos", 400: "quatrocentos",
    500: "quinhentos", 600: "seiscentos", 700: "setecentos", 800: "oitocentos", 900: "novecentos"
}

# Read the number in the XXXXXXXXX,YY format
print("Digite o número: ", end="")
number = input()

# If number doesn't have a comma print message and exit 
if (',' not in number):
    print("Número fora do formato esperado XXXXXXXXX,YY!")
    exit()

# Split number in reais (before comma) and cents (after comma)
parts = number.split(",")
reais = parts[0]
cents = parts[1]

# If we have more or less numbers than allowed in the reais position, print error 
if (len(reais) < 1 or len(reais) > 9):
    print("Quantidade de digitos antes da virgula invalida!")
    exit()

# If we have more or less numbers than allowed in the cents position, print error 
if (len(cents) != 2):
    print("Quantidade de digitos depois da virgula invalida!")
    exit()

# Using the followin logic for number split ->
# A given number 107945,30 has 6 numbers before comma and 2 after comma
# The number can be splitted in groups of 3, so we only have to write numbers from 0 to 999
# 107 -> cento e sete | 945 -> novecentos e quarenta e cinco | 30 -> trinta
# Full number: cento e sete mil e novecentos e quarenta e cinco reais e trinta centavos


# Get the "milhão" number set, if they are available
if (len(reais) > 6):
    # Calculate the indexes for start and end of the "milhão" number set
    string_start = len(reais) - 9 if len(reais) - 9 >= 0 else 0
    string_end = len(reais) - 6
    part = reais[string_start:string_end]

    # Only try to process this part if it's integer value is different than 0
    if (int(part) != 0):
        processNumber(part, numbers_dict, "milhão", "milhões", False)

        # Only print an "e" if the rest of the number parts has any valid value (different than 0)
        if (int(reais[string_end:]) != 0):
            print(" e ", end="")
        # If there isn't any valid value in the rest of the number close "reais" here
        else:
            print(" de reais", end="")

if (len(reais) > 3):
    # Calculate the indexes for start and end of the "mil" number set
    string_start = len(reais) - 6 if len(reais) - 6 >= 0 else 0
    string_end = len(reais) - 3
    part = reais[string_start:string_end]

    # Only try to process this part if it's integer value is different than 0
    if (int(part) != 0):
        processNumber(part, numbers_dict, "mil", "mil", True)

        # Only print an "e" if the rest of the number parts has any valid value (different than 0)
        if (int(reais[string_end:]) != 0):
            print(" e ", end="")
        # If there isn't any valid value in the rest of the number close "reais" here
        else:
            print(" reais", end="")

if (len(reais) > 0):
    # Calculate the indexes for start and end of the "centenas" number set
    string_start = len(reais) - 3 if len(reais) - 3 >= 0 else 0
    string_end = len(reais)
    part = reais[string_start:string_end]

    # Only try to process this part if it's integer value is different than 0
    if (int(part) != 0):
        processNumber(part, numbers_dict, "real", "reais", False)

# Number doesn't have any valid values before and after the comma
if (int(reais) == 0 and int(cents) == 0):
    print("0 reais", end="")

# "cents" part has valid values (different than 0)
if (int(cents) != 0):
    # Only print an "e" before cents value if there was any valid value before comma
    if (int(reais) != 0):
        print(" e ", end="")
    processNumber(cents, numbers_dict, "centavo", "centavos", False)

print()