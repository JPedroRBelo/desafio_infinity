import sys
import yaml
import cv2
import numpy as np
from pydantic import BaseModel
from scipy.spatial.distance import cosine

class InputModel(BaseModel):
    """
    Validação de parâmetros do arquivo YAML de entrada do sistema.

    Atributos:
        image_a (str): Caminho para a primeira imagem.
        image_b (str): Caminho para a segunda imagem.
        output_location (str): Caminho para salvar a imagem concatenada em formato .jpg.
        threshold (float): Valor de limiar para discernir as imagens baseado em distância.
    """
    image_a: str
    image_b: str
    output_location: str
    threshold: float

def load_yaml_file(file_path: str) -> dict:
    """
    Carrega arquivo YAML.

    Args:
        file_path (str): Caminho para o arquivo YAML.

    Returns:
        dict: Dicionário com conteúdo do arquivo YAML.
    """

    try:
        with open(file_path, encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f'Arquivo {file_path} não encontrado!')
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f'Erro ao ler arquivo YAML: {e}')
        sys.exit(1)

def open_image(image_path: str) -> np.ndarray:
    """
    Abre imagem com OpenCV. Note que OpenCV carrega np.ndarray com configuração BGR.

    Args:
        image_path (str): Caminho para a imagem.
    """

    image = cv2.imread(image_path)
    if image is None:
        print(f'Erro ao abrir imagem: {image_path}')
        sys.exit(1)
    return image

def to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Converte uma imagem para escala de cinza.

    Args:
        image (np.ndarray): Imagem em formato BGR carregada com OpenCV.

    Returns:
        np.ndarray: Imagem convertida para escala de cinza.
    """

    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_image

def resize_image(image: np.ndarray, target_size: tuple[int, int] = (256, 256)) -> np.ndarray:
    """
    Redimensiona imagem para o tamanho desejado.

    Args:
        image (np.ndarray): Imagem em grayscale.
        target_size (tuple[int, int], opcional): Tamanho alvo (largura, altura) para redimensionamento.

    Returns:
        np.ndarray: Imagem redimensionada.
    """

    resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)
    return resized_image

def calculate_histogram(image: np.ndarray) -> np.ndarray:
    """
    Calcula o histograma de imagem grayscale.

    Args:
        image (np.ndarray): Imagem grayscale.

    Returns:
        np.ndarray: Histograma com contagem de cada valor de pixel (0 .. 255).
    """

    # [image]: Imagem de entrada
    # [0]: Canal da imagem 
    # None: Máscara da imagem.
    # [256]: Número de intervalos do histograma. 
    # [0, 256]: Intervalo de valores que os pixels podem assumir.
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
    return histogram.flatten()

def preprocess_image(image: np.array):
    """
    Agrega funções de preprocessamento de imagem:
    1. Converte para escala de cinza.
    2. Redimensiona a imagem para 256x256 pixels.

    Args:
        image (np.array): Imagem de entrada como um array NumPy.

    Returns:
        np.array: Imagem pré-processada em escala de cinza e redimensionada para 256x256 pixels.
    """

    preprocessed_image = to_grayscale(image)
    preprocessed_image = resize_image(preprocessed_image, target_size=(256,256))
    return preprocessed_image

def concatenate_images(image_a: np.ndarray, image_b: np.ndarray, axis: int = 1) -> np.ndarray:
    """
    Concatena duas imagens ao longo do eixo especificado.

    Args:
        image_a (np.ndarray): Primeira imagem.
        image_b (np.ndarray): Segunda imagem.
        axis (int): Eixo ao longo do qual as imagens serão concatenadas. 0 = vertical; 1 = horizontal.

    Returns:
        np.ndarray: A imagem resultante da concatenação.
    """

    concatenated_image = np.concatenate((image_a, image_b), axis=axis)
    return concatenated_image

def save_image(image: np.ndarray, output_path: str) -> None:
    """
    Salva imagem em formato JPG.

    Args:
        image (np.ndarray): Imagem a ser salva.
        output_path (str): Caminho para salvar imagem.
    """

    cv2.imwrite(output_path, image)

def main(yaml_path: str):
    """
    Função principal para carregar arquivo YAML, abrir, processar, calcular histograma de imagens e calcular
    distância cosseno dos histogramas, visando verificar similaridade entre os produtos representados na imagem. 

    Args:
        yaml_path (str): Caminho para o arquivo YAML a ser carregado.
    """

    # 1) Abre arquivo YAML
    yaml_file = load_yaml_file(yaml_path)    
    # 2) Valida e carrega arquivo YAML
    input_data = InputModel(**yaml_file)

    # 3) Abre imagens
    image_a = open_image(input_data.image_a)
    image_b = open_image(input_data.image_b)

    # 4) Pré-processa imagens: grayscale e redimensionamento
    pre_image_a = preprocess_image(image_a)
    pre_image_b = preprocess_image(image_b)

    # 5) Calcula histogramas
    histogram_image_a = calculate_histogram(pre_image_a)
    histogram_image_b = calculate_histogram(pre_image_b)

    # 6) Calcula distância cosseno
    # Distância cosseno: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cosine.html
    distance = cosine(histogram_image_a, histogram_image_b)

    # 7) Imprime resultados
    print(f'distância: {distance}')
    if distance < input_data.threshold:
        print('Mesmo produto')
    else:
        print('Produtos diferentes')

    # 8) Concatena e salva imagem concatenada
    concatenated_image = concatenate_images(pre_image_a, pre_image_b)
    save_image(concatenated_image, input_data.output_location)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Insira arquivo YAML de configuração. Exemplo: python solution.py example_1.yaml')
        sys.exit(1)

    input_yaml_file_path = sys.argv[1]
    main(input_yaml_file_path)
