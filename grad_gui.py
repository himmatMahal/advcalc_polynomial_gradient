import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

class PolynomialGradientGUI:

    ALLOWED_CHARS = [
        ' ', 'x', 'y', '*', '+', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', '0', '-',
    ]

    def __init__(self, main_window):
        self.main_window = main_window
        self.WIDTH = 600
        self.HEIGHT = 250

        self.main_window.title('Gradient Visualizer')

        self.main_canvas = tk.Canvas(
            main_window,
            height=self.HEIGHT,
            width=self.WIDTH,
            bg='#ccc5b9'
        )
        self.main_canvas.pack()

        self.main_label = tk.Label(
            self.main_canvas,
            text=f'Only {self.ALLOWED_CHARS} are allowed'
        )
        self.main_label.place(
            width=400,
            height=30,
            anchor='center',
            relx=0.5,rely=0.05
        )

        self.function_label = tk.Label(
            self.main_canvas,
            text="Enter 3D Polynomials of x and y:    f(x,y)="
        )
        self.function_label.place(
            width=250,
            height=75,
            relx=0.1,rely=0.2
        )

        self.function_entry = tk.Entry(self.main_canvas,bd=5)
        self.function_entry.place(
            width=250,
            height=75,
            relx=0.5,rely=0.2
        )

        self.submit_button = tk.Button(
            self.main_canvas,
            text='Create Gradient Plot',
            command=self.submit_command
        )
        self.submit_button.place(
            width=250,
            height=75,
            relx=0.1,rely=0.65
        )

        self.submitMsg = tk.StringVar()
        self.submit_output = tk.Label(
            self.main_canvas,
            textvariable=self.submitMsg,
            wraplength=240,
            justify=tk.LEFT
        )
        self.submit_output.place(
            width=250,
            height=75,
            relx=0.5,rely=0.65
        )



    def submit_command(self):
        try:
            x, y = sp.symbols('x y')
            f = self.parse_polynomial(x, y)

            grad = (sp.diff(f, x), sp.diff(f, y))

            # WARNING: use lambdify sparingly, only with trusted (actual math)
            # functions, here, i only accept polynomials with numbers,
            # addition, subtraction, exponentiation, using x and y, so it is
            # safe
            gradFn = { 'x': sp.lambdify([x,y], grad[0], 'sympy'),
                       'y': sp.lambdify([x,y], grad[1], 'sympy') }
            # More info for numeric computation:
            # https://docs.sympy.org/latest/modules/numeric-computation.html

            # TODO: make plot look cooler

            count = 40
            xyRange = (-5,5)
            # useful for count x count coordinates
            coords = np.linspace(xyRange[0] , xyRange[1], num=count)

            X, Y = np.meshgrid(coords, coords)
            U = gradFn['x'](X,Y)
            V = gradFn['y'](X,Y)

            M = np.hypot(U, V) # length of arrow corresponds with color

            plt.quiver( X, Y, U, V, M, scale=100 )
            plt.ylabel("y")
            plt.xlabel("x")
            plt.title( "Gradient Vector Field of: f(x, y) = " + str(f) )
            plt.show()
            self.submitMsg.set("Success")
        except Exception as e:
            err = repr(e)
            self.submitMsg.set(err)


    def parse_polynomial(self, x, y):
        raw_text = self.function_entry.get()
        for char in list(raw_text):
            if not char in self.ALLOWED_CHARS:
                raise RuntimeError(
                    f'Invalid Equation, only {self.ALLOWED_CHARS} are allowed'
                )
        expr = None
        try:
            expr = sp.parsing.sympy_parser.parse_expr(
                raw_text, evaluate=False,
            )
        except:
            raise RuntimeError('Could Not Parse Equation')

        return sp.sympify(expr, locals={'x':x, 'y':y})

def main():
    root = tk.Tk()
    gradGui = PolynomialGradientGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
