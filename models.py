from dataclasses import dataclass

@dataclass
class Bolag:
    id: int
    bolagsnamn: str
    nuvarande_kurs: float
    omsattning_i_ar: float
    omsattning_nasta_ar: float
    antal_aktier: int
    ps1: float
    ps2: float
    ps3: float
    ps4: float
    ps5: float
