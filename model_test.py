import unittest
import model

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.small_canvas = model.Canvas(2, 3, '.')

        self.shape = model.Shape(3, 5, 1, 2)
        self.wide = model.Shape(1, 9, 0, 1, '+')
        self.tall = model.Shape(1, 1, 1, 20, '@')

        self.filled_canvas = model.Canvas(4, 5, '.')
        self.filled_canvas.fill_char = '.'
        self.filled_canvas.add_shape(self.shape)
        self.filled_canvas.add_shape(self.wide)
        self.filled_canvas.add_shape(self.tall)


    def test_basic_canvas_dimensions(self):
        """Check dimensions on a small canvas."""

        self.assertEqual(self.small_canvas.contents[0], ['.', '.', '.'])
        self.assertEqual(self.small_canvas.contents[1], ['.', '.', '.'])
        with self.assertRaises(KeyError):
            self.small_canvas.contents[2]
    

    def test_change_fill(self):
        """Check new fill on a small canvas."""

        self.small_canvas.fill_char = '-'
        self.small_canvas.clear_canvas()

        self.assertEqual(self.small_canvas.contents[0], ['-', '-', '-'])
        self.assertEqual(self.small_canvas.contents[1], ['-', '-', '-'])

        expected_result = (
            "---\n"
            "---\n"
        )
        self.assertEqual(self.small_canvas.as_string(), expected_result)



    def test_add_shape(self):
        """Check add_shape on a small canvas. Then, test as_string() method."""

        self.small_canvas.add_shape(self.wide)
        self.assertEqual(self.small_canvas.contents[0], ['+', '+', '+'])
        
        # Same test using as_string() to check result.
        expected_result = (
            "+++\n"
            "...\n"
        )
        self.assertEqual(self.small_canvas.as_string(), expected_result)


    def test_add_shape2(self):
        """Check that one shape layers over another on a small canvas."""
        
        self.small_canvas.add_shape(self.wide)
        self.small_canvas.add_shape(self.tall)
        expected_result = (
            "@++\n"
            "@..\n"
        )
        self.assertEqual(self.small_canvas.as_string(), expected_result)


    def test_basic_integration(self):
        """Test end-to-end from creating Canvas to adding multiple Shapes."""

        self.new_canvas = model.Canvas(4, 5, '.')
        expected_result = (
            ".....\n"
            ".....\n"
            ".....\n"
            ".....\n"
        )
        self.assertEqual(self.new_canvas.as_string(), expected_result)

        self.new_canvas.fill_char = ','
        self.new_canvas.clear_canvas()
        updated_result = (
            ",,,,,\n"
            ",,,,,\n"
            ",,,,,\n"
            ",,,,,\n"
        )
        self.assertEqual(self.new_canvas.as_string(), updated_result)

        self.new_canvas.add_shape(model.Shape(3, 5, 1, 2))
        updated_result = (
            ",,***\n"
            ",,***\n"
            ",,,,,\n"
            ",,,,,\n"
        )
        self.assertEqual(self.new_canvas.as_string(), updated_result)


        self.new_canvas.add_shape(model.Shape(-1, 20, -1, 1, '+'))
        updated_result = (
            "+++++\n"
            ",,***\n"
            ",,,,,\n"
            ",,,,,\n"
        )
        self.assertEqual(self.new_canvas.as_string(), updated_result)


        self.new_canvas.add_shape(model.Shape(0, 1, 1, 5, '@'))
        updated_result = (
            "@++++\n"
            "@,***\n"
            "@,,,,\n"
            "@,,,,\n"
        )
        self.assertEqual(self.new_canvas.as_string(), updated_result)


    def test_advanced_integration(self):
        """Test end-to-end from creating Canvas to translating Shapes."""

        self.new_canvas = model.Canvas(4, 5, ',')
        self.new_canvas.add_shape(model.Shape(3, 5, 1, 2))
        self.new_canvas.add_shape(model.Shape(-1, 20, -1, 1, '+'))
        tall_shape = model.Shape(0, 1, 1, 5, '@')
        self.new_canvas.add_shape(tall_shape)
        
        expected_result = (
            "@++++\n"
            "@,***\n"
            "@,,,,\n"
            "@,,,,\n"
        )
        self.assertEqual(self.new_canvas.as_string(), expected_result)

        # Shape translates from (y_start, y_end) of 1,5 to 0, 4.
        # This still covers height of new_canvas, so no change in output 
        self.new_canvas.translate_shape(tall_shape.coords, 'y', -1)
        self.assertEqual(self.new_canvas.as_string(), expected_result)

        # After -1 shift along y-axis, shape's new coords are (0, 1, 0, 4)
        self.new_canvas.translate_shape((0, 1, 0, 4), 'x', 1)
        updated_result = (
            "@@+++\n"
            "@@***\n"
            "@@,,,\n"
            "@@,,,\n"
        )
        self.assertEqual(self.new_canvas.as_string(), updated_result)

        # #This should bring two-line *** shape in front of +++++ shape
        self.new_canvas.add_shape(self.shape)

        expected_result = (
            "@@***\n"
            "@@***\n"
            "@@,,,\n"
            "@@,,,\n"
        )
        self.assertEqual(self.new_canvas.as_string(), expected_result)
    

    def test_translation(self):
        """If y-value of 'tall' shape starts at (-1), should be same output."""

        self.filled_canvas.translate_shape(self.tall.coords, 'y', -2)
        expected_result = (
            "@++++\n"
            "@.***\n"
            "@....\n"
            "@....\n"
        )
        self.assertEqual(self.filled_canvas.as_string(), expected_result)
    

    def test_translation2(self):
        """If start_y of 'tall' is 2, should not be same output."""

        self.filled_canvas.translate_shape(self.tall.coords, 'y', 3)
        expired_result = (
            "@++++\n"
            "@.***\n"
            "@....\n"
            "@....\n"
        )
        self.assertFalse(self.filled_canvas.as_string() == expired_result)
    

    def test_start_point1(self):
        """If 'tall' shape starts at (-1, -1), should be same output.
        
        Similar to last test, but omits translate_shape() method."""

        self.filled_canvas.clear_canvas()
        self.filled_canvas.add_shape(self.shape)
        self.filled_canvas.add_shape(self.wide)
        self.new_tall = model.Shape(-1, 1, -1, 20, '@')
        self.filled_canvas.add_shape(self.new_tall)
        expected_result = (
            "@++++\n"
            "@.***\n"
            "@....\n"
            "@....\n"
        )
        self.assertEqual(self.filled_canvas.as_string(), expected_result)


    def test_start_point2(self):
        """If 'tall' shape starts at (2, 2), should not be same output."""

        self.filled_canvas.clear_canvas()
        self.new_tall = model.Shape(2, 1, 2, 20, '@')
        self.filled_canvas.add_shape(self.shape)
        self.filled_canvas.add_shape(self.wide)
        self.filled_canvas.add_shape(self.new_tall)
        expected_result = (
            "@++++\n"
            "@.***\n"
            "@....\n"
            "@....\n"
        )
        self.assertFalse(self.filled_canvas.as_string() == expected_result)


if __name__ == '__main__':
    unittest.main()