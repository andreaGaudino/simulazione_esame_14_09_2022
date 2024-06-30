from dataclasses import dataclass

@dataclass
class Album:
    id: int
    title:str
    durata:float




    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.id} {self.title} {self.durata}"