import requests
import asyncio
import bs4

from app.schemas import Song


async def Get_Song_Info(song_link: str) :
    response = requests.get(
        url=song_link,
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
    )
    # print(response.text)
    doc = bs4.BeautifulSoup(response.text, "html.parser")
    Artist = str(doc.find(itemprop="byArtist").string)
    Song = str(doc.find(itemprop="name").string)
    # print(Artist, Song)
    txt = doc.find(itemprop = "chordsBlock")
    # print(txt.prettify())
    childrens = list(txt.children)
    # print(str(childrens[1].string))
    chords_words = []
    no_skipped_words = []
    # print(bool(txt.find_all('div', attrs={"class" : "podbor__keyword"})))
    if txt.find_all('div', attrs={"class" : "podbor__keyword"}):
        if txt.find_all('div', attrs={"class": "podbor__inline"}):
            keywords_count = -1
            i = 0
            if isinstance(childrens[0], bs4.element.NavigableString):
                # print(childrens[0])
                chords_words.append([0,str(childrens[0]).split('\n')])
                i = 1

            while i < len(childrens):
                if isinstance(childrens[i], bs4.element.Tag):
                    # print(childrens[i].attrs)
                    if childrens[i]['class'] == ["podbor__inline"]:
                        # print(childrens[i])
                        sub_childrens = childrens[i].children
                        # print(type(sub_childrens))
                        title_str = []
                        for sub_child in sub_childrens:
                            if isinstance(sub_child, bs4.element.NavigableString):
                                pass
                            elif sub_child['class'] == ["podbor__keyword"]:
                                title_str.append(sub_child.string)
                            elif sub_child['class'] == ["podbor__author-comment"]:
                                sub_sub_children = sub_child.children
                                for sub_sub_child in sub_sub_children:
                                    if str(sub_sub_child.string) not in  ['/*', '*/']:
                                        title_str.append(str(sub_sub_child.string))
                        title_str = " ".join(title_str)
                        chords_words.append([title_str, []])
                        keywords_count += 1
                    elif childrens[i]['class'] == ["podbor__author-comment"]:
                        sub_sub_children = childrens[i].children
                        extrachord = []
                        for sub_sub_child in sub_sub_children:
                            if str(sub_sub_child.string) not in ['/*', '*/']:
                                extrachord.append(str(sub_sub_child.string))
                        chords_words[keywords_count][1].append(" ".join(extrachord))
                        no_skipped_words.append(" ".join(extrachord))
                    elif childrens[i]['class'] == ["podbor__keyword"]:
                        chords_words.append([childrens[i].string,[]])
                        keywords_count += 1
                    elif childrens[i]['class'] == ["podbor__pripev"]:
                        sub_children = list(childrens[i].children)
                        j = 0
                        while j < len(sub_children):
                            if childrens[i]['class'] == ["podbor__chord"]:
                                chords_words.append([sub_children[j].string, []])
                            else:
                                chords_words[keywords_count][1].extend(str(sub_children[j].string).split('\n'))
                            j += 1
                    else:
                        if "\n\n" in str(childrens[i].string):
                            extend_list = []
                            k = 0
                            hard_string = str(childrens[i].string)
                            last_n = -1
                            first_n = -1
                            while k < len(hard_string):
                                if hard_string[k] == '\n':
                                    first_n = k
                                    k += 1
                                    while k < len(hard_string) and hard_string[k] == '\n':
                                        last_n = k
                                        k += 1
                                    if first_n < last_n:
                                        extend_list.append(hard_string[first_n:last_n])
                                else:
                                    new_split_word = []
                                    while k < len(hard_string) and hard_string[k] != '\n':
                                        new_split_word.append(hard_string[k])
                                        k += 1
                                    if new_split_word:
                                        extend_list.append("".join(new_split_word))
                            # print(extend_list)
                            chords_words[keywords_count][1].extend(extend_list)
                        else:
                            chords_words[keywords_count][1].extend(str(childrens[i].string).split('\n'))
                else:
                    if "\n\n" in str(childrens[i]):
                        # print(str(childrens[i]))
                        extend_list = []
                        k = 0
                        hard_string = str(childrens[i])
                        last_n = -1
                        first_n = -1
                        while k < len(hard_string):
                            if hard_string[k] == '\n':
                                first_n = k
                                k += 1
                                while k < len(hard_string) and hard_string[k] == '\n':
                                    last_n = k
                                    k += 1
                                if first_n < last_n:
                                    extend_list.append(hard_string[first_n:last_n])
                            else:
                                new_split_word = []
                                while k < len(hard_string) and hard_string[k] != '\n':
                                    new_split_word.append(hard_string[k])
                                    k += 1
                                if new_split_word:
                                    extend_list.append("".join(new_split_word))
                        # print(extend_list)
                        chords_words[keywords_count][1].extend(extend_list)
                    else:
                        chords_words[keywords_count][1].extend(str(childrens[i]).split('\n'))
                i += 1
    else:
        keywords_count = 0
        i = 0
        if isinstance(childrens[0], bs4.element.NavigableString):
            # print(childrens[0])
            chords_words.append([0,[str(childrens[0])]])
            i = 1
        chords_words.append([0,[]])
        while i < len(childrens):
            if isinstance(childrens[i], bs4.element.Tag):
                if childrens[i]['class'] == ["podbor__author-comment"]:
                    sub_sub_children = childrens[i].children
                    extrachord = []
                    for sub_sub_child in sub_sub_children:
                        if str(sub_sub_child.string) not in ['/*', '*/']:
                            extrachord.append(str(sub_sub_child.string))
                    chords_words[keywords_count][1].append(" ".join(extrachord))
                    no_skipped_words.append(" ".join(extrachord))
                elif childrens[i]['class'] == ["podbor__pripev"]:
                    sub_children = list(childrens[i].children)
                    j = 0
                    while j < len(sub_children):
                        if childrens[i]['class'] == ["podbor__chord"]:
                            chords_words.append([sub_children[j].string, []])
                        else:
                            chords_words[keywords_count][1].extend(str(sub_children[j].string).split('\n'))
                        j += 1
                else:
                    if "\n\n" in str(childrens[i].string):
                        extend_list = []
                        k = 0
                        hard_string = str(childrens[i].string)
                        last_n = -1
                        first_n = -1
                        while k < len(hard_string):
                            if hard_string[k] == '\n':
                                first_n = k
                                k += 1
                                while k < len(hard_string) and hard_string[k] == '\n':
                                    last_n = k
                                    k += 1
                                if first_n < last_n:
                                    extend_list.append(hard_string[first_n:last_n])
                            else:
                                new_split_word = []
                                while k < len(hard_string) and hard_string[k] != '\n':
                                    new_split_word.append(hard_string[k])
                                    k += 1
                                if new_split_word:
                                    extend_list.append("".join(new_split_word))
                        # print(extend_list)
                        chords_words[keywords_count][1].extend(extend_list)
                    else:
                        chords_words[keywords_count][1].extend(str(childrens[i].string).split('\n'))
            else:
                if "\n\n" in str(childrens[i]):
                    # print(str(childrens[i]))
                    extend_list = []
                    k = 0
                    hard_string = str(childrens[i])
                    last_n = -1
                    first_n = -1
                    while k < len(hard_string):
                        if hard_string[k] == '\n':
                            first_n = k
                            k += 1
                            while k < len(hard_string) and hard_string[k] == '\n':
                                last_n = k
                                k += 1
                            if first_n < last_n:
                                extend_list.append(hard_string[first_n:last_n])
                        else:
                            new_split_word = []
                            while k < len(hard_string) and hard_string[k] != '\n':
                                new_split_word.append(hard_string[k])
                                k += 1
                            if new_split_word:
                                extend_list.append("".join(new_split_word))
                    print(extend_list)
                    chords_words[keywords_count][1].extend(extend_list)
                else:
                    chords_words[keywords_count][1].extend(str(childrens[i]).split('\n'))
            i += 1
    def is_space(string: str):
        for x in string:
            if x != ' ':
                return False
        return True
    chords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'А', 'В', 'С', 'Е',
              'Am', 'Bm', 'Cm', 'Dm', 'Em', 'Fm', 'Gm', 'Аm', 'Вm', 'Сm', 'Еm',
              'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'А7', 'В7', 'С7', 'Е7',
              'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'А6', 'В6', 'С6', 'Е6',
              'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'А5', 'В5', 'С5', 'Е5',
              'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Аb', 'Вb', 'Сb', 'Еb',
              'Abm', 'Bbm', 'Cbm', 'Dbm', 'Ebm', 'Fbm', 'Gbm', 'Аbm', 'Вbm', 'Сbm', 'Еbm',
              'A#', 'B#', 'C#', 'D#', 'E#', 'F#', 'G#', 'А#', 'В#', 'С#', 'Е#',
              'A#m', 'B#m', 'C#m', 'D#m', 'E#m', 'F#m','G#m', 'А#m', 'В#m', 'С#m', 'Е#m',
              'A#5', 'B#5', 'C#5', 'D#5', 'E#5', 'F#5', 'G#5' 'А#5', 'В#5', 'С#5', 'Е#5',
    ]
    print(*chords_words, sep='\n')
    # print(*no_skipped_words, sep='\n')
    for title, words in chords_words:
        if title != 0:
            print(title)
        is_previous_chord = True
        if not(words):
            continue
        for word in words:
            is_chords = word.strip() in chords
            # print(is_chords, end= ' ' )
            if is_chords or is_space(word):
                # print("chord or space", end='')
                print(word, end='')
                is_previous_chord = True
            else:
                if word in no_skipped_words:
                    print(word, end='')
                    is_previous_chord = True
                else:
                    if is_previous_chord:
                        print()
                        is_previous_chord = False
                    print(word)
    return None

async def main():
    with open("output.html", 'w', encoding='UTF-8') as f:
        await Get_Song_Info('https://m.amdm.ru/akkordi/peredelannye_pesni_parodii/1071/kino_kogda_tvoya_devushka_bolna/')
if __name__ == '__main__':
    asyncio.run(main())
#https://m.amdm.ru/akkordi/akvarium/5779/2_12_85_06/
#https://m.amdm.ru/akkordi/butusov_vyacheslav/210508/ya_hochu_byt_s_toboy/
#https://m.amdm.ru/akkordi/mot/140405/92_dnya/
#https://m.amdm.ru/akkordi/valentin_strykalo/151470/92/
    # for title, words in chords_words:
    #     if title != 0:
    #         print(title)
    #     is_previous_chord = True
    #     if words[0] == "None":
    #         continue
    #     for word in words:
    #         is_chords = word in chords
    #         # print(is_chords, end= ' ' )
    #         if is_chords or is_space(word):
    #             # print("chord or space", end='')
    #             print(word, end='')
    #             is_previous_chord = True
    #         else:
    #             # if is_previous_chord:
    #             #     print('\n')
    #             #     is_previous_chord = False
    #             splited_words = word.split('\n')
    #             for sub_word in splited_words:
    #                 if sub_word in no_skipped_words:
    #                     print(sub_word, end='')
    #                     is_previous_chord = True
    #                 elif is_space(sub_word):
    #                     if is_previous_chord:
    #                         print()
    #                         is_previous_chord = False
    #                     print(sub_word, end='')
    #                 else:
    #                     print(sub_word)