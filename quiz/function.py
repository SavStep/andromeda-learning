def say_hello(name:str):
    print(f"hello, {name}")
def cow_or_chiken():
    answer = input("хочешь говядину или курятину")
    need_answers = ["говядину","курятину"]
    if answer not in need_answers:
        print("такого нет брад")
        return cow_or_chiken()
    print(f"ты всял {answer}")
    return answer
def read_file(filename:str):
    with open(filename, encoding="utf-8") as file:
        data_list = file.read().split("\n")
        return data_list
# print(read_file("вопросы.txt"))

def quiz(quesions,answers):
    for number,que in enumerate(quesions):
        # print(f"{number +1}. {que}")
        answer = answers[number]
        user_ans = ""
        while user_ans != answer:
            user_ans = input(f"{number +1}. {que}"). lower()
            if user_ans == answer:
                print("вернаа:)")
            elif user_ans != answer:
                print("не вернаа :/")