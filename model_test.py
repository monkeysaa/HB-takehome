import unittest
import model

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.small_canvas = model.Canvas(2, 3)
        self.small_canvas.fill_char = '.'

        self.shape = model.Shape(3, 5, 1, 2)
        self.wide = model.Shape(1, 9, 0, 1, '+')
        self.tall = model.Shape(1, 1, 1, 20, '@')

        self.filled_canvas = model.Canvas(4, 5)
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

        expected_result = (
            "@++++\n"
            "@.***\n"
            "@....\n"
            "@....\n"
        )
        self.assertEqual(self.filled_canvas.as_string(), expected_result)

        #This should bring two-line *** shape in front of +++++ shape
        self.filled_canvas.add_shape(self.shape)

        expected_result = (
            "@+***\n"
            "@.***\n"
            "@....\n"
            "@....\n"
        )
        self.assertEqual(self.filled_canvas.as_string(), expected_result)
    

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