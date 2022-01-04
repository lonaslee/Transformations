from __future__ import annotations
from math import sqrt


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)

    def __str__(self) -> str:
        return f'{round(self.x, 2), round(self.y, 2)}'

    def __bool__(self) -> bool:
        if self.x and self.y:
            return True
        else:
            return False
    
    def translate(self, shift: Point):
        original = Point(self.x, self.y)
        self.x, self.y = self.x + shift.x, self.y + shift.y
        return original

    def reflect(self, line_of_refl: Equation):
        original = Point(self.x, self.y)
        if line_of_refl.rslope == 'undef':
            shift = abs(self.x - line_of_refl.m)  # If x is to the right of the
            if self.x >= line_of_refl.m:          # line, then shift has to be
                shift *= -1                       # negative for the next point
            self.x = line_of_refl.m + shift
        elif line_of_refl.rslope == 0:
            shift = abs(self.y - line_of_refl.m)
            if self.y >= line_of_refl.m:
                shift *= -1
            self.y = line_of_refl.m + shift
        else:
            perp_line = Line(self, None, None, line_of_refl.m ** -1 * -1).eq
            intersection = perp_line == line_of_refl
            len_from_point = Line(self, intersection).length
            new_points = Line(intersection, None,
                              len_from_point, perp_line.m).b
            if str(new_points[0]) == str(self):
                self.x, self.y = new_points[1].x, new_points[1].y
            else:
                self.x, self.y = new_points[0].x, new_points[0].y
        return original


class Line:
    def __init__(self, a: Point, b: Point | None,
                 d: float = None, m: float = None) -> None:
        self.a = a
        self._b = b
        self._length = d
        self._slope = m

    @property
    def length(self) -> float:
        if not self._length:
            x2, y2 = self.b.x - self.a.x, self.b.y - self.a.y
            self._length = sqrt(x2 * x2 + y2 * y2)
        return self._length

    @property
    def slope(self) -> float | str:
        if not self._slope:
            if d := self.b.x - self.a.x == 0:
                self._slope = 'undef'
            elif n := self.b.y - self.a.y == 0:
                self._slope = 0.0
            else:
                self._slope = n / d
        return self._slope

    @property
    def b(self) -> Point | tuple:
        if not self._b:
            if self.slope == 'undef':
                self._b = (Point(self.a.x + self.length, self.a.y),
                           Point(self.a.x - self.length, self.a.y))
            elif self.slope == 0:
                self._b = (Point(self.a.x, self.a.y + self.length),
                           Point(self.a.x, self.a.y - self.length))
            else:
                xmove = self.length / sqrt(1 + self.slope * self.slope)
                ymove = self.slope * xmove
                self._b = (Point(self.a.x + xmove, self.a.y + ymove),
                           Point(self.a.x - xmove, self.a.y - ymove))
        return self._b

    @property
    def eq(self) -> Equation:
        if self.slope == 'undef':
            return Equation(f'x={self.a.x}')
        elif self.slope == 0:
            return Equation(f'y={self.a.y}')
        else:
            return Equation(f'y={self.slope}x+'
                            f'{self.slope * self.a.x * -1 + self.a.y}'
                            .replace('+-', '-'))


class Equation:
    def __init__(self, eq: str) -> None:
        self.eq = self.clean_eq(eq)
        self.rslope = 'undef' if 'x=' in eq else 0 if 'x' not in eq else None

    def __repr__(self) -> str:
        rep = f'{self.eq} -> {self.m} -> {self.rslope}'
        if not self.rslope:
            rep += f' -> {self.b}'
        return rep
    
    @staticmethod
    def clean_eq(eq: str):
        eq = eq.strip().lower().replace(' ', '').replace('=x', '=1.0x')
        if eq.endswith('x'):
            eq += '+0.0'
        return eq

    @property
    def m(self) -> float:
        if self.rslope:
            return float(self.eq[2:])
        else:
            return float(self.eq[2:self.eq.index('x')])

    @property
    def b(self) -> float:
        return float(self.eq[self.eq.index('x') + 1:].lstrip('+'))

    def __eq__(self, other: Equation):
        if other.rslope == 'undef':
            if self.rslope == 0:
                x, y = other.m, self.m
            else:  # self.rslope is None
                x = other.m
                y = self.m * x + self.b
        elif other.rslope == 0:
            if self.rslope == 'undef':
                x, y = other.m, self.m
            else:  # self.rslope is None
                y = other.m
                x = (y - self.b) / self.m
        else:  # other.rslope is None
            if not self.rslope:
                mval, bval = self.m - other.m, other.b - self.b
                x = bval / mval
                y = self.m * x + self.b
            elif self.rslope == 'undef':
                x = self.m
                y = other.m * x + other.b
            else:  # self.rslope is False
                y = self.m
                x = (y - other.b) / other.m
        return Point(x, y)


def main():
    points_list = []
    print('Getting all points.')
    while True:
        input_point = input('Point: ').strip().strip('()').replace(',', ' ')
        while '  ' in input_point:
            input_point = input_point.replace('  ', ' ')
        input_point = input_point.split(' ', 2)
        try:
            input_point = Point(input_point[0], input_point[1])
            print(input_point)
            points_list.append(input_point)
        except IndexError:
            break
    operation = input('Operations - {T: translate, r: reflect\nOperator: ')
    if operation == 'T':
        t_amount = (input('Amount to translate: ').strip()
                   .strip('()').replace(',', ' '))
        while '  ' in t_amount:
            t_amount = t_amount.replace('  ', ' ')
        t_amount = t_amount.split(' ', 2)
        t_amount = Point(t_amount[0], t_amount[1])
        for p in points_list:
            p.translate(t_amount)
    elif operation == 'r':
        r_line = Equation(input('Equation of the line of reflection: '))
        for p in points_list:
            p.reflect(r_line)
    for p in points_list:
        print(p)


if __name__ == '__main__':
    main()
