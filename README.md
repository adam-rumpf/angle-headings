# Python Angles

A Python class for representing and performing calculations with angles.

This is a small class meant to simplify common operations with angle measures. The convention used for the arithmetic and comparison operations is meant to capture the idea that we are primarily interested in the smallest angle between two measures, regardless of the numbers, themselves. In particular this includes the following conventions:

* Angles that differ by an integer number of revolutions are considered equivalent.
* Output angle values are limited in size to _±1/2_ full revolution. For example, radian angle measures are restricted to the interval _(-π,π]_, while degree angle measures are restricted to _(-180,180]_.
* Angle comparisons are based on the smallest angle between the two input angles, and on whether the first angle is closer to being clockwise or counterclockwise from the first. By convention we say that _A > B_ if the smallest angle between _A_ and _B_ places _A_ counterclockwise relative to _B_, and _A < B_ if the smallest angle between _A_ and _B_ places _A_ clockwise relative to _B_.

Radian, degree, and gradian measure (or any arbitrary subdivision of the circle) are all supported. Methods perform calculations and return results using the measure of their own angle object, converting other angles or floats when necessary.

## Dependencies

This class requires the `math` module.

## The `Angle` Class

The following is a brief description of selected attributes, custom methods, and overloaded methods for the `Angle` class.

### Attributes

#### Static Attributes

* `rad_str (set)` -- Set of accepted `str` names for radian measure.
* `deg_str (set)` -- Set of accepted `str` names for degree measure.
* `grad_str (set)` -- Set of accepted `str` names for gradian measure.

#### Public Attributes

* `measure (float)` -- Current measure of the angle, always normalized to _±1/2_ full revolutions.
* `mod (float)` -- Measure of a complete revolution (e.g. _2π_ for radian measure, _360_ for degree measure).
* `unit (str)` -- Name of the  unit of measure.

### Methods

* `__init__([measure[, mod]])` -- `Angle` class constructor. Accepts the following keyword arguments:
  * `measure (float) [0.0]` -- Initial angle measure.
  * `mod (int, float, or str) ["radians"]` -- Specifies measure unit. A numerical argument is treated as the measure of a full revolution, while a string argument is taken as the name of a standard unit (radians, degrees, or gradians).
* `convert(mod)` -- Returns the angle's measure converted to a different unit.
* `reldiff(other)` -- Returnes a relative difference between this and another angles' measures, normalized so that 0 represents equality and 1 represents diametrically opposed angles. This is meant to be used as an alternative to direct equality comparisons due to the `float` measures.

### `float`-Valued Operators

* `abs(A)` -- Returns the absolute value of an angle's measure.
* `int(A)` -- Returns an angle's measure, cast as an integer.
* `float(A)` -- Returns an angle's measure, cast as a float.
* `round(A)` -- Returns an angle's measure, rounded to the nearest integer.

### `Angle`-Valued Operators

#### Unary Operators

* `+A` -- Returns an exact copy of the `Angle` object.
* `-A` -- Returns a copy of the `Angle` object with its measure negated.

#### Overloaded Binary Operators

Each of the following operators accepts either another `Angle` object or a `float` as its second argument. If given another `Angle`, the second `Angle` is converted to the first `Angle`'s unit before the operation is performed. If given a `float`, the number is used directly.
* `A + B` -- Returns an `Angle` object with the sum of two angles' measures.
* `A - B` -- Returns an `Angle` object with the difference between two angles' measures.

#### Scalar Operators

* `A * b` -- Returns an `Angle` object with its measure multiplied by a scalar.
* `A / b` -- Returns an `Angle` object with its measure divided by a scalar.
* `A // b` -- Returns an `Angle` objecct with its measure floor divided by a scalar.
* `A ** b` -- Returns an `Angle` object with its measure raised to a scalar power.

### Overloaded Boolean Operators

Each of the following operators accepts either another `Angle` object or a `float` as its second argument. If given another `Angle`, the second `Angle` is converted to the first `Angle`'s unit before the operation is performed. If given a `float`, the number is used directly.

#### Equality Comparisons

Due to the fact that each angle's measure is stored as a `float`, it is not recommended to directly test measure equality, and to instead make use of the `Angle.reldiff()` method.
* `A == B` -- Tests for equality of two measures (after unit conversion and normalization).
* `A != B` -- Tests for inequality of two measures.

#### Order Comparisons

The following comparisons are based on the smallest angle between two given measures.
* `A > B` -- Returns `True` if and only if the smallest angle between `A` and `B` places `A` counterclocwise relative to `B`.
* `A >= B` -- Returns `True` if and only if `A > B` or `A == B`.
* `A < B` -- Returns `True` if and only if the smallest angle between `A` and `B` places `A` clocwise relative to `B`.
* `A <= B` -- Returns `True` if and only if `A < B` or `A == B`.
