import math

class Angle:
    """A Python class for representing and performing calculations with angles.
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
            self.mod = float(mod)
            self.unit = "/ " + str(self.mod)

        # Rename unit for recognized moduli
        if mod == 2*math.pi:
            self.unit = "rad"
        elif mod == 360.0:
            self.unit = "deg"
        elif mod == 400.0:
            self.unit = "grad"

        # Bound measure
        self.measure = self.measure % self.mod

    #-------------------------------------------------------------------------

    def __str__(self):
        """Angle.__str__() -> str
        Angle string conversion.

        Returns the measure of the angle as a string, along with an
        abbreviation of the angle unit.
        """

        return str(self.measure) + " " + self.unit

    #-------------------------------------------------------------------------

    def convert(self, new_mod):
        """Angle.convert(mod) -> float
        Converts the angle measure to a different unit.

        Positional arguments:
        mod (str or float) ["radians"] -- angle unit, or measure of one full
            revolution
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
            new_mod = float(new_mod)

        # Convert measure as a fraction of a complete revolution
        return (self.measure/self.mod)*new_mod

    #-------------------------------------------------------------------------

    def __abs__(self):
        """Angle.__abs__() -> float
        Returns the absolute value of the angle's measure's modulus.

        The output of this method is always between 0.0 and the full
        revolution measure.
        """

        return self.measure % self.mod

    #-------------------------------------------------------------------------

    def __add__(self, b):
        """Angle.__add__(b) -> Angle
        Angle addition operator.

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

        # If given an Angle object, convert its measure to the current unit
        if type(b) == Angle:
            b = b.convert(self.mod)

        # Sum the measures, restricted to one revolution
        m = (self.measure + b) % self.mod

        # Return an Angle object
        return Angle(measure=m, mod=self.mod)

    #-------------------------------------------------------------------------

    def __sub__(self, b):
        """Angle.__sub__(b) -> Angle
        Angle subtraction operator.

        Returns an Angle object whose measure represents the difference
        between two angle measures. The unit of the returned object matches
        that of the current object.

        The returned measure is the smallest acute angle between the current
        object's measure and the given measure (after conversion), positive if
        this acute angle positions the current angle counterclockwise relative
        to the other and negative otherwise.

        Positional arguments:
        b (Angle, int, or float) -- angle to subtract from the current measure

        Subtracting a number from the current Angle treats the number as a
        measure of the same unit as the current object.

        Subtracting an Angle from the current Angle results in the other
        measure being converted to the current object's unit, after which the
        two are subtracted,
        """

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
print(a - b)
print(b - a)
print(c - a)
