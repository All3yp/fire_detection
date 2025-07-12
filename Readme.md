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