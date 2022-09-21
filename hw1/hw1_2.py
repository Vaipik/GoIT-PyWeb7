"""
Напишіть клас метаклас Meta, який усім класам, для кого він буде метакласом, встановлює порядковий номер.
"""


class Meta:

    def __new__(cls, name, bases, attrs):
        """

        :param name: class name
        :param bases: class parents
        :param attrs: class attributes
        """
        attrs['class_number'] = Meta.children_number  # New attrs with order
        Meta.children_number += 1
        return type(name, bases, attrs)


Meta.children_number = 0


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data


assert (Cls1.class_number, Cls2.class_number) == (0, 1)
a, b = Cls1(''), Cls2('')
assert (a.class_number, b.class_number) == (0, 1)
