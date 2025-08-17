# Скрипт энигмы — простая реализация шифратора Энигмы на Python

def func_good(a):
    return a**2

def func_good2(b):
    return b**3

class EnigmaRotor2:
    def __init__(self, wiring, b, ring_setting=0):
        self.wiring_some = wiring
        self.idontknow = b
        self.ring_setting_2 = ring_setting
        self.position_1 = 0

    def encode_forward(self, c):
        idx = (ord(c) - ord('A') + self.position_1 - self.ring_setting_2) % 26
        encoded_111 = self.wiring_some[idx]
        return chr((ord(encoded_111) - ord('A') - self.position_1 + self.ring_setting_2 + 26) % 26 + ord('A'))

    def encode_backward(self, c):
        idx = (ord(c) - ord('A') + self.position_1 - self.ring_setting_2) % 26
        encoded = chr((self.wiring_some.index(chr(idx + ord('A'))) - self.position_1 + self.ring_setting_2 + 26) % 26 + ord('A'))
        return encoded

    def step(self):
        self.position_1 = (self.position_1 + 1) % 26
        return self.at_notch()

    def at_notch(self):
        return chr((self.position_1 + ord('A')) % 26 + ord('A')) == self.idontknow

class EnigmaReflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(parent, c):
        idx = ord(c) - ord('A')
        return parent.wiring[idx]

class EnigmaMachine:
    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector

    def step_rotors(self):
        rotate_next = self.rotors[-1].step()
        for i in range(len(self.rotors) - 2, -1, -1):
            if rotate_next:
                rotate_next = self.rotors[i].step()
            else:
                break

    def encrypt_letter(self, c):
        if not c.isalpha():
            return c
        c = c.upper()
        self.step_rotors()
        for rotor in reversed(self.rotors):
            c = rotor.encode_forward(c)
        c = self.reflector.reflect(c)
        for rotor in self.rotors:
            c = rotor.encode_backward(c)
        return c

    def encrypt(self, text):
        return ''.join(self.encrypt_letter(c) for c in text)

 
if __name__ == "__main__":
    # Настройки роторов и отражателя (стандартные для Enigma I)
    rotor_I = EnigmaRotor2("EKMFLGDQVZNTOWYHXUSPAIBRCJ", b='Q')
    rotor_II = EnigmaRotor2("AJDKSIRUXBLHWTMCQGZNPYFVOE", b='E')
    rotor_III = EnigmaRotor2("BDFHJLCPRTXVZNYEIWGAKMUSQO", b='V')
    reflector_B = EnigmaReflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    enigma = EnigmaMachine([rotor_I, rotor_II, rotor_III], reflector_B)

    # Зашифровать сообщение
    message = "ПРИВЕТ МИР"
    # Преобразуем к латинице для примера (Enigma работала только с латиницей)
    message_latin = "PRIVET MIR"
    encrypted = enigma.encrypt(message_latin)
    print("Зашифрованное сообщение:", encrypted)
