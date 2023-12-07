from pdfminer.high_level import extract_text
text = extract_text('/Users/yanyuming/Desktop/中国计算机学会推荐中文科技期刊目录.pdf')
# text = extract_text('/Users/yanyuming/Library/Mobile Documents/iCloud~QReader~MarginStudy/Documents/论文/VersatileGait- A Large-Scale Synthetic Gait Dataset with Fine-Grained Attributes and Complicated Scenarios.pdf')
# print(repr(text))
print(text)

# from io import StringIO
# from pdfminer.high_level import extract_text_to_fp
# from pdfminer.layout import LAParams
# output_string = StringIO()
# with open('/Users/yanyuming/Desktop/Gait review.pdf', 'rb') as fin:
#     extract_text_to_fp(fin, output_string, laparams=LAParams(),
#                        output_type='html', codec=None)
# print(output_string.getvalue().strip())

# from io import StringIO
# from pdfminer.high_level import extract_text_to_fp
# output_string = StringIO()
# with open('/Users/yanyuming/Library/Mobile Documents/iCloud~QReader~MarginStudy/Documents/论文/VersatileGait- A Large-Scale Synthetic Gait Dataset with Fine-Grained Attributes and Complicated Scenarios.pdf', 'rb') as fin:
#     extract_text_to_fp(fin, output_string)
# print(output_string.getvalue().strip())