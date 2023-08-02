import function
# from function import say_hello


# name = "Tio" 
# function.say_hello("Kio")
# say_hello(name)
# food = function.cow_or_chiken()
# print(f"{name} сейчас будет кушать {food}")

questions = function.read_file("quiz/вопросы.txt")
answers = function.read_file("quiz/ответы.txt")
function.quiz(questions, answers)