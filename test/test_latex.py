import re
import unicodedata

class CombiningType:
    FirstChar = 1
    LastChar = 2
    EveryChar = 3

class LaTeX2Unicode:
    def __init__(self):
        self.escape_map = {
            "\\&": "&",
            "\\$": "$",
            "\\{": "{",
            "\\}": "}",
            "\\%": "%",
            "\\#": "#",
            "\\_": "_",
            "$": "",

            "~": " ",
            "\\;": " ",
            "\\:": " ",
            "\\,": " ",
            "\\quad": " ",
            "\\qquad": " ",
            """\\""": "\n",
            "-": "-",
            "--": "\u2013",
            "---": "\u2014",
            "\\colon": ":",
            "\\lbrack": "[",
            "\\rbrack": "]",
            "\\textasciicircum": "^",
            "\\textbackslash": "\\",
            "\\textless": "<",
            "\\textgreater": ">",
            "\\textbar": "|",
            "\\textasciitilde": "~",
            "\\textunderscore": "_",
            "\\textendash": "–",
            "\\texttrademark": "™",
            "\\textexclamdown": "¡",
            "\\textemdash": "—",
            "\\textregistered": "®",
            "\\textquestiondown": "¿",
            "\\textvisiblespace": "␣",
            "\\textminus": "\u2212",

            # Greek alphabet
            "\\alpha": "α",
            "\\beta": "β",
            "\\Gamma": "Γ",
            "\\gamma": "γ",
            "\\Delta": "Δ",
            "\\delta": "δ",
            "\\zeta": "ζ",
            "\\eta": "η",
            "\\Theta": "Θ",
            "\\theta": "θ",
            "\\Iota": "Ι",
            "\\iota": "ι",
            "\\kappa": "κ",
            "\\Lambda": "Λ",
            "\\lambda": "λ",
            "\\mu": "μ",
            "\\Nu": "Ν",
            "\\nu": "ν",
            "\\Xi": "Ξ",
            "\\xi": "ξ",
            "\\Pi": "Π",
            "\\pi": "π",
            "\\rho": "ρ",
            "\\Sigma": "Σ",
            "\\sigma": "σ",
            "\\tau": "τ",
            "\\Upsilon": "Υ",
            "\\upsilon": "υ",
            "\\Phi": "Φ",
            "\\phi": "φ",
            "\\chi": "χ",
            "\\Psi": "Ψ",
            "\\psi": "ψ",
            "\\Omega": "Ω",
            "\\omega": "ω",
            "\\P": "¶",
            "\\S": "§",
            "\\|": "‖",
            "\\wr": "≀",
            "\\wp": "℘",
            "\\wedge": "∧",
            "\\veebar": "⊻",
            "\\vee": "∨",
            "\\vdots": "⋮",
            "\\vdash": "⊢",
            "\\vartriangleright": "⊳",
            "\\vartriangleleft": "⊲",
            "\\vartriangle": "△",
            "\\vartheta": "ϑ",
            "\\varsigma": "ς",
            "\\varrho": "ϱ",
            "\\varpropto": "∝",
            "\\varpi": "ϖ",
            "\\varphi": "ϕ",
            "\\varnothing": "∅",
            "\\varkappa": "ϰ",
            "\\varepsilon": "ε",
            "\\vDash": "⊨",
            "\\upuparrows": "⇈",
            "\\uplus": "⊎",
            "\\upharpoonright": "↾",
            "\\upharpoonleft": "↿",
            "\\updownarrow": "↕",
            "\\uparrow": "↑",
            "\\unrhd": "⊵",
            "\\unlhd": "⊴",
            "\\twoheadrightarrow": "↠",
            "\\twoheadleftarrow": "↞",
            "\\trianglerighteq": "⊵",
            "\\triangleright": "▷",
            "\\triangleq": "≜",
            "\\trianglelefteq": "⊴",
            "\\triangleleft": "◁",
            "\\triangledown": "▽",
            "\\triangle": "△",
            "\\top": "⊤",
            "\\times": "×",
            "\\thicksim": "∼",
            "\\thickapprox": "≈",
            "\\therefore": "∴",
            "\\swarrow": "↙",
            "\\surd": "√",
            "\\supseteq": "⊇",
            "\\supsetneq": "⊋",
            "\\supset": "⊃",
            "\\sum": "∑",
            "\\succsim": "≿",
            "\\succeq": "≽",
            "\\succcurlyeq": "≽",
            "\\succ": "≻",
            "\\subseteq": "⊆",
            "\\subsetneq": "⊊",
            "\\subset": "⊂",
            "\\star": "⋆",
            "\\square": "□",
            "\\sqsupseteq": "⊒",
            "\\sqsupset": "⊐",
            "\\sqsubseteq": "⊑",
            "\\sqsubset": "⊏",
            "\\sqcup": "⊔",
            "\\sqcap": "⊓",
            "\\sphericalangle": "∢",
            "\\spadesuit": "♠",
            "\\smile": "⌣",
            "\\smallsmile": "⌣",
            "\\smallsetminus": "∖",
            "\\smallfrown": "⌢",
            "\\simeq": "≃",
            "\\sim": "∼",
            "\\shortparallel": "∥",
            "\\sharp": "♯",
            "\\setminus": "∖",
            "\\searrow": "↘",
            "\\rtimes": "⋈",
            "\\risingdotseq": "≓",
            "\\rightthreetimes": "⋌",
            "\\rightsquigarrow": "⇝",
            "\\rightrightarrows": "⇉",
            "\\rightleftharpoons": "⇌",
            "\\rightleftarrows": "⇄",
            "\\rightharpoonup": "⇀",
            "\\rightharpoondown": "⇁",
            "\\rightarrowtail": "↣",
            "\\to": "→",
            "\\rightarrow": "→",
            "\\rhd": "⊳",
            "\\rfloor": "⌋",
            "\\rceil": "⌉",
            "\\rangle": "〉",
            "\\propto": "∝",
            "\\prod": "∏",
            "\\prime": "′",
            "\\precsim": "≾",
            "\\preceq": "≼",
            "\\preccurlyeq": "≼",
            "\\prec": "≺",
            "\\pm": "±",
            "\\pitchfork": "⋔",
            "\\perp": "⊥",
            "\\partial": "∂",
            "\\parallel": "∥",
            "\\otimes": "⊗",
            "\\oslash": "⊘",
            "\\oplus": "⊕",
            "\\ominus": "⊖",
            "\\oint": "∮",
            "\\odot": "⊙",
            "\\nwarrow": "↖",
            "\\notin": "∉",
            "\\ni": "∋",
            "\\nexists": "∄",
            "\\neq": "≠",
            "\\neg": "¬",
            "\\lnot": "¬",
            "\\nearrow": "↗",
            "\\natural": "♮",
            "\\nabla": "∇",
            "\\multimap": "⊸",
            "\\mp": "∓",
            "\\models": "⊨",
            "\\mid": "∣",
            "\\mho": "℧",
            "\\mho": "℧",
            "\\measuredangle": "∡",
            "\\mapsto": "↦",
            "\\ltimes": "⋉",
            "\\lozenge": "◊",
            "\\looparrowright": "↬",
            "\\looparrowleft": "↫",
            "\\longrightarrow": "→",
            "\\longmapsto": "⇖",
            "\\longleftrightarrow": "↔",
            "\\longleftarrow": "←",
            "\\lll": "⋘",
            "\\ll": "≪",
            "\\lhd": "⊲",
            "\\lfloor": "⌊",
            "\\lesssim": "≲",
            "\\lessgtr": "≶",
            "\\lesseqgtr": "⋚",
            "\\lessdot": "⋖",
            "\\leqslant": "≤",
            "\\leqq": "≦",
            "\\leq": "≤",
            "\\leftthreetimes": "⋋",
            "\\leftrightsquigarrow": "↭",
            "\\leftrightharpoons": "⇋",
            "\\leftrightarrows": "⇆",
            "\\leftrightarrow": "↔",
            "\\leftleftarrows": "⇇",
            "\\leftharpoonup": "↼",
            "\\leftharpoondown": "↽",
            "\\leftarrowtail": "↢",
            "\\gets": "←",
            "\\leftarrow": "←",
            "\\leadsto": "↝",
            "\\le": "≤",
            "\\lceil": "⌈",
            "\\langle": "〈",
            "\\intercal": "⊺",
            "\\int": "∫",
            "\\iint": "∬",
            "\\iiint": "∭",
            "\\iiiint": "⨌",
            "\\infty": "∞",
            "\\in": "∈",
            "\\implies": "⇒",
            "\\hslash": "ℏ",
            "\\hookrightarrow": "↪",
            "\\hookleftarrow": "↩",
            "\\heartsuit": "♡",
            "\\hbar": "ℏ",
            "\\hbar": "ℏ",
            "\\gtrsim": "≳",
            "\\gtrless": "≷",
            "\\gtreqless": "⋛",
            "\\gtrdot": "⋗",
            "\\gimel": "ג",
            "\\ggg": "⋙",
            "\\gg": "≫",
            "\\geqq": "≧",
            "\\geq": "≥",
            "\\ge": "≥",
            "\\frown": "⌢",
            "\\forall": "∀",
            "\\flat": "♭",
            "\\fallingdotseq": "≒",
            "\\exists": "∃",
            "\\eth": "ð",
            "\\equiv": "≡",
            "\\eqcirc": "≖",
            "\\epsilon": "∊",
            "\\Epsilon": "Ε",
            "\\emptyset": "∅",
            "\\ell": "ℓ",
            "\\downharpoonright": "⇂",
            "\\downharpoonleft": "⇃",
            "\\downdownarrows": "⇊",
            "\\downarrow": "↓",
            "\\dots": "…",
            "\\ldots": "…",
            "\\dotplus": "∔",
            "\\doteqdot": "≑",
            "\\doteq": "≐",
            "\\divideontimes": "⋇",
            "\\div": "÷",
            "\\digamma": "Ϝ",
            "\\diamondsuit": "♢",
            "\\diamond": "⋄",
            "\\ddots": "⋱",
            "\\ddag": "‡",
            "\\ddagger": "‡",
            "\\dashv": "⊣",
            "\\dashrightarrow": "⇢",
            "\\dashleftarrow": "⇠",
            "\\daleth": "ד",
            "\\dag": "†",
            "\\dagger": "†",
            "\\textdagger": "†",
            "\\curvearrowright": "↷",
            "\\curvearrowleft": "↶",
            "\\curlywedge": "⋏",
            "\\curlyvee": "⋎",
            "\\curlyeqsucc": "⋟",
            "\\curlyeqprec": "⋞",
            "\\cup": "∪",
            "\\coprod": "∐",
            "\\cong": "≅",
            "\\complement": "∁",
            "\\colon": ":",
            "\\clubsuit": "♣",
            "\\circleddash": "⊝",
            "\\circledcirc": "⊚",
            "\\circledast": "⊛",
            "\\circledS": "Ⓢ",
            "\\circlearrowright": "↻",
            "\\circlearrowleft": "↺",
            "\\circeq": "≗",
            "\\circ": "∘",
            "\\centerdot": "⋅",
            "\\cdots": "⋯",
            "\\cdot": "⋅",
            "\\cap": "∩",
            "\\bumpeq": "≏",
            "\\bullet": "∙",
            "\\boxtimes": "⊠",
            "\\boxplus": "⊞",
            "\\boxminus": "⊟",
            "\\boxdot": "⊡",
            "\\bowtie": "⋈",
            "\\bot": "⊥",
            "\\blacktriangleright": "▷",
            "\\blacktriangleleft": "◀",
            "\\blacktriangledown": "▼",
            "\\blacktriangle": "▲",
            "\\blacksquare": "■",
            "\\blacklozenge": "◆",
            "\\bigwedge": "⋀",
            "\\bigvee": "⋁",
            "\\biguplus": "⊎",
            "\\bigtriangleup": "△",
            "\\bigtriangledown": "▽",
            "\\bigstar": "★",
            "\\bigsqcup": "⊔",
            "\\bigotimes": "⊗",
            "\\bigoplus": "⊕",
            "\\bigodot": "⊙",
            "\\bigcup": "⋃",
            "\\bigcirc": "○",
            "\\bigcap": "⋂",
            "\\between": "≬",
            "\\beth": "ב",
            "\\because": "∵",
            "\\barwedge": "⊼",
            "\\backsim": "∽",
            "\\backprime": "‵",
            "\\backepsilon": "∍",
            "\\asymp": "≍",
            "\\ast": "∗",
            "\\approxeq": "≊",
            "\\approx": "≈",
            "\\angle": "∠",
            "\\angle": "∠",
            "\\aleph": "א",
            "\\Vvdash": "⊪",
            "\\Vdash": "⊩",
            "\\Updownarrow": "⇕",
            "\\Uparrow": "⇑",
            "\\Supset": "⋑",
            "\\Subset": "⋐",
            "\\Rsh": "↱",
            "\\Rrightarrow": "⇛",
            "\\Rightarrow": "⇒",
            "\\Re": "ℜ",
            "\\Lsh": "↰",
            "\\Longrightarrow": "⇒",
            "\\iff": "⇔",
            "\\Longleftrightarrow": "⇔",
            "\\Longleftarrow": "⇐",
            "\\Lleftarrow": "⇚",
            "\\Leftrightarrow": "⇔",
            "\\Leftarrow": "⇐",
            "\\Join": "⋈",
            "\\Im": "ℑ",
            "\\Finv": "Ⅎ",
            "\\Downarrow": "⇓",
            "\\Diamond": "◇",
            "\\Cup": "⋓",
            "\\Cap": "⋒",
            "\\Bumpeq": "≎",
            "\\Box": "□",
            "\\ae": "æ",
            "\\AE": "Æ",
            "\\oe": "œ",
            "\\OE": "Œ",
            "\\aa": "å",
            "\\AA": "Å",
            "\\dh": "ð",
            "\\DH": "Ð",
            "\\dj": "đ",
            "\\DJ": "Ð",
            "\\o": "ø",
            "\\O": "Ø",
            "\\i": "ı",
            "\\imath": "ı",
            "\\j": "ȷ",
            "\\jmath": "ȷ",
            "\\L": "Ł",
            "\\l": "ł",
            "\\ss": "ß",
            "\\aleph": "ℵ",
            "\\copyright": "©",
            "\\pounds": "£",
            "\\euro": "€",
            "\\EUR": "€",
            "\\texteuro": "€"
        }

        self.combining = {
            "\\grave": ('\u0300', CombiningType.FirstChar),
            "\\`": ('\u0300', CombiningType.FirstChar),
            "\\acute": ('\u0301', CombiningType.FirstChar),
            "\\'": ('\u0301', CombiningType.FirstChar),
            "\\hat": ('\u0302', CombiningType.FirstChar),
            "\\^": ('\u0302', CombiningType.FirstChar),
            "\\tilde": ('\u0303', CombiningType.FirstChar),
            "\\~": ('\u0303', CombiningType.FirstChar),
            "\\bar": ('\u0304', CombiningType.FirstChar),
            "\\=": ('\u0304', CombiningType.FirstChar),
            "\\overline": ('\u0305', CombiningType.EveryChar),
            "\\breve": ('\u0306', CombiningType.FirstChar),
            "\\u": ('\u0306', CombiningType.FirstChar),
            "\\dot": ('\u0307', CombiningType.FirstChar),
            "\\.": ('\u0307', CombiningType.FirstChar),
            "\\ddot": ('\u0308', CombiningType.FirstChar),
            "\\\"": ('\u0308', CombiningType.FirstChar),
            "\\mathring": ('\u030A', CombiningType.FirstChar),
            "\\r": ('\u030A', CombiningType.FirstChar),
            "\\H": ('\u030B', CombiningType.FirstChar),
            "\\check": ('\u030C', CombiningType.FirstChar),
            "\\v": ('\u030C', CombiningType.FirstChar),
            "\\d": ('\u0323', CombiningType.FirstChar),
            "\\c": ('\u0327', CombiningType.FirstChar),
            "\\k": ('\u0328', CombiningType.LastChar),
            "\\b": ('\u0332', CombiningType.FirstChar),
            "\\underline": ('\u0332', CombiningType.EveryChar),
            "\\underbar": ('\u0332', CombiningType.EveryChar),
            "\\t": ('\u0361', CombiningType.FirstChar),
            "\\vec": ('\u20D7', CombiningType.FirstChar),
            "\\textcircled": ('\u20DD', CombiningType.FirstChar)
        }

        self.binary_commands = {
            "\\frac": self.make_fraction
        }

        # 其他样式映射 (如 bb, bf, cal, frak, it, tt) 也需要定义

    def is_combining_char(self, char):
        return ('\u0300' <= char <= '\u036F' or
                '\u1AB0' <= char <= '\u1AFF' or
                '\u1DC0' <= char <= '\u1DFF' or
                '\u20D0' <= char <= '\u20FF' or
                '\uFE20' <= char <= '\uFE2F')

    def is_combining_or_control_char(self, char):
        return char.isspace() or self.is_combining_char(char)

    def translate_escape(self, name):
        return self.escape_map.get(name, name)

    def translate_combining(self, command, text):
        if command not in self.combining:
            raise ValueError(f"Unknown combining command: {command}")

        combining_char, combining_type = self.combining[command]

        if not text:
            text = " "

        if combining_type == CombiningType.FirstChar:
            i = 1
            while i < len(text) and self.is_combining_or_control_char(text[i]):
                i += 1
            return text[:i] + combining_char + text[i:]
        elif combining_type == CombiningType.LastChar:
            return text + combining_char
        elif combining_type == CombiningType.EveryChar:
            if not text:
                return ""
            return ''.join(char + combining_char for char in text)

    def should_parenthesize_string_with_char(self, c):
        return (not c.isalnum() and
                not self.is_combining_char(c) and
                unicodedata.category(c) not in ['No', 'Pc'])

    def maybe_parenthesize(self, s):
        if not any(self.should_parenthesize_string_with_char(c) for c in s):
            return s
        return f"({s})"

    def make_fraction(self, numerator, denominator):
        frac = {
            ("1", "2"): "½",
            ("1", "3"): "⅓",
            ("2", "3"): "⅔",
            ("1", "4"): "¼",
            ("3", "4"): "¾",
            ("1", "5"): "⅕",
            ("2", "5"): "⅖",
            ("3", "5"): "⅗",
            ("4", "5"): "⅘",
            ("1", "6"): "⅙",
            ("5", "6"): "⅚",
            ("1", "8"): "⅛",
            ("3", "8"): "⅜",
            ("5", "8"): "⅝",
            ("7", "8"): "⅞"
        }
        n, d = numerator.strip(), denominator.strip()
        if not n and not d:
            return ""
        if (n, d) in frac:
            return frac[(n, d)]

        # 移除 \left 和 \right
        n = n.replace("\\left", "").replace("\\right", "")
        d = d.replace("\\left", "").replace("\\right", "")

        return f"{self.maybe_parenthesize(n)}/{self.maybe_parenthesize(d)}"


    def parse(self, latex):
        result = []
        i = 0
        while i < len(latex):
            if latex[i] == '\\':
                command, i = self.parse_command(latex, i)
                handled, i = self.handle_command(command, latex, i)
                result.append(handled)
            elif latex[i] == '{':
                block, i = self.parse_block(latex, i)
                result.append(block)
            elif latex[i].isspace():
                spaces, i = self.parse_spaces(latex, i)
                result.append(spaces)
            else:
                result.append(latex[i])
                i += 1
        return ''.join(result)

    def handle_command(self, command, latex, index):
        if command in self.escape_map:
            return self.translate_escape(command), index
        elif command in self.combining:
            arg, new_index = self.parse_block(latex, index)
            return self.translate_combining(command, arg), new_index
        elif command in self.binary_commands:
            param1, index = self.parse_block(latex, index)
            param2, index = self.parse_block(latex, index)
            return self.binary_commands[command](param1, param2), index
        elif command in ["\\left", "\\right"]:
            # 忽略 \left 和 \right 命令
            return "", index
        # 处理其他类型的命令 (如样式等)
        # ...
        return command, index  # 如果无法处理,返回原命令

    def parse_command(self, latex, start):
        match = re.match(r'\\([a-zA-Z]+|.)', latex[start:])
        if match:
            return match.group(0), start + match.end()
        return '\\', start + 1

    def parse_block(self, latex, start):
        level = 1
        end = start + 1
        while end < len(latex) and level > 0:
            if latex[end] == '{':
                level += 1
            elif latex[end] == '}':
                level -= 1
            end += 1
        return self.parse(latex[start+1:end-1]), end

    def parse_spaces(self, latex, start):
        end = start
        while end < len(latex) and latex[end].isspace():
            end += 1
        spaces = latex[start:end]
        if '\n' in spaces:
            return '\n\n', end
        return ' ', end

    def convert(self, latex):
        try:
            return self.parse(latex)
        except Exception:
            return latex  # 如果解析失败,返回原始字符串

# 使用示例

# 根据欧拉函数的性质，对于 \( n = p_1^{k_1} \times p_2^{k_2} \times \cdots \times p_r^{k_r} \)（其中 \( p_1, p_2, \ldots, p_r \) 是互不相同的质数），有：

# \[ \varphi(n) = n \left(1 - \frac{1}{p_1}\right) \left(1 - \frac{1}{p_2}\right) \cdots \left(1 - \frac{1}{p_r}\right) \]

# 所以：

# \[ \varphi(35) = 35 \left(1 - \frac{1}{5}\right) \left(1 - \frac{1}{7}\right) \]

# 计算每一步：

# \[ \varphi(35) = 35 \left(\frac{4}{5}\right) \left(\frac{6}{7}\right) \]

# \[ \varphi(35) = 35 \times \frac{24}{35} \]

# \[ \varphi(35) = 24 \]

# 因此，欧拉函数 \( \varphi(35) \) 的值是 24。
latex2unicode = LaTeX2Unicode()
result = latex2unicode.convert("\\varphi(35) = 35 \\left(1 - \\frac{1}{5}\\right) \\left(1 - \\frac{1}{7}\\right)")
print(result)  # 预期输出: ϕ(35) = 35(1 - ⅕)(1 - 1/7)
result = latex2unicode.convert("\\alpha + \\beta = \\gamma")
print(result)  # 预期输出: α + β = γ
result = latex2unicode.convert("35 = 5 \\times 7")
print(result)  # 预期输出: α + β = γ
result = latex2unicode.convert("n = p_1^{k_1} \\times p_2^{k_2} \\times \\cdots \\times p_r^{k_r}")
print(result)  # 预期输出: α + β = γ
result = latex2unicode.convert("\\varphi(35) = 35 \\left(1 - \\frac{1}{5}\\right) \\left(1 - \\frac{1}{7}\\right)")
print(result)  # 预期输出: α + β = γ
result = latex2unicode.convert("\\varphi(35) = 35 \\times \\frac{24}{35}")
print(result)  # 预期输出: α + β = γ
result = latex2unicode.convert("\\varphi(35) = 24")
print(result)  # 预期输出: α + β = γ