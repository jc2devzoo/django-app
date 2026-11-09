# biblioteca/utils.py
import re
import pytesseract
from PIL import Image

# Se o Tesseract não estiver no PATH (Windows), descomente e ajuste:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extrair_cdu_cdi(arquivo_imagem):
    """
    Recebe um InMemoryUploadedFile / FieldFile do Django,
    abre a imagem, aplica OCR e extrai CDU e CDI via regex.
    """
    arquivo_imagem.seek(0)
    imagem = Image.open(arquivo_imagem)

    texto = pytesseract.image_to_string(imagem, lang='por')

    cdu = re.search(r'CDU\s*([\d\.\-]+)', texto, re.IGNORECASE)
    cdi = re.search(r'CDI\s*([\d\.\-]+)', texto, re.IGNORECASE)

    return (
        cdu.group(1).strip() if cdu else '',
        cdi.group(1).strip() if cdi else '',
    )