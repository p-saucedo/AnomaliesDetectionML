from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

class DistributionGenerator:
    def __init__(self, y, tolerance):
        self.y_values = np.array(y)
        self.x_values = np.linspace(0, 24, num=len(self.y_values), endpoint=True)
        self.f = interp1d(self.x_values, self.y_values, kind='cubic')

        self.y_min_values = self.y_values - tolerance
        self.f_min = interp1d(self.x_values, self.y_min_values, kind='cubic')

        self.y_max_values = self.y_values + tolerance
        self.f_max = interp1d(self.x_values, self.y_max_values, kind='cubic')

    def plot(self):
        xnew = np.linspace(0, 24, num=100, endpoint=True)
        plt.plot(self.x_values, self.y_values, 'ro')
        plt.plot(xnew, self.f(xnew), 'r-', label = 'data')

        plt.plot(self.x_values, self.y_min_values, 'b.')
        plt.plot(xnew, self.f_min(xnew), 'b-', label ='min_limit')

        plt.plot(self.x_values, self.y_max_values, 'y.')
        plt.plot(xnew, self.f_max(xnew), 'y-', label = 'max_limit')

        plt.legend(loc='best')
        plt.xlim([0,24])
        plt.title('Distribution of values')
        plt.xlabel('Hours in the day')
        plt.ylabel('Value accepted')
        plt.show()

    def evaluate_on_centered(self,x):
        return np.round(self.f(x),2)

    def evaluate_on_min(self, x):
        return np.round(self.f_min(x),2)

    def evaluate_on_max(self,x):
        return np.round(self.f_max(x),2)

    def evaluate(self,x):
        return (self.evaluate_on_centered(x), self.evaluate_on_min(x), self.evaluate_on_max(x))

    def check_valid(self, x, y):
        e, e_min, e_max = self.evaluate(x)
        valid = True if (y >= e_min and y <= e_max) else False
        return valid