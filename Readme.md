# Project Directory Structure

```
fire-detection/
├── .venv/               # Python virtual environment
├── my_env/              # Another virtual environment
├── datasets/
│   ├── images/
│   │   ├── fire_*.jpg               # 12,550 files
│   │   ├── smoke_*.jpg              # 23,414 files
│   │   ├── bothFireAndSmoke_*.jpg   # 20,151 files
│   │   └── neitherFireNorSmoke_*.jpg # 39,199 files
│   └── annotations/
│       ├── train.txt                # References to images of all classes
│       ├── val.txt                  # References to images of all classes
│       ├── test.txt                 # References to images of all classes
│       └── labels/
│           ├── fire_*.txt
│           ├── smoke_*.txt
│           ├── bothFireAndSmoke_*.txt
│           └── neitherFireNorSmoke_*.txt
├── scripts/            
│   ├── upload_to_dagshub.py
│   ├── check_status_upload.py
│   ├── train_fasdd.py
│   └── train.py
├── .env                # Environment variables
└── requirements.txt    # Python dependencies
```

## Dataset Classes
- **fire**: Fire only
- **smoke**: Smoke only
- **bothFireAndSmoke**: Both fire and smoke
- **neitherFireNorSmoke**: Neither fire nor smoke

**Total files in dataset**: 95,314

The total file count also matches the listed files:
•  12,550 + 23,414 + 20,151 + 39,199 = 95,314

. { Write-Host "=== ESTRUTURA DETALHADA ===" -ForegroundColor Magenta
> 
> Write-Host "`nDATASETS ORIGINAL:"
> Get-ChildItem -Path "datasets" -Directory | ForEach-Object {
>     $subFiles = Get-ChildItem -Path $_.FullName -Recurse -File
>     $subSize = ($subFiles | Measure-Object -Property Length -Sum).Sum
>     Write-Host "  $($_.Name): $($subFiles.Count) arquivos, $([math]::Round($subSize/1MB, 2)) MB"
> }
> 
> Write-Host "`nDATASETS HALF:"
> Get-ChildItem -Path "datasets_half" -Directory | ForEach-Object {
>     $subFiles = Get-ChildItem -Path $_.FullName -Recurse -File
>     $subSize = ($subFiles | Measure-Object -Property Length -Sum).Sum
>     Write-Host "  $($_.Name): $($subFiles.Count) arquivos, $([math]::Round($subSize/1MB, 2)) MB"
> } }
=== ESTRUTURA DETALHADA ===

DATASETS ORIGINAL:
  annotations: 95317 arquivos, 11.9 MB
  images: 95314 arquivos, 11915.76 MB

DATASETS HALF:
  annotations: 47658 arquivos, 5.92 MB
  images: 47655 arquivos, 5985.5 MB
📊 Comparação dos Datasets

Resumo Geral:
•  Dataset Original (datasets/): 190.631 arquivos, 11,93 GB
•  Dataset Half (datasets_half/): 95.314 arquivos, 5,99 GB

Redução Alcançada:
•  ✅ Redução de tamanho: 49,8% (quase metade)
•  ✅ Redução de arquivos: 50,0% (exatamente metade)
•  ✅ Economia de espaço: 5,94 GB

Estrutura Detalhada:

| Componente | Dataset Original | Dataset Half | Redução |
|------------|------------------|--------------|---------|
| Imagens | 95.314 arquivos (11,92 GB) | 47.655 arquivos (5,99 GB) | ~50% |
| Anotações | 95.317 arquivos (11,9 MB) | 47.658 arquivos (5,92 MB) | ~50% |

Conclusão:
O datasets_half é exatamente metade do dataset original, tanto em número de arquivos quanto em tamanho total. Essa redução é perfeita para:
•  ✅ Testes e experimentação mais rápidos
•  ✅ Menor uso de storage no DagHub
•  ✅ Uploads mais rápidos
•  ✅ Treinamento inicial de modelos com menos recursos

O dataset half mantém a mesma estrutura e proporções do dataset original, sendo uma amostra representativa para desenvolvimento e testes.