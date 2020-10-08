# Python Angles

A Python class for representing and performing calculations with angles.

This is a small class meant to simplify common operations with angle measures. The convention used for the arithmetic and comparison operations is meant to capture the idea that we are primarily interested in the smallest angle between two measures, regardless of the numbers, themselves. In particular this includes the following conventions:

* Angles that differ by an integer number of revolutions are considered equivalent.
* Angle differences 

Both radian and degree measure (or any arbitrary subdivision of the circle) are supported. Methods perform calculations and return results using the measure of their own angle object, converting other angles when necessary.

## Dependencies

This class requires the `math` module.

## The `Angle` Class

The following is a brief description of selected attributes, custom methods, and overloaded methods for the `Angle` class.

### Attributes

* `measure (float)` -- Current measure of the angle.
* `mod (float)` -- Measure of a complete revolution (e.g. 2pi for radian measure, 360 for degree measure).
* `unit (str)` -- Name of the  unit of measure.

### Custom Methods

*

### Overloaded Methods

*
