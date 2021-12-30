class quadrato:
    def __init__(self, lato):
        self.lato = lato
    
    def perimetro(self):
        return self.lato * 4
    
    def area(self):
        return self.lato ** 2