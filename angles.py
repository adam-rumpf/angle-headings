"""Defines a lightweight Python Angle class."""

### Consider redoing the conventions to make all results between -180 and 180.
### We might be able to make this work more naturally with negation corresponding to subtraction.

### Methods to overwrite:
### __sub__            a - b
### __floordiv__       a // b
### __mod__            a % b (have this return the measure modulo any base)
### (include a method to get or change the attributes)
### __mul__            a * b
### __pow__            a ** b
### __truediv__        a / b
### __iadd__           a += b
### __ifloordiv__      a // b
### __imod__           a %= b (have this update the angle's unit)
### __imul__           a *= b
### __ipow__           a **= b
### __isub__           a -= b
### __itruediv__       a /= b
### __lt__             a < b
### __le__             a <= b
### __eq__             a == b
### __ne__             a != b
### __ge__             a >= b
### __gt__             a > b
### __round__          rounds self (may have an optional ndigits keyword argument)
### __trunc__          truncates self to int
### __floor__          floor of self
### __ceil__           ceiling of self

### Note that _normalize can go at the end of some of these (like negation)
### due to the rules of modular arithmetic.

### Whatever definitions we arrive at, we should try to have the operations satisfy the basic algebraic properties of modular arithmetic.
### In particular it would be good if addition and subtraction (as well as negation) made sense together, but there is probably no particular need to think very deeply about multiplication and division.

import math

class Angle:
    """A Python class for representing and performing calculations with
    angles.

    This is a lightweight data structure for representing angles. It is
    designed to make performing common operations with angles easy, with a
    focus on applications involving headings in the 2D plane.

    An Angle object has three public attributes:
        measure (float) -- the numerical measure of the angle, used for most
            calculations
        mod (float) -- the measure of one full revolution (e.g. 2pi for
            radians, 360 for degrees)
        unit (str) -- string version of the angle's unit

    All Angle measures are normalized to be between -1/2 (exclusive) and 1/2
    (inclusive) of a full revolution, with negative measures indicating
    clockwise rotation and positive indicating counterclockwise.

    Binary operations that are defined between Angle objects use the first
    object's unit. Most (Angle, Angle) binary operators have an equivalent
    (Angle, float) version that performs the same operation, but treating the
    given float as the measure of a second angle that matches the first
    angle's unit.

    The following is a summary of the major public Angle methods.
        Angle([measure[, mod]]) -- constructor can set the initial measure and
            mod (default 0.0 and 2pi, respectively)
        convert([mod]) -- returns the measure of the Angle converted to a
            different unit

    The following operators are defined for Angle objects, and perform their
    usual float operations on the Angle's measure, returning a numerical value
    of the appropriate class.
        abs(A) (Angle) -- absolute value of measure
        int(A) (Angle) -- truncates measure to int
        float(A) (Angle) -- returns measure
        round(A) (Angle) -- rounds measure to nearest int

    The following operators are defined for Angle objects, and combine the
    Angle with either another Angle or a float. In all cases the expected
    operation is performed on the Angles' measures (as floats), and a new
    Angle object (whose unit matches the first Angle) is returned, normalized
    to be between -1/2 (exclusive) and 1/2 (inclusive) of a full revolution.
        +A (Angle) -- exact copy of this Angle
        -A (Angle) -- negates measure
        A + B (Angle, Angle) -- adds measures
        A + b (Angle, float)
        A += B (Angle, Angle) -- combined addition and assignment
        A += b (Angle, Angle)
        A - B (Angle, Angle) -- subtracts measures
        A - b (Angle, float)
        A -= B (Angle, Angle) -- combined subtraction and assignment
        A -= b (Angle, float)
        A * b (Angle, float) -- multiplies measure by a scalar
        A *= b (Angle, float) -- combined multiplication and assignment
        A / b (Angle, float) -- divides measure by a scalar
        A /= b (Angle, float) -- combined division and assignment

    The following comparison operators are defined for Angle objects, and
    perform the expected comparison with the Angle's measure and another
    Angle's measure or a float. Measures are considered to be equal if their
    normalized values are equal after conversion to a common unit.
        A == B (Angle, Angle) -- equal (after conversion to the same unit)
        A == b (Angle, float)
        A != B (Angle, Angle) -- not equal
        A != b (Angle, float)

    The following comparison operators are defined for Angle objects, and
    compare the Angle to either another Angle or a float. In all cases, the
    comparison's result is based on the smallest angle between the two
    arguments. If the smallest angle between A and B places A counterclockwise
    relative to B, then we say that A > B, and if it places A clockwise
    relative to B, then we say that A < B. By convention, if A and B are
    diametrically opposed, we say that we say that A > B if A is the caller
    and B > A if B is the caller. In all cases the comparison is performed on
    the Angles' measures (as floats), after both have been converted to the
    first argument's unit.
        A > B (Angle, Angle) -- smallest A--B angle is CW
        A > b (Angle, float)
        A >= B (Angle, Angle) -- A > B or A == B
        A >= b (Angle, float)
        A < B (Angle, Angle) -- smallest A--B angle is CCW
        A < b (Angle, float)
        A <= B (Angle, Angle) -- A < B or A == B
        A <= b (Angle, float)
    """

    # Static attributes for accepted unit names
    rad_str = {"radians", "radian", "rad", "r"}
    deg_str = {"degrees", "degree", "deg", "d"}
    grad_str = {"gradians", "gradian", "grad", "g"}

    #=========================================================================
    # Technical Methods
    #=========================================================================

    def __init__(self, measure=0.0, mod="radians"):
        """Angle.__init__([measure[, mod]]) -> Angle
        Angle constructor.

        Keyword arguments:
        measure (float) [0.0] -- initial angle measure
        mod (str or float) ["radians"] -- angle unit, or measure of one full
            revolution

        The optional "mod" argument is used to specify the unit of angle
        measure. If given as a number, this number is treated as the measure
        of one full revolution. If given as a string, it uses a standardized
        unit of measure. The following strings are recognized:
            radians, radian, rad, r -- radians (2pi)
            degrees, degree, deg, d -- degrees (360)
            gradians, gradian, grad, g -- gradians (400)
        """

        # Parse unit arguments
        self._set_mod(mod)

        # Set initial measure (automatically normalizes self)
        self.measure = float(measure) # current angle measure

    #-------------------------------------------------------------------------

    def __str__(self):
        """Angle.__str__() -> str
        Angle string conversion.

        Returns the measure of the angle as a string, along with an
        abbreviation of the angle unit.
        """

        return str(self.measure) + " " + self.unit

    #-------------------------------------------------------------------------

    def _set_mod(self, mod):
        """Angle._set_mod(mod) -> None
        Sets mod and unit based on a given mod input.

        Positional arguments:
        mod (str or float) -- angle unit, or measure of one full revolution

        This is a private method called during the Angle's initialization, or
        when its mod value is reset. It includes a procedure for parsing the
        input (which can have several different types) and setting the unit
        string.
        """

        # Initialize mod and unit
        self.mod = 0.0 # full revolution measure
        self.unit = "rad" # name of unit for string output

        # Attempt to parse string mod argument
        if type(mod) == str:
            # Search through recognized words
            if mod in Angle.rad_str:
                self.mod = 2*math.pi
                self.unit = "rad"
            elif mod in Angle.deg_str:
                self.mod = 360.0
                self.unit = "deg"
            elif mod in Angle.grad_str:
                self.mod = 400.0
                self.unit = "grad"
            else:
                # If unrecognized, raise a value error
                raise ValueError("unrecognized unit name string")
        else:
            # Otherwise attempt to parse numerical mod argument
            self.mod = abs(float(mod))
            self.unit = "/ " + str(self.mod)

        # Rename unit for recognized moduli
        if mod == 2*math.pi:
            self.unit = "rad"
        elif mod == 360.0:
            self.unit = "deg"
        elif mod == 400.0:
            self.unit = "grad"

    #-------------------------------------------------------------------------

    @property
    def measure(self):
        """Angle.measure() -> float
        Retrieves normalized angle measure.
        """

        return self._measure

    #-------------------------------------------------------------------------

    @measure.setter
    def measure(self, value):
        """Angle.measure(value) -> None
        Updates the angle measure, then automatically normalizes.

        Positional arguments:
        value (float) -- new angle measure
        """

        # Set private measure variable
        self._measure = value

        # Normalize if needed
        if self._measure < -self.mod/2 or self._measure > self.mod/2:
            self._measure = (((self._measure + (self.mod/2)) % self.mod)
                             - (self.mod/2))
        if (self._measure == -self.mod/2):
            self._measure = -self._measure

    #=========================================================================
    # Custom Methods
    #=========================================================================

    def convert(self, new_mod="radians"):
        """Angle.convert([mod]) -> float
        Returns the angle measure converted into a different unit.

        Positional arguments:
        mod (str or float) ["radians"] -- angle unit, or measure of one full
            revolution

        The resulting measure is between (-1/2,1/2] full revolutions (relative
        to the given unit).
        """

        # Attempt to parse string mod argument
        if type(new_mod) == str:
            # Search through recognized words
            if new_mod in Angle.rad_str:
                new_mod = 2*math.pi
            elif new_mod in Angle.deg_str:
                new_mod = 360.0
            elif new_mod in Angle.grad_str:
                new_mod = 400.0
            else:
                # If unrecognized, raise a value error
                raise ValueError("unrecognized unit name string")
        else:
            # Otherwise attempt to parse numerical mod argument
            new_mod = abs(float(new_mod))

        # Convert measure as a fraction of a complete revolution
        return ((self._measure/self.mod) % 1.0)*new_mod

    #=========================================================================
    # Overloaded Numerical Operators
    #=========================================================================

    def __abs__(self):
        """abs(Angle) -> float
        Returns the absolute value of the Angle's measure.
        """

        return abs(self.measure)

    #-------------------------------------------------------------------------

    def __int__(self):
        """int(Angle) -> int
        Returns the measure of the Angle, cast as an integer.
        """

        return int(self.measure)

    #-------------------------------------------------------------------------

    def __float__(self):
        """float(Angle) -> float
        Returns the measure of the Angle, cast as a float.
        """

        return float(self.measure)

    #-------------------------------------------------------------------------

    def __round__(self):
        """round(Angle) -> int
        Returns the measure of the Angle, rounded to the nearest integer.
        """

        return round(self.measure)

    #=========================================================================
    # Overloaded Operators
    #=========================================================================

    def __pos__(self):
        """+Angle -> Angle
        Returns an exact copy of this Angle.

        The returned Angle has this Angle's mod and measure, automatically
        normalized to lie within (-1/2,1/2] fullrevolutions.
        """

        return Angle(self.measure, self.mod)

    #-------------------------------------------------------------------------

    def __neg__(self):
        """-Angle -> Angle
        Returns a new Angle with the negative of this Angle's measure.

        The returned Angle has this Angle's mod, and the negative of its
        measure, automatically normalized to lie within (-1/2,1/2] full
        revolutions.
        """

        return Angle(-self.measure, self.mod)

    #-------------------------------------------------------------------------

    def __add__(self, other):
        """Angle + Angle -> Angle
        Returns a new Angle with the sum of two angles' measures.

        Positional arguments:
        other (Angle or float) -- measure to be added to this angle's measure

        This is a method of the operator's first argument. If the second
        argument is an Angle, it is first converted to this Angle's unit. If
        the second argument is a float, it is assumed to already match this
        Angle's unit.

        The returned Angle has this Angle's mod, and its measure is
        automatically normalized to lie within (-1/2,1/2] full revolutions.
        """

        # Determine class of second argument
        if type(other) == Angle:
            # If another angle, convert the other argument
            theta = other.convert(self.mod)
        else:
            # Otherwise attempt to parse second argument as a float
            theta = float(other)

        # Add to this Angle's measure and return result
        return Angle(self.measure + theta, self.mod)

### A += B (Angle, Angle) -- combined addition and assignment
### A += b (Angle, Angle)
### A - B (Angle, Angle) -- subtracts measures
### A - b (Angle, float)
### A -= B (Angle, Angle) -- combined subtraction and assignment
### A -= b (Angle, float)
### A * b (Angle, float) -- multiplies measure by a scalar
### A *= b (Angle, float) -- combined multiplication and assignment
### A / b (Angle, float) -- divides measure by a scalar
### A /= b (Angle, float) -- combined division and assignment

    #=========================================================================
    # Overloaded Equality Comparisons
    #=========================================================================

    #=========================================================================
    # Overloaded Inequality Comparisons
    #=========================================================================

##############################################################################

a = Angle(1, 2*math.pi)
b = Angle(180, "deg")
c = Angle(math.pi, 2*math.pi)
d = Angle(10, "deg")
e = Angle(350, "deg")
f = Angle(0)
g = Angle(2*math.pi)
print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
print(g)
print(b.convert("rad"))
print("-"*20)
print(e)
print(abs(e))
print(int(e))
print(float(e))
print(round(e))
print("-"*20)
print(-a)
print(a+a)
print(a+b)
print(Angle(3*math.pi/4) + Angle(math.pi/2))
