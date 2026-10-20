import numpy as np

class KalmanFilter:
    def __init__(self, dim_x, dim_z, dim_u = 0):
        """
        The following are place holder objects and must be defined appropriately after calling the class.
        dim_x is the dimension of the state vector
        dim_z is the dimension of the measurement
        dim_u is the dimension of the driving force
        """
        self.x = np.zeros((dim_x, 1))       #State
        self.P = np.eye(dim_x)              #Error Covariance Matrix
        self.Q = np.eye(dim_x)              #Process Variance
        self.R = np.eye(dim_z)              #Measurement Variance
        self.u = np.zeros((dim_u, 1))       #Driving Force
        self.B = np.zeros((dim_x, dim_u))   #Control Transition Matrix
        self.F = np.zeros((dim_x, dim_x))   #State Transition Matrix
        self.H = np.zeros((dim_z, dim_x))   #Measurement Function
        self._I = np.eye(dim_x)             #Identity Matrix
        self.K = np.zeros((dim_x, dim_z))   #Kalman Gain
        self.dim_z = dim_z

    def predict(self):
        """
        Filter produces an a priori estimate of the next position off of the current estimate.
        """
        self.x = (self.F @ self.x) + (self.B @ self.u)
        self.P = (self.F @ self.P @ self.F.T) + self.Q

    def update(self, z):
        """
        Filter produces an a posteriori estimate by combining the a priori estimate with an observation.
        z - observation
        """
        z = np.asarray(z).reshape(self.dim_z, 1)
        self.K = self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.R)
        self.x = self.x + self.K @ (z - self.H @ self.x)
        self.P = (self._I - self.K @ self.H) @ self.P @ (self._I - self.K @ self.H).T + (self.K @ self.R @ self.K.T)