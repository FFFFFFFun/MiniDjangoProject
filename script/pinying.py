from  pypinyin import lazy_pinyin , Style

style = Style.TONE3
name_list=lazy_pinyin('林非凡',style=style)
print(''.join(name_list))
print(name_list)
