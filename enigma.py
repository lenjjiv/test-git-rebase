# Скрипт энигмы — простая реализация шифратора Энигмы на Python

class EnigmaRotor2:
    def __init__(self, wiring, notch, ring_setting=0):
        self.wiring = wiring
        self.notch = notch
        self.ring_setting = ring_setting
        self.position = 0

    def encode_forward(self, c):
        idx = (ord(c) - ord('A') + self.position - self.ring_setting) % 26
        encoded = self.wiring[idx]
        return chr((ord(encoded) - ord('A') - self.position + self.ring_setting + 26) % 26 + ord('A'))

    def encode_backward(self, c):
        idx = (ord(c) - ord('A') + self.position - self.ring_setting) % 26
        encoded = chr((self.wiring.index(chr(idx + ord('A'))) - self.position + self.ring_setting + 26) % 26 + ord('A'))
        return encoded

    def step(self):
        self.position = (self.position + 1) % 26
        return self.at_notch()

    def at_notch(self):
        return chr((self.position + ord('A')) % 26 + ord('A')) == self.notch

class EnigmaReflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, c):
        idx = ord(c) - ord('A')
        return self.wiring[idx]

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
    rotor_I = EnigmaRotor1("EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch='Q')
    rotor_II = EnigmaRotor1("AJDKSIRUXBLHWTMCQGZNPYFVOE", notch='E')
    rotor_III = EnigmaRotor1("BDFHJLCPRTXVZNYEIWGAKMUSQO", notch='V')
    reflector_B = EnigmaReflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    enigma = EnigmaMachine([rotor_I, rotor_II, rotor_III], reflector_B)

    # Зашифровать сообщение
    message = "ПРИВЕТ МИР"
    # Преобразуем к латинице для примера (Enigma работала только с латиницей)
    message_latin = "PRIVET MIR"
    encrypted = enigma.encrypt(message_latin)
    print("Зашифрованное сообщение:", encrypted)
