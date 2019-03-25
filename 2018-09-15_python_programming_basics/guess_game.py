import random

def main():
    lower = 1
    upper = 100
    while True:
        myval = random.randrange(lower, upper)
        print(f'Я загадал число от {lower} до {upper - 1}, попробуй угадай?')

        while True:
            guess = int(input('Введи число: '))

            if guess > myval:
                print('Загаданое число меньше!')
                continue
            elif guess < myval:
                print('Загаданое число больше!')
                continue
            else: #guess == myval:
                print('Верно, ты угадал!\n\n\n')
            break

        retry = input('Введи слово "да", если хочешь сыграть ещё раз: ')
        if retry.lower() == 'да':
            print('Ура! Я люблю играть!')
            continue
        else:
            print('До скорой встречи!')
            return


if __name__ == '__main__':
    main()
