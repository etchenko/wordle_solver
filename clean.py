def main():
    with open('words_input.txt','r') as file:
        lines = file.readlines()
        words = lines[0].replace('"','').split(',')
        words.sort()
        with open('words.txt','w') as w:
            for word in words:
                w.write(word+'\n')

def main2():
    with open('previous.txt','r') as file:
        lines = file.readlines()
        words = [i.split(' ')[5] for i in lines]
        words.sort()
        with open('previous_words.txt','w') as w:
            for word in words:
                w.write(word)


if __name__ == "__main__":
    main2()