
pigpen_table = {
    'A': '_|', 'B': '|_|', 'C': '|_', 'D': '=|', 'E': '|=|',
    'F': '|=', 'G': '-|', 'H': '|-|', 'I': '|-', 'J': '_.|',  
    'K': '|_.|', 'L': '|._', 'M': '=.|', 'N': '|=.|', 'O': '|.=',
    'P': '-.|', 'Q': '|-.|', 'R': '|.-', 'S': 'V', 'T': '>',
    'U': '<', 'V': '/|', 'W': 'V.', 'X': '>.', 'Y': '>.', 'Z': '/.|'
}

reverse_pigpen = {v: k for k, v in pigpen_table.items()}

def encrypt(message):
    result = ""
    for ch in message.upper():
        if ch == " ":
            result += " "   
        elif ch in pigpen_table:
            result += pigpen_table[ch]
    return result

def decrypt(code):
    result = ""
    temp = ""
    i = 0
    while i < len(code):
        if code[i] == " ":
            result += " "
            i += 1
            continue

        for l in range(4, 0, -1): 
            chunk = code[i:i+l]
            if chunk in reverse_pigpen:
                result += reverse_pigpen[chunk]
                i += l
                break
        else:
            i += 1
    return result


