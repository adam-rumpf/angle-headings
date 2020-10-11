### Consider redoing the conventions to make all results between -180 and 180.
### We might be able to make this work more naturally with negation corresponding to subtraction.

### Methods to overwrite:
### __floordiv__       a // b
### __int__            integer version of self
### __float__          float version of self
### __complex__        complex version of self
### __mod__            a % b (have this return the measure modulo any base)
### (include a method to get or change the attributes)
### __mul__            a * b
### __pos__            +a (returns an exact copy object, ensured to be modded)
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
    """

    # Static attributes for accepted unit names
    rad_str = {"radians", "radian", "rad", "r"}
    deg_str = {"degrees", "degree", "deg", "d"}
    grad_str = {"gradians", "gradian", "grad", "g"}

    #-------------------------------------------------------------------------

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

        # Parse keyword arguments
        self.measure = float(measure) # current angle measure
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

        # Normalize measure
        self._normalize()

    #-------------------------------------------------------------------------

    def _normalize(self):
        """Angle._normalize() -> None
        Normalizes the measure to be between 0 and 1 full revolutions.

        This private method should be called at the beginning of all other
        methods to ensure that a standardized angle measure is used, since all
        calculations assume an angle measure between 0 (inclusive) and 1 (non-
        inclusive) full revolutions.
        """

        self.measure %= self.mod

    #-------------------------------------------------------------------------

    def __str__(self):
        """Angle.__str__() -> str
        Angle string conversion.

        Returns the measure of the angle as a string, along with an
        abbreviation of the angle unit.
        """

        self._normalize()

        return str(self.measure) + " " + self.unit

    #-------------------------------------------------------------------------

    def convert(self, new_mod):
        """Angle.convert(mod) -> float
        Returns the angle measure converted into a different unit.

        Positional arguments:
        mod (str or float) ["radians"] -- angle unit, or measure of one full
            revolution

        The resulting measure is between 0 and 1 full revolutions (relative to
        the given unit).
        """

        self._normalize()

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
        return ((self.measure/self.mod) % 1.0)*new_mod

    #-------------------------------------------------------------------------

    def __abs__(self):
        """Angle.__abs__() -> float
        Angle absolute value operator: abs(a)

        Returns the absolute difference between the current Angle object's
        measure and 0, as a float.

        Specifically, the returned value is the magnitude of the smallest
        rotation that would move this Angle to 0. If this object's measure is
        between 0 and one half revolution, then its absolute value will simply
        equal its measure.  If its measure is between one half and one full
        revolution, then the supplement of its measure will be returned.

        For example, the absolute values of a 10 degree Angle object and a 350
        degree Angle object would both be 10, since in both cases 10 degrees
        (either clockwise or counterclockwise) is the smallest change needed
        to move the angle to 0.
        """

        self._normalize()

        return min(self.measure % self.mod,
                   (self.mod-self.measure) % self.mod)

    #-------------------------------------------------------------------------

    def __add__(self, b):
        """Angle.__add__(b) -> Angle
        Angle addition operator: a + b

        Returns an Angle object whose measure represents the sum of two angle
        measures. The unit of the returned object matches that of the current
        object.

        Positional arguments:
        b (Angle, int, or float) -- angle to add to the current measure

        Adding a number to the current Angle treats the number as a measure of
        the same unit as the current object.

        Adding an Angle to the current Angle results in the other measure
        being converted to the current object's unit, after which the two are
        added.
        """

        self._normalize()

        # If given an Angle object, convert its measure to the current unit
        if type(b) == Angle:
            b = b.convert(self.mod)

        # Sum the measures, restricted to one revolution
        m = (self.measure + b) % self.mod

        # Return an Angle object
        return Angle(m, self.mod)

    #-------------------------------------------------------------------------

    def __neg__(self):
        """Angle.__neg__() -> Angle
        Angle negation operator: -a

        Returns an Angle object whose measure is the conjugate of this
        object's measure (i.e. a nonnegative angle that can be added to this
        object's measure to yield one full revolution).
        """

        self._normalize()

        return Angle((self.mod - self.measure) % self.mod, self.mod)

    #-------------------------------------------------------------------------

    def __sub__(self, b):
        """Angle.__sub__(b) -> Angle
        Angle subtraction operator: a - b

        Returns an Angle object whose measure represents the difference
        between two angle measures. The unit of the returned object matches
        that of the current object.

        The returned measure is the smallest acute angle between the current
        object's measure and the given measure (after conversion), positive if
        this acute angle positions the current angle counterclockwise relative
        to the other and negative otherwise.

        For example, subtracting a 10 degree Angle from a 350 degree Angle
        yields a +20 degree Angle object, since 20 degrees CCW is the smallest
        angle from 350 to 10. On the other hand, subtracting 350 degrees from
        10 degrees yields -20 degrees, since 20 degrees CW is the smallest
        angle from 10 to 350.

        Positional arguments:
        b (Angle, int, or float) -- angle to subtract from the current measure

        Subtracting a number from the current Angle treats the number as a
        measure of the same unit as the current object.

        Subtracting an Angle from the current Angle results in the other
        measure being converted to the current object's unit, after which the
        two are subtracted.
        """

        self._normalize()

        # If given an Angle object, convert its measure to the current unit
        if type(b) == Angle:
            b = b.convert(self.mod)

        # Find the smallest CW and CCW differences between the angles
        ###
        pass

#=============================================================================

a = Angle(1, 2*math.pi)
b = Angle(180, "deg")
c = Angle(math.pi, 2*math.pi)
d = Angle(10, "deg")
e = Angle(350, "deg")
f = Angle(0)
g = Angle(2*math.pi)
print(-a)
print(-b)
print(-c)
print(-d)
print(-e)
print(-f)
print(-g)
