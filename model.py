#!/usr/bin/env python3.6
"""API for ASCII Graphics Library."""

class Shape():
    """A shape to be added to canvas - for now, rectangles only."""

    # TODO: error-handle if decimal height/width submitted.
    def __init__(self, start_x, end_x, start_y, end_y, fill_char='*'):
        """For now, create a rectangle with the given length and width."""

        self.start_x = int(start_x)
        self.end_x = int(end_x)
        self.start_y = int(start_y)
        self.end_y = int(end_y)
        self.fill_char = fill_char
        self.coords = (self.start_x, self.end_x, self.start_y, self.end_y)
        
        # self.height = self.end_y - self.start_y
        # self.width = self.end_x - self.start_x


    def change_fill(self, new_fill_char):
        """Change a shape's fill character"""
        
        self.fill_char = new_fill_char
    
    
    def _move_shape(self, axis, diff):
        """Update shape coordinates 
        
        Should be called ONLY via Canvas' translate_shape() method."""

        if axis == 'x':
            self.start_x += diff
            self.end_x += diff
        
        elif axis == 'y':
            self.start_y += diff
            self.end_y += diff
        
        self.coords = (self.start_x, self.end_x, self.start_y, self.end_y)

    
    def __repr__(self):
        return f"<Shape {self.coords}>"
    

class Canvas():
    """A rectangular shape on which to draw ASCII art."""

    def __init__(self, height, width):
        "Declare a canvas object with the given dimensions."

        self.height = height
        self.width = width
        self.fill_char = '.'

        # A dictionary of lists -- each with chars for one line of Canvas
        self.contents = {}

        # A dictionary of Shapes currently on this Canvas, 
        #    with Shape coordinates as keys and Shape objects as values.
        self.shapes = {}
        
        # Origin at Top Left Corner. Values increase down and to the right.
        # Origin set to (1, 1) but can be adjusted here.
        self.origin = {'x': 1, 'y': 1}

        self.clear_canvas()
    
    
    def as_string(self):

        response_str = ''

        for line in self.contents:
            response_str += (''.join(self.contents[line]))
            response_str += '\n'
        
        return response_str


    def print_canvas(self):
        """Prints the canvas and any shapes to standard output."""

        print(self.as_string())
    

    def clear_canvas(self):
        """Clears all shapes from a Canvas."""

        self.shapes = {}
        self._update_dict();
    

    def _update_dict(self):
        """Update Canvas dictionary."""
        
        for x in range(self.height):
            line = self.fill_char * self.width
            self.contents[x] = [char for char in line]
        
        for shape_object in self.shapes.values():
            self.add_shape(shape_object)


    def add_shape(self, shape):
        """Update Canvas object, storing new shape."""

        self.shapes[shape.coords] = shape

        # If shape is outside Canvas boundaries, do not change Canvas dict.
        if (
            shape.start_x > self.width or 
            shape.start_y > self.height or
            shape.end_x < self.origin['x'] or 
            shape.end_y < self.origin['y']
        ):
            return
        
        # If partly outside canvas bounds, only update within bounds.
        def _set_point(value, boundary, minmax):
            """Adjusts start- and/or end-points based on canvas bounds."""

            if (minmax == 'min' and value < boundary) or (minmax == 'max' and value > boundary):
                    return boundary
            return value
        
        x_start = _set_point(shape.start_x, self.origin['x'], 'min')
        y_start = _set_point(shape.start_y, self.origin['y'], 'min')
        x_end = _set_point(shape.end_x, self.width, 'max')
        y_end = _set_point(shape.end_y, self.height, 'max')

        # Adjust start-points if origin set to (1, 1) or other non-zero #s
        x_start -= self.origin['x']
        y_start -= self.origin['y']

        for y_value in range(y_start, y_end):
            for x_value in range(x_start, x_end):
                self.contents[y_value][x_value] = shape.fill_char
    

    def translate_shape(self, former_coords, axis, num):
        """Move a shape up, down, left, or right."""

        shape_to_move = self.shapes.pop(former_coords)
        shape_to_move._move_shape(axis, num)
        self.shapes[shape_to_move.coords] = shape_to_move
        self._update_dict()
    
    
    def __repr__(self):
        return f"<Canvas ({self.height}, {self.width})>"


# if __name__ == "__main__":
#     import unittest
#     doctest.testmod()