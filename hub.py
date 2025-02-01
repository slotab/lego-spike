from types import SimpleNamespace

port = {
    "A":0,
    "B":0,
    "C":0,
    "D":0,
    "E":0,
    "F":0,
}


light_matrix = SimpleNamespace(
    write = lambda txt: print(f"Pouet: {txt}")
)