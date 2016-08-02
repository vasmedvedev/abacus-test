import inspect


class CallableInteger(int):

    def __call__(self, *args, **kwargs):
        return self


class ReadOnlyField(object):

    def __set__(self, obj, value):
        raise AttributeError


class CallableIntegerField(ReadOnlyField):

    def __init__(self, value):
        self.field = CallableInteger(value)

    def __get__(self, obj, owner):
        return self.field


class Parent(object):

    true_int_field = CallableIntegerField(1)
    false_int_field = CallableIntegerField(0)

    def __init__(self, *args, **kwargs):
        self.classes = set(cls.__name__ for cls in inspect.getmro(self.__class__)) | {self.__class__.__name__}

    def __getattr__(self, item):
        if item.startswith('is'):
            is_instance = item[2:] in self.classes
            return self.true_int_field if is_instance else self.false_int_field
        return getattr(self, item)

    def __setattr__(self, key, value):
        if key.startswith('is'):
            raise AttributeError
        super(Parent, self).__setattr__(key, value)


class MyError(Exception):
    pass


class First(Parent):
    pass


class Second(Parent):
    pass


class A(First):

    i = 3

    @staticmethod
    def fnc(a):
        if a == 7:
            raise MyError("Error text")
        return a * a * 3
