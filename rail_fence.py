def encrypt(text, key):
    try:
        num_rails = int(key)
    except:
        raise ValueError("Key sayı olmalı")
    if num_rails < 2:
        raise ValueError("Rail sayısı en az 2 olmalı")
    
    rails = ['' for _ in range(num_rails)]
    rail = 0
    direction = 1 

    for ch in text:
        rails[rail] += ch
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    return ''.join(rails)


def decrypt(text, key):
    try:
        num_rails = int(key)
    except:
        raise ValueError("Key sayı olmalı")
    if num_rails < 2:
        raise ValueError("Rail sayısı en az 2 olmalı")
    
    # zigzak yapıyoruz
    pattern = [0] * len(text)
    rail = 0
    direction = 1
    for i in range(len(text)):
        pattern[i] = rail
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    # raylar için harfleri ayırıyoruz
    rails = ['' for _ in range(num_rails)]
    index = 0
    for r in range(num_rails):
        for i, p in enumerate(pattern):
            if p == r:
                rails[r] += text[index]
                index += 1

    # zigzagdan harfleri alıyoruz
    result = ''
    rail_indices = [0] * num_rails
    for p in pattern:
        result += rails[p][rail_indices[p]]
        rail_indices[p] += 1

    return result
