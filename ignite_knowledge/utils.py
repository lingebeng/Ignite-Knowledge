import re
import markdown
from django.conf import settings


# 将markdown转换成html，其中添加了行内latex公式的转换！
def markdown_transfer(content,flag=True):
    md = markdown.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
    content = md.convert(content)
    """
    @linhaifeng:奇技淫巧使得在markdown中显示latex数学公式，但是没法变颜色，网上的方法不太行！
    """
    if flag:
        all_latex = re.findall("\$(.*?)\$", content, re.S)
        for latex in all_latex:
            latex = latex.strip()
            transfer = f"""<div style="background-color:white"><img align="center" src="https://latex.codecogs.com/svg.latex?{latex}"></div>"""
            content = content.replace(latex, transfer)
        content = content.replace("$", '')
        content = re.sub(r'<img', r'<img class="diy-image" ', content)
        toc = md.toc
        return content,toc
    else:
        return content