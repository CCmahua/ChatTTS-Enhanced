import re
import jieba.posseg as pseg
from modules.zh_normalization import TextNormalizer
splits = {"，", "。", "？", "！", ",", ".", "?", "!", "~", ":", "：", "—", "…", }

def cut2(inp, segment_length):
    inp = inp.strip("\n")
    inps = split(inp)
    if len(inps) < 2:
        return [inp]
    opts = []
    summ = 0
    tmp_str = ""
    for i in range(len(inps)):
        summ += len(inps[i])
        tmp_str += inps[i]
        if summ >= segment_length:
            summ = 0
            opts.append(tmp_str)
            tmp_str = ""
    if tmp_str != "":
        opts.append(tmp_str)
    if len(opts) > 1 and len(opts[-1]) < segment_length:
        opts[-2] = opts[-2] + opts[-1]
        opts = opts[:-1]
    return opts

def split(todo_text):
    todo_text = todo_text.replace("……", "。").replace("——", "，")
    if todo_text[-1] not in splits:
        todo_text += "。"
    i_split_head = i_split_tail = 0
    len_text = len(todo_text)
    todo_texts = []
    while 1:
        if i_split_head >= len_text:
            break
        if todo_text[i_split_head] in splits:
            i_split_head += 1
            todo_texts.append(todo_text[i_split_tail:i_split_head])
            i_split_tail = i_split_head
        else:
            i_split_head += 1
    return todo_texts


# 数字转为中文读法
def num_to_chinese(num):
    num_str = str(num)
    chinese_digits = "零一二三四五六七八九"
    units = ["", "十", "百", "千"]
    big_units = ["", "万", "亿", "兆"]
    result = ""
    zero_flag = False  # 标记是否需要加'零'
    part = []  # 存储每4位的数字

    # 将数字按每4位分组
    while num_str:
        part.append(num_str[-4:])
        num_str = num_str[:-4]

    for i in range(len(part)):
        part_str = ""
        part_zero_flag = False
        for j in range(len(part[i])):
            digit = int(part[i][j])
            if digit == 0:
                part_zero_flag = True
            else:
                if part_zero_flag or (zero_flag and i > 0 and not result.startswith(chinese_digits[0])):
                    part_str += chinese_digits[0]
                    zero_flag = False
                    part_zero_flag = False
                # 如果是十位并且是1，特殊处理
                if len(part[i]) == 2 and digit == 1 and j == 0:
                    part_str += units[len(part[i]) - j - 1]
                else:
                    part_str += chinese_digits[digit] + units[len(part[i]) - j - 1]
        if part_str.endswith("零"):
            part_str = part_str[:-1]  # 去除尾部的'零'
        if part_str:
            zero_flag = True

        if i > 0 and not set(part[i]) <= {'0'}:  # 如果当前部分不全是0，则加上相应的大单位
            result = part_str + big_units[i] + result
        else:
            result = part_str + result

    # 处理输入为0的情况或者去掉开头的零
    result = result.lstrip(chinese_digits[0])
    if not result:
        return chinese_digits[0]
    return result





# 数字转为英文读法
def num_to_english(num):
    num_str = str(num)
    # English representations for numbers 0-9
    english_digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    units = ["", "ten", "hundred", "thousand"]
    big_units = ["", "thousand", "million", "billion", "trillion"]
    result = ""
    need_and = False  # Indicates whether 'and' needs to be added
    part = []  # Stores each group of 4 digits
    is_first_part = True  # Indicates if it is the first part for not adding 'and' at the beginning

    # Split the number into 3-digit groups
    while num_str:
        part.append(num_str[-3:])
        num_str = num_str[:-3]

    part.reverse()

    for i, p in enumerate(part):
        p_str = ""
        digit_len = len(p)
        if int(p) == 0 and i < len(part) - 1:
            continue

        hundreds_digit = int(p) // 100 if digit_len == 3 else None
        tens_digit = int(p) % 100 if digit_len >= 2 else int(p[0] if digit_len == 1 else p[1])

        # Process hundreds
        if hundreds_digit is not None and hundreds_digit != 0:
            p_str += english_digits[hundreds_digit] + " hundred"
            if tens_digit != 0:
                p_str += " and "

        # Process tens and ones
        if 10 < tens_digit < 20:  # Teens exception
            teen_map = {
                11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
                16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"
            }
            p_str += teen_map[tens_digit]
        else:
            tens_map = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
            tens_val = tens_digit // 10
            ones_val = tens_digit % 10
            if tens_val >= 2:
                p_str += tens_map[tens_val] + (" " + english_digits[ones_val] if ones_val != 0 else "")
            elif tens_digit != 0 and tens_val < 2:  # When tens_digit is in [1, 9]
                p_str += english_digits[tens_digit]

        if p_str and not is_first_part and need_and:
            result += " and "
        result += p_str
        if i < len(part) - 1 and int(p) != 0:
            result += " " + big_units[len(part) - i - 1] + ", "

        is_first_part = False
        if int(p) != 0:
            need_and = True

    return result.capitalize()


def get_lang(text):
    # 定义中文标点符号的模式
    chinese_punctuation = "[。？！，、；：‘’“”（）《》【】…—\u3000]"
    # 使用正则表达式替换所有中文标点为""
    cleaned_text = re.sub(chinese_punctuation, "", text)
    # 使用正则表达式来匹配中文字符范围
    return "zh" if re.search('[\u4e00-\u9fff]', text) is not None else "en"

def fraction_to_words(match):
    numerator, denominator = match.groups()
    # 这里只是把数字直接拼接成了英文分数的形式, 实际上应该使用某种方式将数字转换为英文单词
    # 例如: "1/2" -> "one half", 这里仅为展示目的而直接返回了 "numerator/denominator"
    return numerator + " over " + denominator


# 数字转为中英文读法
def num2text(text):
    lang = get_lang(text)
    if lang == 'zh':
        numtext = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        point = '点'

        text = re.sub(r'(\d+)\s*\+', r'\1 加', text)
        text = re.sub(r'(\d+)\s*\-', r'\1 减', text)
        text = re.sub(r'(\d+)\s*[\*x]', r'\1 乘', text)
        text = re.sub(r'(\d+)\s*/\s*(\d+)', r'\2分之\1', text)

    # 英文字符长度超过一半
    else:
        numtext = [' zero ', ' one ', ' two ', ' three ', ' four ', ' five ', ' six ', ' seven ', ' eight ', ' nine ']
        point = ' point '
        text = re.sub(r'(\d+)\s*\+', r'\1 plus ', text)
        text = re.sub(r'(\d+)\s*\-', r'\1 minus ', text)
        text = re.sub(r'(\d+)\s*[\*x]', r'\1 times ', text)
        text = re.sub(r'(\d+)\s*/\s*(\d+)', fraction_to_words, text)

    # 取出数字 number_list= [('1000200030004000.123', '1000200030004000', '123'), ('23425', '23425', '')]
    number_list = re.findall('((\d+)(?:\.(\d+))?%?)', text)
    if len(number_list) > 0:
        # dc= ('1000200030004000.123', '1000200030004000', '123','')
        for m, dc in enumerate(number_list):
            if len(dc[1]) > 16:
                continue
            int_text = num_to_chinese(dc[1]) if lang == 'zh' else num_to_english(dc[1])
            if len(dc) > 2 and dc[2]:
                int_text += point + "".join([numtext[int(i)] for i in dc[2]])
            if dc[0][-1] == '%':
                int_text = ('百分之' if lang == 'zh' else ' the pronunciation of ') + int_text
            text = text.replace(dc[0], int_text)
    if lang == 'zh':
        text = text.replace('1', '一').replace('2', '二').replace('3', '三').replace('4', '四').replace('5', '五').replace(
            '6', '六').replace('7', '七').replace('8', '八').replace('9', '九').replace('0', '零').replace('+', '加').replace(
            '÷', '除以').replace('=', '等于')
    else:
        text = text.replace('1', ' one ').replace('2', ' two ').replace('3', ' three ').replace('4', ' four ').replace('5',
                                                                                                                       ' five ').replace(
            '6', ' six ').replace('7', 'seven').replace('8', ' eight ').replace('9', ' nine ').replace('0',
                                                                                                       ' zero ').replace(
            '=', ' equals ')

    # 去除所有空格
    text = text.replace(" ", "")
    return text

def fraction_to_words(match):
    numerator, denominator = match.groups()
    # 这里只是把数字直接拼接成了英文分数的形式, 实际上应该使用某种方式将数字转换为英文单词
    # 例如: "1/2" -> "one half", 这里仅为展示目的而直接返回了 "numerator/denominator"
    return numerator + " over " + denominator



# ref https://github.com/6drf21e/ChatTTS_colab/blob/main/utils.py

def replace_tokens(text):
    remove_tokens = ['UNK']
    for token in remove_tokens:
        text = re.sub(r'\[' + re.escape(token) + r'\]', '', text)

    tokens = ['uv_break', 'laugh','lbreak']
    for token in tokens:
        text = re.sub(r'\[' + re.escape(token) + r'\]', f'uu{token}uu', text)
        text = text.replace('_', '')
    return text

def restore_tokens(text):
    tokens = ['uvbreak', 'laugh', 'UNK', 'lbreak']
    for token in tokens:
        text = re.sub(r'uu' + re.escape(token) + r'uu', f'[{token}]', text)
    text = text.replace('[uvbreak]', '[uv_break]')
    return text




def split_text(text, min_length=60):
    """
    将文本分割为长度不小于min_length的句子
    :param text:
    :param min_length:
    :return:
    """
    # 短句分割符号
    sentence_delimiters = re.compile(r'([。？！\.]+)')
    # 匹配多个连续的回车符 作为段落点 强制分段
    paragraph_delimiters = re.compile(r'(\s*\n\s*)+')

    paragraphs = re.split(paragraph_delimiters, text)

    result = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            continue  # 跳过空段落
        # 小于阈值的段落直接分开
        if len(paragraph.strip()) < min_length:
            result.append(paragraph.strip())
            continue
        # 大于的再计算拆分
        sentences = re.split(sentence_delimiters, paragraph)
        current_sentence = ''

        for sentence in sentences:
            if re.match(sentence_delimiters, sentence):
                current_sentence += sentence.strip() + ''
                if len(current_sentence) >= min_length:
                    result.append(current_sentence.strip())
                    current_sentence = ''
            else:
                current_sentence += sentence.strip()

        if current_sentence:
            if len(current_sentence) < min_length and len(result) > 0:
                result[-1] += current_sentence
            else:
                result.append(current_sentence)

    if detect_language(text[:1024]) == "zh":
        result = [normalize_zh(_.strip()) for _ in result if _.strip()]
    else:
        result = [normalize_en(_.strip()) for _ in result if _.strip()]
    return result


def detect_language(sentence):
    # ref: https://github.com/2noise/ChatTTS/blob/main/ChatTTS/utils/infer_utils.py#L55
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]')
    english_word_pattern = re.compile(r'\b[A-Za-z]+\b')

    chinese_chars = chinese_char_pattern.findall(sentence)
    english_words = english_word_pattern.findall(sentence)

    if len(chinese_chars) > len(english_words):
        return "zh"
    else:
        return "en"

def normalize_zh(text):
    return process_ddd(text_normalize(remove_chinese_punctuation(text)))


def normalize_en(text):
    from tn.english.normalizer import Normalizer
    normalizer = Normalizer()
    return remove_english_punctuation(normalizer.normalize(text))


def process_ddd(text):
    """
    处理“地”、“得” 字的使用，都替换为“的”
    依据：地、得的使用，主要是在动词和形容词前后，本方法没有严格按照语法替换，因为时常遇到用错的情况。
    另外受 jieba 分词准确率的影响，部分情况下可能会出漏掉。例如：小红帽疑惑地问
    :param text: 输入的文本
    :return: 处理后的文本
    """
    word_list = [(word, flag) for word, flag in pseg.cut(text, use_paddle=False)]
    processed_words = []
    for i, (word, flag) in enumerate(word_list):
        if word in ["地", "得"]:
            # Check previous and next word's flag
            # prev_flag = word_list[i - 1][1] if i > 0 else None
            # next_flag = word_list[i + 1][1] if i + 1 < len(word_list) else None

            # if prev_flag in ['v', 'a'] or next_flag in ['v', 'a']:
            if flag in ['uv', 'ud']:
                processed_words.append("的")
            else:
                processed_words.append(word)
        else:
            processed_words.append(word)

    return ''.join(processed_words)



def text_normalize(text):
    """
    对文本进行归一化处理
    :param text:
    :return:
    """
    # ref: https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/paddlespeech/t2s/frontend/zh_normalization
    tx = TextNormalizer()
    sentences = tx.normalize(text)

    _txt = ''.join(sentences)
    # 替换掉除中文之外的所有字符
    # _txt = re.sub(
    #     r"[^\u4e00-\u9fa5，。！？、]+", "", _txt
    # )
    return _txt


def remove_chinese_punctuation(text):
    """
    移除文本中的中文标点符号 [：；！（），【】『』「」《》－‘“’”:,;!\(\)\[\]><\-] 替换为 ，
    :param text:
    :return:
    """
    chinese_punctuation_pattern = r"[：；！（），【】『』「」《》－‘“’”:,;!\(\)\[\]><\-·]"
    text = re.sub(chinese_punctuation_pattern, '，', text)
    # 使用正则表达式将多个连续的句号替换为一个句号
    text = re.sub(r'[。，]{2,}', '。', text)
    # 删除开头和结尾的 ， 号
    text = re.sub(r'^，|，$', '', text)
    return text


def remove_english_punctuation(text):
    """
    移除文本中的中文标点符号 [：；！（），【】『』「」《》－‘“’”:,;!\(\)\[\]><\-] 替换为 ，
    :param text:
    :return:
    """
    chinese_punctuation_pattern = r"[：；！（），【】『』「」《》－‘“’”:,;!\(\)\[\]><\-·]"
    text = re.sub(chinese_punctuation_pattern, ',', text)
    # 使用正则表达式将多个连续的句号替换为一个句号
    text = re.sub(r'[,\.]{2,}', '.', text)
    # 删除开头和结尾的 ， 号
    text = re.sub(r'^,|,$', '', text)
    return text





