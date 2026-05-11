#9-1
print("LAB 9-1")
#1
a = (200).__sub__(100)
print(a)
b = (200).__mul__(100)
print(b)
c = (200).__truediv__(100)
print(c)
#2
list_1 = [10, 20, 30, 40].pop()
print(list_1)
#3
print("2) keys")
#4
print(dir(int))
#5
print(dir(list))

#9-2
print("\nLAB 9-2")
#1
print("a) 데이터와 그 데이터를 처리하는 함수를 '겍체'라는 하나의 단위로 묶어서 프로그램을 구성하는 방식.")
print("b) 프로그램을 일련의 순차적인 명령 수행으로 파악하는 방식.")
print("c) 사용자가 컴퓨터와 상호작용할 때, 텍스트 명령어가 아닌 아이콘, 버튼, 메뉴 등 그래픽 요소를 통해 마우스나 터치로 조작할 수 있게 해주는 환경.")
#2
print("객체 지향 프로그래밍 기법은 프로그램을 독립적인 기능을 가진 객체들의 조립으로 보는 것이고, 절차적 프로그래밍은 위에서 아래로 흐르는 명령으로 보는 것이다.")
#9-3
print("\nLAB 9-3")
#1
print("a) 객체가 가져야 할 데이터와 기능을 정의해 놓은 것")
print("b) 클래스를 바탕으로 만들어진 것")
print("c) 클래스로부터 특정 객체가 메모리에 실제로 생성된 상태")
print("d) 객체가 가지고 있는 상태나 특징을 나타내는 데이터")
print("e) 객체가 할 수 있는 기능이나 행동")
#9-4
print("\nLAB 9-4")
class Dog :
    def bark(self) :
        print("멍멍~~")
my_dog = Dog()
my_dog.bark()

#9-5
print("\nLAB 9-5")
class Dog :
    def __init__(self, name) :
        self.name = name
    def bark(self) :
        print("멍멍~~")
my_dog = Dog('Jindo')
my_dog.bark()

#9-6
print("\nLAB 9-6")
class Dog :
    def __init__(self, name) :
        self.name = name
    def __str__(self) :
        return self.name
my_dog = Dog('Jindo')
print("my_dog의 정보 :", my_dog)

#9-7
print("\nLAB 9-7")
n = 100
m = 100
if n is m :
    print("n is m")
else :
    print("n is not m")
print("n과 m이 같기 때문이다.")

#9-8
print("\nLAB 9-8")
class Vector2D :
    def __init__(self, v1, v2) :
        self.v1 = v1
        self.v2 = v2
    def __mul__(self, other) :
        return Vector2D(self.v1 * other.v1, self.v2 * other.v2)
    def __truediv__(self, other) :
        return Vector2D(self.v1 / other.v1, self.v2 / other.v2)
    def __neg__(self) :
        return Vector2D(-self.v1, -self.v2)
    def __str__(self) :
        return "({}, {})".format(self.v1, self.v2)
v1 = Vector2D(30, 40)
v2 = Vector2D(10, 20)
print("v1 * v2 =", v1 * v2)
print("v1 / v2 =", v1 / v2)
print("-v1 =", -v2)

#9-9
print("\nLAB 9-9")
class Vector2D :
    def __init__(self, v1, v2) :
        self.v1 = v1
        self.v2 = v2
    def length(self) :
        return (self.v1 ** 2 + self.v2 ** 2) ** 0.5
    def __gt__(self, other) :
        return self.length() > other.length()
    def __ge__(self, other) :
        return self.length() >= other.length()
    def __lt__(self, other) :
        return self.length() < other.length()
    def __le__(self, other) :
        return self.length() <= other.length()
    def __str__(self) :
        return "({}, {})".format(self.v1, self.v2)
v1 = Vector2D(30, 40)
v2 = Vector2D(10, 20)
print("LAB 9-9")
print("v1 > v2 =", v1 > v2)
print("v1 >= v2 =", v1 >= v2)
print("v1 < v2 =", v1 < v2)
print("v1 <= v2 =", v1 <= v2)

#9-10
print("\nLAB 9-10")
#1
class Rect :
    def __init__(self, width, height) :
        self.width = width
        self.height = height
r1 = Rect(100, 200)
print(r1.__dict__)
print(r1.__dict__['width'])

#2
class Rect :
    def __init__(self, width, height) :
        self.__width = width
        self.__height = height
r1 = Rect(100, 200)
print(r1.__dict__)
print(r1.__dict__['_Rect__width'])
