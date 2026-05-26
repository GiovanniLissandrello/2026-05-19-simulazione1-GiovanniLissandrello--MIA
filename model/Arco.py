from dataclasses import dataclass

from model.artista import Artista


@dataclass
class Arco:
    u : Artista
    v : Artista
    peso : int
