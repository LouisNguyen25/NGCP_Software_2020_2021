"""Please have all of the following concepts understood by the time we start next Semester:

1. Conditional statements (i.e. if else statements)
2. For and while loops
3. Nested statements 
    ∙(Task 1)
4. Using lists and tuples
    .(Task 2)
5. Creating a function
6. Using a dictionary
    .(Task 3)
7. Error handling
    .(Task 4)
8. File I/O
    .(Task 5)
9. Custom classes
    .(Task 6)
10. Lambda Functions
11. Using pip and import
12. Multi threading 
13. Machine Learning (if you are bored and have time)

Below we will provide exercises for you to complete to get a better understanding of python. If you are already comftorable with any of them,
do not feel the need to do the corresponding exercise. If you do the exercise and want it checked over or just need help, feel free to reach out
to either Donald or Greg on the discord so that we may check it over or provide help. We assume you know the basics of programming and thus have 
not made this too in depth. If you would like further explanations of how any of this works, please do not hesitate to ask.
Also, if there are any errors, let us know.

If there are any topics missing that you would like to learn about or want some practice on, let us know so we can make it for you. Or if you want
more examples of a certain topic, we will make those for you as well.

________________________________________________________________________________________________________________________________________________

Quick tip, # is the comment denotation for python much like the // is in java
"""
"""
Also to block comment use three double quotes(like shown on the line above) which is equivalent to the /*   */ in java

________________________________________________________________________________________________________________________________________________


1. Conditional Statements
	Conditional Statements are great for decision making.
	The basic conditional statements are != , == , < , > , <= , >= , and a little more complex one: in
    We almost always use conditional statements with the if else statements

    So if we wanted to check whether or not some boolean value was true, we could do the following
    
        boolean = True
        if boolean == True:
            .
            .
            .
        
    Since the boolean value was true, the chunk of code under the if statement would be executed.
    We can simplify the code to the following

        boolean = True
        if boolean:
            .
            .
            .

    Checking if boolean == True is redundant because we are just asking if True equals True
    We can also compare numbers using the statements
    if 7 < 5:       This would result in false as 7 is not less than 5
    if 2 + 5 == 7:  This would result to true as 7 equals 7
    etc.

    Python also offers other handy statements to determine if a string or list might contain something inside of it

    if 'ban' in 'banana':
        .
        .
        .

    This will result in true and execute the code underneath it. 
    We can also use this method to check whether a list has an item in it

    list = ['orange', 'pineapple', 'squash']
    if 'banana' in list:
        .
        .
        .
    
    The above if statement would result in false as there is no 'banana' in our list
    
    As you have seen the way to use the conditional statements is with the if statement
    which is very versatile and has the following layout

    if "something":
        do something
    elif "something else":
        do something else
    else:
        "default"

    Lets say we have some mathematical calculation before and want to check to see where the answer is on a range

    answer = some_number
    if answer < 100:
        print('Small number')
    elif answer < 300:
        print('Medium Number')
    elif answer < 600:
        print('Big number')
    else:
        print('Huge number')

    If our answer was 63, we would get an output of 'Small number'
    If our answer was 211, we would get an output of 'Medium number'
    If our answer was 350, we would get an output of 'Big number'
    If our answer was 1900, we would get an output of 'Huge number'

    Notice that once one of the condtions is met and the code under that conditions is executed, no other conditions are checked
    So if the initial if statement is met as True, no other elif or else statements will be processed

    If you want to be big brain, you can do an if statement in one line
    if <expression>: <code to execute>
________________________________________________________________________________________________________________________________________________

2. Loops
    The main two loops that are used in python are the while and for loops. We will show off the basic syntax of the for loop.

    ex. If we want to iterate through a range of numbers.
    for i in range(100): #this goes from 0 to 99 for i.  In other words it is not inclusive
        .
        .
        .

    for i in range(69,100): #this will go from 69 - 99
        .
        .
        .
    
    We can also iterate through a list
    a = ['banana', 'guava', 'pineapple']
    for i in a: #this will iterate through the list from index 0, banana, to the end of the list, pineapple.
        .
        .
        .

    We can also iterate througha string
    for x in "banana": #this loops through every character in a string
        .
        .
        .
    The pass statement is a very useful piece of code in python as it allows you to skip the for loop completely
    for i in range(100):
        pass
    The code here would look inside the for loop and just skip by it

    The continue statement is a very useful piece of code in python as it allows you to skip one iteration of the loop (just like the continue command in java)
    for i in range(100):
        if i ==31:
            continue

    The break statement will break you out of the for loop (just like the break command in java)
    for i in range(100):
        if i == 31:
            break
    So if i = 31, the code will break and the for loop will cease
    
    --------------------------------------------------------------------------------------------------------------------------------------------------------------

    The second most commonly used loop is the while loop with very similar functionality
    while (conditional): #this is the basic look of a while loop
        .
        .
        .

    ex.
    This code will go through the while loop 10 times
    index = 0
    while index < 10:
        print(index)
        index = index + 1

    This while loop will continue until the flag is set to false
    flag = True
    while (flag):
        print("The flag is true")
        flag = False

    Note: You can tack on an else statement on the end of either a for loop or a while loop
    This else statement will execute once the loop has finished running
    ex. 
    for i in range(13):
        .
        .
        .
    else:
        print("I am an else statement")

________________________________________________________________________________________________________________________________________________

3. Nested Statements
    You can also tack together for loops and while loops and if statements to create stronger code.
    Lets say I wanted to learn my times tables
    for i in range(11):
        for x in range(11):
            print(f"The result of {i} x {x} is: {i * x}") #the f print statement is like the printf in java


    Or I wanted to go through a list of numbers and wanted to determine when I hit 2
    for i in range(-14, 69):
        if i == 2:
            print("Huzzah")
            break

    That is the basic gist of the nested statements and here is the first task we would like you guys to do.
    Once again, you do not need to do this if you already feel comftorable, but we expect you to come with these skills
    already known on day one of the semester.

    Task: Create a continuous rock paper scissors game 
        Continuous as in the user would have to quit the game for the game to continue running.
        So after every game is over ask if the user want to play again.  If no end the game.

    To do this you are going to need user input, shown below.
    variable = input("Your name: ") #this will prompt you when you run your code to input a value.

    Below is a rough template of how the game might be setup, feel free to use this or not

        import random
        game_choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(game_choices)

        valid_choice = False
        user_choice = ""
        while not valid_choice:
            user_choice = input("rock, paper or scissors?: ").lower().strip()
            if(user_choice in game_choices):
                valid_choice = True
            else:
                print("Please enter a valid option\n")

        #Please write your conditional statements here checking who would win
        #then print out the winner of the game, the player or the computer

________________________________________________________________________________________________________________________________________________

4.Lists and tuples
    Lists and tuples both function very similarly to arrays in other languages in that they can hold data inside of them.
    The great thing about python is that since there are no distinct data types, we can put a string, an integer, or even another
    list inside of a list or tuple and it will still be valid.

    To create a list:
    list = ['item1', 'item2', 'item3']
    To create a tuple
    tuple = ('item1', 'item2', 'item3')

    What is the main difference between a tuple and a list is that a list is mutable while a tuple is immutable. 
    Immutable means not changable or as Greg says non alterable so we cannot change it in run time.
    Tuples cannot be copied either.
    You may ask, why do tuples exist? They take up less space than a list, thus operations on tuples are quicker like Lightining McQueen
    Lists have infinite Length as well while tuples are fixed.

    Most of the commands are very similar on both, but in this quick guide, I will only be going over list commands as they are used more
    in my experience.

    list = ['avacado', 'banana', 'celery']
    print(list) #prints out the entire list, so "['avacado', 'banana', 'celery']" would be printed

    We can also access elements of the list
    print(list[1]) #prints 'banana'

    Python also has a wrap around feature so we can work from the back to the front
    print(list[-1]) #would print 'celery'

    We can take a range of the list
    print(list[0:2]) #this would print ['avacado', 'banana']

    We can also overwrite values
    list[1] = "bangladesh"
    print(list[1]) # we would get 'bangladesh'

    we can loop through the list as already seen
    for i in list: #will go through every item
        .
        .
        .
    
    If we want to add an item we use append
    list.append('dino nuggets') #this will add 'dino nuggets' at the end of the list
    print(list) #yields ['avacado', 'banana', 'celery', 'dino nuggets']

    If we want to insert an item at a specific index we use insert
    list.insert(1, 'dino nuggets') #adds 'dino nugget' at index 1
    print(list) #yields ['avacado','dino nuggets' ,'banana', 'celery']

    If we want to remove an item
    list.remove('banana') #removes banana from the list

    If we want the length of the list
    len(list) #We would get 3 as there are three items in the list
    
    There are a bunch of different things you can do with lists like concatenate and find the difference between two lists,
    So if ever needed look up the other uses or ask us and we will be happy to help

    Task 2: Please create a program to do the following:
    Create a list with numbers 1 - 30 using a loop
    Then add the numbers all together which should get you: 465
    After that add only the odd numbers together which should get you: 225
    Lastly, remove numbers 10 - 20 and print out the list

    to check if a number is odd, use modulo (%) with an if statement
    ex. 7%2 = 1
        6%2 = 0
    An odd number modulo 2 will give you 1 and aen even number will give you 0

________________________________________________________________________________________________________________________________________________

5. Functions
    Functions are amazing tools - "Donald"
    Wayne Gretzky - "Michael Scott"

    To create a function, we use 'def' which stands for definition
    ex. Lets create a function that takes a number,x and prints out all numbers 0 - x
    def printNumbers(x):
        for i in range(x):
            print(i)

    The to call our function,
    numbers = 18
    printNumbers(numbers) #would print all the numbers we want

    Python functions have to be declared before they can be called unlike in java

    If we want to return something from a function, we use return
    def add(x, b=20):
        return x + b

    Also in the above function, we can also set default values to a function so if we did
    answer = add(20)
    print(answer) #we would get 40
    but if we do add(20, 15) # we would get 35 as we can overwrite that local parameter

    Also all variables in a function are local, so if you change a parameter variable in the function it doesnt change outside that scope

________________________________________________________________________________________________________________________________________________

6. Dictionaries
    A dictionary is a set of items relating to one another that are indexed.
    Dictionaries can also act like switch case blocks from java
    We can create a dictionary by:
    dict = {
        "fruit" : "banana",
        "soda" : "root beer",
        "favorite number" : 13
    }

    So we can use this to relate items to one another,
    ex. output = dict["fruit] #output would then be "banana"

    We can also change the values of a dict
    dict["fruit"] = "orange"
    dict["fruit"] #output would be "orange" now

    if we want all the dictionary keys
    for x in dict:
        print(x)

    if we want all the values
    for x in dict:
        print(dict[x])

    or lets say we want both side by side
    for x, y in dict.items():
        print(x, y)

    Does a key exist?:
    if "fruit" in dict:
        .
        .
        .
    
    Want to add an item?
    dict["drugs"] = "heroine"

    Want to remove an item?
    dict.pop("drugs")

    You can also nest dictionaries and do other fun stuff with them like copy them and triple nest them. WOWIE!

    Task 3: Please recreate the rock paper scissors activity but with a dictionary.
    For example if the computer randomly chose "scissors", we would do dict["scissors"]
    and that would return paper. So if your play was paper, you would lose, else if you
    would do dict[your play], and if that result equaled the computer play, you would win, 
    else it is a tie.
    I know this was not the best explanation, but if further help is needed, just google
    'rock paper scissors with python dictionaries' and you will get plenty of results

________________________________________________________________________________________________________________________________________________

7. Error handling
    the most classic error handler is the try catch block
    try:
        .
        .
        .
    catch error:
        .
        .
        .
    
    This will execute the code underneath the try block and if an error occurrs, it will check if the error is being caught
    and if the catch block is catching the error, the code under the catch block runs
    So lets say we are trying to get the user to input a number to us:
    
    while True:
        try:
            number = int(input("Gimme a number: "))
            break
        except ValueError:
            print("That's not a number")

    So this block of code will run asking for a number. If anything but a number is entered we will get a ValueError when we
    try to cast it to an int which is what int() does.
    If anything but a number is put in, we will execute the except block which will execute the print statement and since we
    did not break out of the while loop, we would run through the try catch block again

    If we want to catch multiple errors we can do
    try:
        .
        .
        .
    except (error1, error2, error3, ...):
        pass

    Or if we want specific things to happen per error
    try:
        .
        .
        .
    except error1:
        .
        .
    except error2:
        .
        .

    You can also make your own exceptions ocurr by using raise. So lets say we want a number 1-100 entered and we get 211
    if number > 100 or number < 1:
        raise NameError("Your number was outside the bounds")

    The user will get an error saying 'Your number was outside the bounds' if their number was not in the bounds

    There is also the try-finally block
    try:
        .
        .
        .
    finally:
        .
        .
        .
    
    The finally block executes no matter what so even if no error occurrs in try, we go to finally still
    We can combine them as such

    try:
        .
        .
        .
    catch error:
        .
        .
    finally:
        .
        .
        .

    The try and finally blocks will be ran no matter what and the catch block will run if an error occurrs in the try block

    Task 4. Please have a try catch block where in the try block you attempt to divide by 0, then have the catch block
    succesfully catch that error. Inside of the catch block, create a list that has 4 elements in it then try to access
    the fifth element. Have a catch block to handle that error as well that prints "Success"

________________________________________________________________________________________________________________________________________________

8. File I/O
    It is generally great use to do all of your file IO tasks under a try-catch-finally block or some variation of it
    Or we can use the with command which I will quickly run over
    Lets say we want to open a file up, we can do
    with open('text.txt' , 'w') as file:
        .
        .
        .

    This will open a file in your current directory called 'text.txt' if it exists and create it if it does not. 'w' stands for writing as 
    we are going to write as the file. You can also put 'r' if you want to read from the file instead.
    'as file' means that we can reference this file as 'file' while underneath the with block.
    The great thing about the with block is that the file will be properly closed after leaving the block without having to write the
    command to close the file which would be file.close()

    If you want to open a file without with, you would do:
    file = open('text.txt', 'r')
    for line in file:
        print(line)     #would print every line of the file

    Now lets say we want to write lines to the file
    with open('text.txt' , 'w') as file:
        file.write("orangutan") #line 1
        filw.write("this dude") #line 2

    What if we want to read the file now?
    with open('text.txt' , 'w') as file:
        file.read() #output everyline of the file
        file.readline() #outputs a single line of the file and then moves onto the next keeping track of how many lines had been read

    However python likes to try and be helpful all the time so if we ran print(file.readline()) twice, we would get:
    orangutan

    this dude

    Notice the space between the two words. Python always has a new line character anyttime a new print is executed.
    We can get around this by doing print(file.readline(), end = '')
    This will change what the end character is on the print statement. So instead of a new line character, it is an empty character

    One nifty thing you can do is read the lines in reverse
    with open('test.txt', 'r') as file:
    lines = file.readlines()
    for line in reversed(lines):
        print(line)

    As always, there are more commands with reading and writing files, but they are well documented on the internet already

    Task 5. Please write the first 30 numbers to a txt file and then read the numbers ends to center
    So the result should be:
        29
        0
        28
        1
        27
        2
        .
        .
        .

________________________________________________________________________________________________________________________________________________

9. Classes
    Python just like java is an object oriented programming language so it is very useful to be able to create your own objects, which classes 
    help you do.
    For this example, we will be creating a car class so that we can represent different types

    class Car:
        def __init__(self, make, model, engine, cost): #__init__ gets run at time of object creation
            self.make = make
            self.model = model
            self.engine = engine
            self.cost = cost

        def getInfo(self):
            print(f"Make: {self.make} \nModel: {self.model} \nEngine: {self.engine} \nCost: {self.cost} \n ")

        def changePrice(self, newPrice):
            self.price = newPrice

        def makeNoise(self):
            print("Car goes Vroooooom")

    We put 'self' inside of every function as the function needs to know whose variables it is referencing while inside of it. Similar to 'this' in java
    Now let's say we wanted to create our own brand spanking new cars
    Tacoma  = Car("Toyota", "Tacoma", "6 cylinder", "55k")
    Tundra = Car("Toyota", "Tundra", "2 cylinder", "13k")
    Hylander = Car("Toyota", "Hylander", "4 cylinder", "183k")

    This would create three different objects, the Tacoma, Tundra, and Hylander
    On each of these objects we can run the getInfo, changePrice, and makeNoise function on
    If we did:
        Tacoma  = Car("Toyota", "Tacoma", "6 cylinder", "55k")
        Tundra = Car("Toyota", "Tundra", "2 cylinder", "13k")
        Hylander = Car("Toyota", "Hylander", "4 cylinder", "183k")

        Tundra.getInfo()
        Tacoma.getInfo()
        Tacoma.changePrice("420.69")
        Tacoma.getInfo()
        Hylander.makeNoise()

    Our output would be:
        Make: Toyota 
        Model: Tundra
        Engine: 2 cylinder
        Cost: 13k

        Make: Toyota
        Model: Tacoma
        Engine: 6 cylinder
        Cost: 55k

        Make: Toyota
        Model: Tacoma
        Engine: 6 cylinder
        Cost: 420.69

        Hylander Car goes Vroooooom

    Task 6: You are the local Venezuelan drug lord and you cannot keep track of all your drugs and prices
    please make a 'Drug' class that contains the name of the drug, the price per gram, the color, and the amount owned in grams.
    This class should have a couple different functions:
        Function 1: Given a weight in grams, how much would that much of the drug cost. Before returning that value, ensure that
        you have that much drug left otherwise return the max they can buy at that point.
        Function 2: As you farm more drugs, you should be able to increase the amount you have. This function will increase how
        much of that drug you own in grams.
        Function 3: This function will advertise said drug. It will print out the name of it in all caps
                You can make a string in caps by doing variable_name.upper()

     Disclaimer: I am pretty tired while writing this task so please dont judge me lol

     Classes can also uses inheritance which I think you all know, but if not please contact us and we will explain it
________________________________________________________________________________________________________________________________________________

10. lambda Functions
    A lambda function is a one line function. They can take as many arguments as you want, but only can do one expression
    They are great for code simplification if a function was only going to be used once
    ex. Lets add two numbers with a normal function
    def add(x, y):
        return x + y
    print(add(5,3)) # we would get 8

    Now lets do the same thing with a lambda function
    add = lambda x, y: x + y
    print(add(5, 3)) # we would once again get 8

    Lets reduce this even further
    (lambda x, y: x + y)(5, 3) # once again we get 8

    If you are not planning on reusing a function, we can use the lambda expression to really simplify our code.
    I personally am not a huge fan of using lambdas as even though they offer simplicity, it just does not feel quite right to me. I will not be 
    explaining them further here because I am not super familiar with them. You can explore on the internet if you want more on them

________________________________________________________________________________________________________________________________________________

11. Using pip and import
    Pip comes in a package with your python installation, so you will have it if you checked the box when installing otherwise go here:
    https://pip.pypa.io/en/stable/installing/ to install Pip

    Pip is a command line tool that lets you install python libraries very easily.
    For example, lets say I wanted to install a popular machine learning library: 'tensorflow'
    I would open up my command promp and write 'pip install tensorflow'
    
    Now whenever I wanted to use tensorflow, I can use the import function.
    Import tells your program that you want thus library referenced in your current directory. So if i want to use the random library to generate
    a random number I would need to do

    import random #imports the random library so we can use it
    print(random.randint(0,9))  #generate a random number 0-8

    Using import is what python is all about. There are thousands of opensource libraries ready to be used that make our lives easier.

________________________________________________________________________________________________________________________________________________

12. Multithreading
    We both know a little about multi threading but are not as well versed as the previous topics. So if our explanation is unsatisfactory,
    please see the python website below
    https://docs.python.org/3/library/multiprocessing.html#using-a-pool-of-workers

    Our favorite way to use multi processing is with the pool of workers. Traditionally, you have one worker. So you give that worker a task,
    they complete it and come back to you ready for the next task. This is great if you want everything done in linear order. However, sometimes
    you want to do stuff at the same time. Lets say you have two people waiting to buy something at a store. It would be much better to service 
    both simultaneously rather than have one being served at a time. You could potentially cut your time in two. However, multi processing
    takes more overhead power from the CPU.

    A super simple example is running multiple inputs through the same function. let us say we have a factorial function
        def factorial(number):
        fact = 1
        for i in range(1, 1 + number):
            fact = fact * i
        return fact

    And we want to factorial a few different numbers
    Traditionally, we might do
        factorial(8)
        factorial(16)
        factorial(24)
        factorial(32)
    
    This would take some amount of time and do all of the processes for us
    Now, if we wanted to do the same thing with multi processing, we could create the pool of workers. Once again, we are using the with command 
    cause its amazing.
        with multiprocessing.Pool(5) as p:      #declaring a multiprocessing pool object
            p.map(factorial, [32, 24, 16, 8])   #here we are mapping multiple factorial function calls to our pool

    This calls the factorial function with the same inputs as the above function
    Now you might be thinking, "WOWeeeee!!!, this is amazing and needs to be used everywhere."
    Unfortunately, since there is more overhead to multiprocessing, there is a time to start up the pool

        import multiprocessing
        import time

        def factorial(number):
            fact = 1
            for i in range(1, 1 + number):
                fact = fact * i
            return fact

        if __name__ == '__main__':
            before = time.perf_counter()
            #denotes the number of workers
            with multiprocessing.Pool(5) as p:
                p.map(factorial, [800, 600, 400, 200])
            after = time.perf_counter()
            print(after - before, '\n')

            before = time.perf_counter()
            [factorial(800), factorial(600), factorial(400), factorial(200)]
            after = time.perf_counter()
            print(after - before)

    The above code runs the factorial function with four different inputs. It first runs it in the multiprocessing matter
    then in the traditional way timing both. The output of this code with these numbers is: 
    0.26933419999999997 seconds for the multiprocessing and 
    0.00105069999999996 seconds for the traditional way

    Now lets say we ran the same function with (80000, 60000, 40000, 20000). We would get
    4.1761948 seconds for multiprocessing
    5.708471300000001 seconds for traditional

    This difference in time will continue to grow with multiprocessing getting faster the bigger the processes that have
    to complete.

    Please let Donald know if you want more added to this practice bit.
"""