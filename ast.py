import abc

class TypeErrorException(Exception):
    pass

class Expr(object):
    __metaclass__ = abc.ABCMeta

    def __add__(self, other):
        return Addition(self, other)

    @abc.abstractmethod
    def evaluate(self, environment):
        pass

    @abc.abstractproperty
    def type(self):
        pass

    @abc.abstractmethod
    def type_check(self):
        pass

class Variable(Expr):
    def __init__(self, name, var_type):
        self.name     = name
        self.var_type = var_type

    def evaluate(self, environment):
        value = environment[self.name]
        if type(value) is not self.type:
            raise TypeErrorException()
        return value

    def type_check(self):
        "With no context, this should always be well-typed"
        pass

    def __str__(self):
        return self.name

    @property
    def type(self):
        return self.var_type

class Addition(Expr):

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def type_check(self):
        if self.lhs.type is not self.rhs.type:
            raise TypeErrorException()

    @property
    def type(self):
        self.type_check()
        return self.lhs.type

    def __str__(self):
        return "{lhs} + {rhs}".format(lhs=self.lhs, rhs=self.rhs)

    def evaluate(self, environment):
        return self.lhs.evaluate(environment) + self.rhs.evaluate(environment)

def main():
    x = Variable(name='x', var_type=int)
    y = Variable(name='y', var_type=int)
    z = Variable(name='z', var_type=int)

    expr1 = x + y + z
    print expr1
    expr1.type_check()
    print "expr1 has type " + str(expr1.type)
    print expr1.evaluate(dict(x=5, y=2, z=3))
    print

    a = Variable(name='a', var_type=str)
    b = Variable(name='b', var_type=str)
    c = Variable(name='c', var_type=str)

    expr2 = a + b + c
    print expr2
    expr2.type_check()
    print "expr2 has type " + str(expr2.type)
    print expr2.evaluate(dict(a='my ', b='little', c=' pony'))
    print

    expr3 = expr1 + b
    try:
        (expr1+b).type_check()
    except TypeErrorException:
        print "Type error in expression " + str(expr3)


if __name__ == "__main__":
    main()
