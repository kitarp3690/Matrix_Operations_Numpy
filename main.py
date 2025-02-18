import numpy as np

class Matrix:
    def __init__(self):
        """This function initializes 3 matrices"""
        self.matrixA = None
        self.matrixB = None
        self.matrixC= None
        self.ans= None
        self.data = {1:self.matrixA, 2:self.matrixB, 3:self.matrixC}

    def display_matlist(self)->int:
        """This function displays the matrix list and return given matrix number"""
        print('''
        Matrix
        [1]. Matrix A
        [2]. Matrix B
        [3]. Matrix C
        [4]. Back
        :: ''')

    def show_matrix_data(self):
        while True:
            try:
                user_ip = int(input('''
                Show Matrix
                [1]. Matrix A
                [2]. Matrix B
                [3]. Matrix C
                [4]. Back
                :: '''))
                match user_ip:
                    case 1:
                        print(f"Matrix A = \n{self.matrixA}")
                    case 2:
                        print(f"Matrix B = \n{self.matrixB}")
                    case 3:
                        print(f"Matrix C = \n{self.matrixC}")
                    case 4:
                        return
                    case _:
                        print("Please enter valid input")
                    
            except ValueError:
                print('Please enter valid input')

    def take_input(self):
        while True:
            try:
                user_ip = int(input(f'''
                Input for 
                [1]. Matrix A
                [2]. Matrix B
                [3]. Matrix C
                [4]. Back\n
                '''))
                match user_ip:
                    case 1:
                        self.matrixA = self.input_matrix('A')
                    case 2:
                        self.matrixB = self.input_matrix('B')
                    case 3:
                        self.matrixC = self.input_matrix('C')
                    case 4:
                        return
                    case _:
                        print("Invalid selection! Please choose a valid option.")
            except ValueError:
                print("Please Enter valid input")

    def input_matrix(self, matrix_name:str):
        """ function to take input for matrices """
        while True:
            try:
                size = tuple(map(int, input(f"Enter matrix {matrix_name} size in n,m format: ").split(',')))
                # Validate size format (two positive integers)
                if len(size) != 2 or size[0] <= 0 or size[1] <= 0:
                    print("❌ Error: Please enter two positive integers separated by a comma (e.g., 2,3).")
                    continue 
                matrix = np.zeros(size, dtype=int)

                for i in range(size[0]):
                    for j in range(size[1]):
                        matrix[i, j] = int(input(f"Enter value for {matrix_name}[{i},{j}]: "))

                print(f"Matrix {matrix_name} stored successfully!\n")
                return matrix

            except ValueError:
                print("Invalid input! Please enter valid input.")
                return None

    def add_matrix(self):
        """Function that adds matrices"""
        while True:
            try:
                print("Enter matrix numbers that you want to add ")
                self.display_matlist()
                user_ip = tuple(map(int,input("Plese enter giving comma (e.g. 2,3): ").split(',')))
                for i in user_ip:
                    self.ans += self.data.get(i) 

            except ValueError:
                print('Invalid input! Please enter valid input.')

    def operations(self):
        while True:
            print(f'''
            What operation do you want to perform?
            [1]. Input
            [2]. Data
            [3]. Add
            [4]. Subtract
            [5]. Determinant
            [6]. Transpose
            [7]. Inversion
            [8]. Eigenvalues and Eigenvectors
            [9]. Exit
            ''')
            user_ip = int(input('::'))
            match user_ip:
                case 1:
                    self.take_input()
                case 2:
                    self.show_matrix_data()
                case 3:
                    self.add_matrix()
                case 9:
                    break

if __name__=='__main__':
    mat1 = Matrix()
    mat1.operations()