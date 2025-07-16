import os

# Caminhos dos arquivos de anotação e diretório de imagens
ANNOTATION_FILES = [
    r'datasets4gb/annotations/test.txt',
    r'datasets4gb/annotations/train.txt',
    r'datasets4gb/annotations/val.txt'
]
LABELS_DIR = r'datasets4gb/annotations/labels'
IMAGES_DIR = r'datasets4gb/images'

# Função para ler nomes de arquivos de anotação

def get_image_names_from_txt(txt_path):
    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    # Considera que cada linha é o caminho relativo da imagem
    return set([os.path.basename(line) for line in lines])

def get_image_names_from_labels(labels_dir):
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    # Assume que o nome do arquivo de label corresponde ao nome da imagem, trocando .txt por .jpg
    return set([f.replace('.txt', '.jpg') for f in label_files])

def get_image_names_from_images(images_dir):
    return set([f for f in os.listdir(images_dir) if f.lower().endswith('.jpg')])

def main():
    # Coleta nomes de imagens dos arquivos de anotação
    images_from_txts = set()
    for txt in ANNOTATION_FILES:
        if os.path.exists(txt):
            images_from_txts.update(get_image_names_from_txt(txt))
        else:
            print(f'Arquivo não encontrado: {txt}')
    # Coleta nomes de imagens dos labels
    images_from_labels = get_image_names_from_labels(LABELS_DIR)
    # Coleta nomes de imagens reais
    images_from_dir = get_image_names_from_images(IMAGES_DIR)

    print(f'Imagens referenciadas nos .txt: {len(images_from_txts)}')
    print(f'Imagens com labels: {len(images_from_labels)}')
    print(f'Imagens no diretório: {len(images_from_dir)}')

    # Checa imagens referenciadas mas não existentes
    missing_in_dir = images_from_txts - images_from_dir
    if missing_in_dir:
        print(f'Imagens referenciadas nos .txt mas não encontradas no diretório:')
        for img in sorted(missing_in_dir):
            print(f'  {img}')
    else:
        print('Todas as imagens referenciadas nos .txt existem no diretório.')

    # Checa labels sem imagem correspondente
    missing_label_in_dir = images_from_labels - images_from_dir
    if missing_label_in_dir:
        print(f'Labels sem imagem correspondente:')
        for img in sorted(missing_label_in_dir):
            print(f'  {img}')
    else:
        print('Todas as labels têm imagem correspondente.')

    # Checa imagens sem label
    missing_label = images_from_dir - images_from_labels
    if missing_label:
        print(f'Imagens sem label correspondente:')
        for img in sorted(missing_label):
            print(f'  {img}')
    else:
        print('Todas as imagens têm label correspondente.')

    # Checa imagens sem referência nos .txt
    not_in_txt = images_from_dir - images_from_txts
    if not_in_txt:
        print(f'Imagens no diretório não referenciadas nos .txt:')
        for img in sorted(not_in_txt):
            print(f'  {img}')
    else:
        print('Todas as imagens do diretório estão referenciadas nos .txt.')

if __name__ == '__main__':
    main()
