V = []
raw = []
E = []

with open('./eng.txt', 'r', encoding='utf-8') as file:
    E = file.read().split('\n')

with open('./vietnam74K.txt', 'r', encoding='utf-8') as file:
    tudien = file.read().split('\n')

    for word in tudien:
        V.append(word.strip().replace('-', '_').replace(' ', '_').lower())

    V = list(set(V))

    file.close()

with open('./words_2.txt', 'r', encoding='utf-8') as file:
    raw = file.read().split('\n')
    file.close()

with open('./tula.txt', 'w', encoding='utf-8') as file:
    for word in raw:
        if word not in V and word.find('_') == -1 and word not in E:
            file.write(word + '\n')
    file.close()
