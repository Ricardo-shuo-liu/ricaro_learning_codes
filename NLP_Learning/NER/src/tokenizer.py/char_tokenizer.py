# src/tokenizer/char_tokenizer.py
from .base import BaseTokenizer
from ..utils.file_io import load_json
from .vocabulary import Vocabulary

def normalize_text(text):
    """
    规范化文本
    """
    full_width = "０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ！＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～＂"
    half_width = r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&'" + r'()*+,-./:;<=>?@[\]^_`{|}~".'
    mapping = str.maketrans(full_width, half_width)
    return text.translate(mapping)



class CharTokenizer(BaseTokenizer):
    def __init__(self, vocab: Vocabulary):
        self.vocab = vocab

    def text_to_tokens(self, text: str):
        normalized_text = normalize_text(text)
        return list(normalized_text)

    def tokens_to_ids(self, tokens: list[str]):
        return self.vocab.convert_tokens_to_ids(tokens)
    
    def get_pad_id(self) -> int:
        return self.vocab.pad_id