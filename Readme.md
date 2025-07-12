
# Structure directories FASDD
```
FS_DETECTION
└───data
    ├───FASDD_CV
    │   ├───annotations
    │   │   └───YOLO_CV
    │   │       └───labels
    │   └───images 
    └───FASDD_UAV
        ├───annotations
        │   └───YOLO_UAV
        │       └───labels
```

## Contagem de Arquivos por Dataset e Tipo

### FASDD_CV
- **bothFireAndSmoke**: 20151 arquivos
- **fire**: 12550 arquivos
- **neitherFireNorSmoke**: 39199 arquivos
- **smoke**: 23414 arquivos
Total de arquivos em FASDD_CV: 95314

### FASDD_UAV
- **bothFireAndSmoke**: 7821 arquivos
- **fire**: 210 arquivos
- **neitherFireNorSmoke**: 11986 arquivos
- **smoke**: 5080 arquivos
Total de arquivos em FASDD_UAV: 25097

# Detalhes da estrutura pra treino CV e UAV
```
data/FASDD_MERGED/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```


### FASDD_CV
```
FASDD_CV/
├── annotations/
│   └── YOLO_CV/
│       ├── train.txt (referências a imagens de todas as classes)
│       ├── val.txt (referências a imagens de todas as classes)
│       ├── test.txt (referências a imagens de todas as classes)
│       └── labels/
│           ├── fire_*.txt
│           ├── smoke_*.txt
│           ├── bothFireAndSmoke_*.txt
│           └── neitherFireNorSmoke_*.txt
└── images/
    ├── fire_*.jpg (12,550 arquivos)
    ├── smoke_*.jpg (23,414 arquivos)
    ├── bothFireAndSmoke_*.jpg (20,151 arquivos)
    └── neitherFireNorSmoke_*.jpg (39,199 arquivos)
```

#### Classes:
- **fire** (fogo)
- **smoke** (fumaça) 
- **bothFireAndSmoke** (ambos fogo e fumaça)
- **neitherFireNorSmoke** (nem fogo nem fumaça)

**Total de arquivos em FASDD_CV**: 95,314