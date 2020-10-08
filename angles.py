import math

class Angle:
    """A Python class for representing and performing calculations with angles.
    """

    #-------------------------------------------------------------------------

    def __init__(self, measure=0.0, mod="radians"):
        """Angle.__init__([mod]) -> Angle
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
            if mod in {"radians", "radian", "rad", "r"}:
                self.mod = 2*math.pi
                self.unit = "rad"
            elif mod in {"degrees", "degree", "deg", "d"}:
                self.mod = 360.0
                self.unit = "deg"
            elif mod in {"gradians", "gradian", "grad", "g"}:
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

    #-------------------------------------------------------------------------

    def __str__(self):
        """Angle.__str__() -> str
        Angle string conversion.

        Returns the measure of the angle as a string, along with an
        abbreviation of the angle unit.
        """

        return str(self.measure) + " " + self.unit

#=============================================================================

temp = Angle(10, 2*math.pi)
print(temp)
