# Python Angles

A Python class for representing and performing calculations with angles.

This is a small class meant to simplify common operations with angle measures. The convention used for the arithmetic and comparison operations is meant to capture the idea that we are primarily interested in the smallest angle between two measures, regardless of the numbers, themselves. In particular this includes the following conventions:

* Angles that differ by an integer number of revolutions are considered equivalent.
* Output angle values are limited in size to one full revolution (e.g. all radian Angle objects maintain a measure between 0 and 2π).
* Angle differences and comparisons are based on the smallest angle between the two input angles, and on whether the second angle is closer to being clockwise or counterclockwise from the first (positive differences indicate counterclockwise movement, while negative differences indicate clockwise).

Both radian and degree measure (or any arbitrary subdivision of the circle) are supported. Methods perform calculations and return results using the measure of their own angle object, converting other angles when necessary.

## Dependencies

This class requires the `math` module.

## The `Angle` Class

The following is a brief description of selected attributes, custom methods, and overloaded methods for the `Angle` class.

### Attributes

#### Static Attributes

* `rad_str (set)` -- Set of accepted `str` names for radian measure.
* `deg_str (set)` -- Set of accepted `str` names for degree measure.
* `grad_str (set)` -- Set of accepted `str` names for gradian measure.

#### Class Attributes

* `measure (float)` -- Current measure of the angle.
* `mod (float)` -- Measure of a complete revolution (e.g. 2π for radian measure, 360 for degree measure).
* `unit (str)` -- Name of the  unit of measure.

### Methods

* `__init__([measure[, mod]])` -- `Angle` class constructor. Accepts the following keyword arguments:
  * `measure (float) [0.0]` -- Initial angle measure.
  * `mod (int, float, or str) ["radians"]` -- Specifies measure unit. A numerical argument is treated as the measure of a full revolution, while a string argument is taken as the name of a standard unit (radians, degrees, or gradians).
* `convert(mod)` -- Returns the angle's measure converted to a different unit.

### Operators

In all of the following descriptions, `a` represents the `Angle` object in question.

* `a + b` -- Returns an `Angle` object whose unit matches that of `a` and whose measure is the sum of the measures of `a` and `b`. If `b` is a number, then this is treated as a measure (with the same unit as `a`). If `b` is another `Angle` object, then its measure is first converted to the unit of `a` before being added.
