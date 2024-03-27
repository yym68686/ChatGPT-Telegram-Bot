def is_surrounded_by_chinese(text, index):
    if 0 < index < len(text) - 1:
        left_char = text[index - 1]
        right_char = text[index + 1]
        return '\u4e00' <= left_char <= '\u9fff' or '\u4e00' <= right_char <= '\u9fff'
    return False

def replace_char(string, index, new_char):
    return string[:index] + new_char + string[index+1:]

def claude_replace(text):
    Punctuation_mapping = {",": "，", ":": "："}
    for i in range(len(text)):
        if is_surrounded_by_chinese(text, i) and (text[i] == ',' or text[i] == ':'):
            text = replace_char(text, i, Punctuation_mapping[text[i]])
    return text

text = '''
absmax量化的具体过程如下:

1. 确定量化比特位宽b:根据需求选择量化的目标位宽,如8位、4位等。

2. 计算量化因子s:对于一个待量化的张量T,找到其绝对值的最大值absmax,然后计算量化因子s = absmax / (2^(b-1) - 1)。这里的absmax是为了将张量的取值范围映射到[0, 2^(b-1) - 1]的区间内。

3. 量化权重:对于张量T中的每个元素t,计算其量化值q_t = round(t / s),其中round表示四舍五入到最近的整数。这一步将浮点数值映射到离散的整数值。

4. 反量化:在推理时,需要将量化后的值q_t还原为浮点数。反量化的过程为t' = q_t * s,其中t'为还原后的近似值。

下面以一个具体的例子说明计算过程:

假设有一个权重矩阵W:
[[0.3, -0.7, 1.2],
 [0.8, -0.2, -0.5]]

选择8位量化,即b=8。

计算量化因子s:
absmax = max(abs(0.3), abs(-0.7), abs(1.2), abs(0.8), abs(-0.2), abs(-0.5)) = 1.2
s = 1.2 / (2^(8-1) - 1) = 1.2 / 127 ≈ 0.0094

量化权重:
q_0.3 = round(0.3 / 0.0094) = 32
q_-0.7 = round(-0.7 / 0.0094) = -74
q_1.2 = round(1.2 / 0.0094) = 127
q_0.8 = round(0.8 / 0.0094) = 85
q_-0.2 = round(-0.2 / 0.0094) = -21
q_-0.5 = round(-0.5 / 0.0094) = -53

量化后的矩阵Q:
[[32, -74, 127],
 [85, -21, -53]]

反量化:
t'_0.3 = 32 * 0.0094 = 0.3008
t'_-0.7 = -74 * 0.0094 = -0.6956
...

反量化后的矩阵W':
[[0.3008, -0.6956, 1.1938],
 [0.7990, -0.1974, -0.4982]]

可以看到,量化后的矩阵Q的取值范围在[-128, 127]之间,每个元素用8位有符号整数表示。反量化后的矩阵W'与原始矩阵W非常接近,但并非完全相等,这是量化过程引入的误差。

'''

if __name__ == '__main__':
    new_text = claude_replace(text)
    print(new_text)