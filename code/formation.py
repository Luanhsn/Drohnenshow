class Formation:
    # Feste Zuweisung: Buchstabe → benötigte Drohnenanzahl
    LETTER_DRONE_COUNTS = {
        'A': 11,
        'B': 14,
        'C': 9,
        'D': 12,
        'E': 11,
        'F': 9,
        'G': 11,
        'H': 12,
        'I': 9,
        'J': 12,
        'K': 12,
        'L': 7,
        'M': 13,
        'N': 11,
        'O': 10,
        'P': 11,
        'Q': 14,
        'R': 14,
        'S': 13,
        'T': 8,
        'U': 9,
        'V': 7,
        'W': 13,
        'X': 9,
        'Y': 9,
        'Z': 11
    }

    def get_drone_count(self, letter: str) -> int:
        """
        Gibt die Anzahl der Drohnen für einen bestimmten Buchstaben zurück.
        Groß- und Kleinschreibung wird ignoriert.
        """
        return self.LETTER_DRONE_COUNTS.get(letter.upper(), 0)

    def total_drones_for_word(self, word: str) -> int:
        """
        Berechnet die gesamte Anzahl an Drohnen für ein gegebenes Wort.
        Nicht-Buchstaben werden ignoriert.
        """
        return sum(self.get_drone_count(c) for c in word if c.isalpha())

    def __str__(self):
        return "\n".join(f"{letter}: {count} Drohnen" for letter, count in self.LETTER_DRONE_COUNTS.items())
