import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
import re

class Matrix:
    def __init__(self, root):
        """This function initializes 3 matrices"""
        self.root = root
        self.matrixA = None
        self.matrixB = None
        self.matrixC = None
        self.ans = None
        self.data = {1: self.matrixA, 2: self.matrixB, 3: self.matrixC}

        # adding background color in root
        self.root.configure(bg="lightgray")

        # GUI elements    
        self.matrix_label = tk.Label(root, text="Matrix Operations", font=("Arial", 16))
        self.matrix_label.pack(pady=10)

        # Matrix buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.button_matrixA = tk.Button(self.button_frame, text="Matrix A", width=15, height=1 , command=lambda: self.take_input('A'))
        self.button_matrixA.grid(row=0, column=0, padx=5, pady=9)
        self.add_hover_effect(self.button_matrixA)

        self.button_matrixB = tk.Button(self.button_frame, text="Matrix B", width=15, height=1 , command=lambda: self.take_input('B'))
        self.button_matrixB.grid(row=0, column=1, padx=5, pady=5)
        self.add_hover_effect(self.button_matrixB)

        self.button_matrixC = tk.Button(self.button_frame, text="Matrix C", width=15, height=1 , command=lambda: self.take_input('C'))
        self.button_matrixC.grid(row=0, column=2, padx=5, pady=5)
        self.add_hover_effect(self.button_matrixC)
        
        # frame for add, subtract and other functionalities
        self.functionalities_frame = tk.Frame(root)
        self.functionalities_frame.pack(side="top", anchor="center", pady=20) 

        self.button_show = tk.Button(self.functionalities_frame, text="Show Matrix Data", width=20, height=2 , command=self.show_matrix_data)
        self.button_show.grid(row=0, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_show)

        self.button_add = tk.Button(self.functionalities_frame, text="Add Matrices", width=20, height=2 , command=self.add_matrix)
        self.button_add.grid(row=1, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_add)

        self.button_subtract = tk.Button(self.functionalities_frame, text="Subtract Matrices", width=20, height=2 , command=self.subtract_matrix)
        self.button_subtract.grid(row=2, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_subtract)
        
        self.button_multiply = tk.Button(self.functionalities_frame, text="Multiply Matrices", width=20, height=2 , command=self.multiply_matrix)
        self.button_multiply.grid(row=3, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_multiply)

        self.button_inverse = tk.Button(self.functionalities_frame, text="Inverse Matrix", width=20, height=2 , command=self.inverse_matrix)
        self.button_inverse.grid(row=4, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_inverse)

        self.button_transpose = tk.Button(self.functionalities_frame, text="Transpose Matrix", width=20, height=2 , command=self.transpose_matrix)
        self.button_transpose.grid(row=5, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_transpose)

        self.button_determinant = tk.Button(self.functionalities_frame, text="Determinant of Matrix", width=20, height=2 , command=self.determinant_matrix)
        self.button_determinant.grid(row=6, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_determinant)

        self.button_eigen = tk.Button(self.functionalities_frame, text="Eigen of Matrix", width=20, height=2 , command=self.eigen_matrix)
        self.button_eigen.grid(row=7, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_eigen)

        self.result_label = tk.Label(root, text="Recent: ", font=("Arial", 12))
        self.result_label.pack(pady=10)
    
    def add_hover_effect(self, button):
        """Adds hover effect to a button"""
        def on_enter(event):
            button.config(bg="lightblue")  # Change color on hover
        def on_leave(event):
            button.config(bg="SystemButtonFace")  # Reset color when hover ends

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def take_input(self, matrix_name):
        """Function to create a grid of Entry widgets for matrix input"""
        size_str = simpledialog.askstring("Matrix Size", f"Enter {matrix_name}'s size in n,m format:")
        try:
            if size_str:
                size = tuple(map(int, size_str.split(',')))
                if len(size) != 2 or size[0] <= 0 or size[1] <= 0:
                    messagebox.showerror("Invalid Input", "Please enter two positive integers separated by a comma (e.g., 2,3).")
                    return

                # Creating the matrix grid window
                self.grid_window = tk.Toplevel(self.root)
                self.grid_window.title(f"Enter Values for Matrix {matrix_name}")
                self.grid_window.geometry("400x400")
                
                self.entries = []  # To store the Entry widgets
                self.size = size

                # Creating the grid of Entry widgets
                for i in range(size[0]):
                    row_entries = []
                    for j in range(size[1]):
                        entry = tk.Entry(self.grid_window, width=5)
                        entry.grid(row=i, column=j, padx=5, pady=5)
                        row_entries.append(entry)
                        # Set focus to the first Entry widget at [0,0]
                        if i == 0 and j == 0:
                            entry.focus_set() # setting the focus to [0,0]
                    self.entries.append(row_entries)

                # Adding a button to save the input and close the grid window
                save_button = tk.Button(self.grid_window, text="Save Matrix", command=lambda: self.save_matrix(matrix_name))
                save_button.grid(row=size[0], column=0, columnspan=size[1], pady=10)

                # Bind the Enter key to the save_matrix function
                save_button.bind('<Return>', lambda event: self.save_matrix(matrix_name, event))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_matrix(self, matrix_name, event=None):
        """Function to save the values from the Entry widgets into the matrix"""
        try:
            matrix = np.zeros(self.size, dtype=int)
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    value = self.entries[i][j].get()
                    if re.match(r"^-?\d+$", value):  # Checking if the value is an integer using regular expression
                        matrix[i, j] = int(value)
                    else:
                        messagebox.showerror("Invalid Input", f"Please enter a valid integer for position [{i},{j}]")
                        return

            if matrix_name == 'A':
                self.matrixA = matrix
            elif matrix_name == 'B':
                self.matrixB = matrix
            elif matrix_name == 'C':
                self.matrixC = matrix

            messagebox.showinfo("Success", f"Matrix {matrix_name} stored successfully!")
            self.grid_window.destroy()  

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_matrix_data(self):
        """ Displays the matrix data in a properly formatted dialog box """

        def format_matrix(matrix):
            """Formats a matrix for display with proper alignment"""
            if matrix is None:
                return "Not Initialized"
            return "\n".join("  ".join(f"{x:>10,}" for x in row) for row in matrix)

        formatted_A = format_matrix(self.matrixA)
        formatted_B = format_matrix(self.matrixB)
        formatted_C = format_matrix(self.matrixC)

        data_str = f"Matrix A:\n{formatted_A}\n\nMatrix B:\n{formatted_B}\n\nMatrix C:\n{formatted_C}"

        self.silent_popup("Matrix Data", data_str)

    def add_matrix(self):
        """frontend portion of adding matrix """
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title(f"Add Matrices")
        self.new_window.geometry("400x400")

        # Storing equation text
        self.equation_text = tk.StringVar()
        self.equation_text.set("")  # Initially empty
        
        # eqn stores the eqn value 
        eqn = []

        # to display how to use message
        htu = tk.Label(self.new_window,text='Press Button ', font=(16))
        htu.pack()

        # Buttons for Matrixs
        button_frame = tk.Frame(self.new_window)
        button_frame.pack()

        # Function to update equation
        def update_equation(matrix_name: str):
            current_text: str = self.equation_text.get()
            # print(f'current_text ={current_text}')

            # for delete button
            if matrix_name == "D":    
                if current_text:
                    if len(current_text) < 2:
                        self.equation_text.set(current_text[:-1])  # Removing last character (mat)
                    else:
                        self.equation_text.set(current_text[:-4])  # Removing last 3 character ( _,+,mat,_ )
                    eqn.pop()
                return  
            else:    
                eqn.append(matrix_name)
                if current_text:  
                    current_text += " + "  # Ensuring proper formatting
                
                self.equation_text.set(current_text + matrix_name)


        button_matrixA = tk.Button(button_frame, text="Matrix A", command=lambda: update_equation("A"))
        self.add_hover_effect(button_matrixA)
        button_matrixA.grid(row=0, column=0, padx=5, pady=5)

        button_matrixB = tk.Button(button_frame, text="Matrix B", command=lambda: update_equation("B"))
        self.add_hover_effect(button_matrixB)
        button_matrixB.grid(row=0, column=1, padx=5, pady=5)

        button_matrixC = tk.Button(button_frame, text="Matrix C", command=lambda: update_equation("C"))
        self.add_hover_effect(button_matrixC)
        button_matrixC.grid(row=0, column=2, padx=5, pady=5)

        # Equation label
        equation_label = tk.Label(self.new_window, textvariable=self.equation_text, font=("Arial", 12))
        equation_label.pack(pady=10)

        delete_button = tk.Button(self.new_window, text="DEL", width=5, height=1, command= lambda: update_equation("D"))
        self.add_hover_effect(delete_button)
        delete_button.pack()

        equalsto_button = tk.Button(self.new_window, text="=", width=5, height=1, command= lambda: self.add_matrix_backend(eqn))
        equalsto_button.pack()
        self.add_hover_effect(equalsto_button)

    def add_matrix_backend(self, eqn):
        """ Performs the matrix addition (Backend portion)"""
        try:
            if eqn == []:
                ans = '0'
                result_str = f"Addition Result: {ans}"
                self.result_label.config(text="Result: " + ans)
                self.silent_popup('Addition Result',result_str)
            else:
                mat_dict={'A': self.matrixA, 'B': self.matrixB, 'C' : self.matrixC}

                # checking if any matrix of eqn is of None type (i.e. value is not added in that matrix)
                if any(mat_dict.get(mat) is None for mat in eqn):
                    messagebox.showerror("Error","One or more selected matrices are not initialized! ")
                    self.new_window.destroy()
                    return

                # Ensuring all matrices have the same shape
                shape = mat_dict.get(eqn[0]).shape
                if not all(mat_dict.get(i).shape == shape for i in eqn):
                    messagebox.showerror("Error", "Matrices must have the same dimensions for addition!")
                    return

                # Performing addition
                matrices = [mat_dict.get(i) for i in eqn]
                self.ans = np.sum(matrices, axis=0)
                result_str = f"Addition Result:\n{self.ans}"
                self.result_label.config(text="Result: " + result_str)
                self.silent_popup('Addition Result',result_str)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        self.new_window.destroy()

    def subtract_matrix(self):
        """Frontend portion of subtracting matrices"""
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title(f"Subtract Matrices")
        self.new_window.geometry("400x400")

        # Storing equation text
        self.equation_text = tk.StringVar()
        self.equation_text.set("")  # Initially empty
        
        # eqn stores the eqn value 
        eqn = []

        # to display how to use(htu) message
        htu = tk.Label(self.new_window,text='Press Button ', font=(16))
        htu.pack()

        # Buttons for Matrixs
        button_frame = tk.Frame(self.new_window)
        button_frame.pack()

        # Function to update equation
        def update_equation(matrix_name: str):
            current_text: str = self.equation_text.get()

            # for delete button
            if matrix_name == "D":    
                if current_text:
                    if len(current_text) < 2:
                        self.equation_text.set(current_text[:-1])  # Removing last character (mat)
                    else:
                        self.equation_text.set(current_text[:-4])  # Removing last 3 character ( _,-,mat,_ )
                    eqn.pop()
                return 
            else:    
                eqn.append(matrix_name)
                if current_text:  
                    current_text += " - "  # Ensuring proper formatting
                
                self.equation_text.set(current_text + matrix_name)


        button_matrixA = tk.Button(button_frame, text="Matrix A", command=lambda: update_equation("A"))
        self.add_hover_effect(button_matrixA)
        button_matrixA.grid(row=0, column=0, padx=5, pady=5)

        button_matrixB = tk.Button(button_frame, text="Matrix B", command=lambda: update_equation("B"))
        self.add_hover_effect(button_matrixB)
        button_matrixB.grid(row=0, column=1, padx=5, pady=5)

        button_matrixC = tk.Button(button_frame, text="Matrix C", command=lambda: update_equation("C"))
        self.add_hover_effect(button_matrixC)
        button_matrixC.grid(row=0, column=2, padx=5, pady=5)

        # Equation label
        equation_label = tk.Label(self.new_window, textvariable=self.equation_text, font=("Arial", 12))
        equation_label.pack(pady=10)

        delete_button = tk.Button(self.new_window, text="DEL", width=5, height=1, command= lambda: update_equation("D"))
        self.add_hover_effect(delete_button)
        delete_button.pack()

        equalsto_button = tk.Button(self.new_window, text="=", width=5, height=1, command= lambda: self.subtract_matrix_backend(eqn))
        equalsto_button.pack()
        self.add_hover_effect(equalsto_button)
    
    def subtract_matrix_backend(self, eqn):
        """ Performs the matrix subtraction (Backend portion) """
        try:
            if eqn == []:
                ans = '0'
                result_str = f"Subtraction Result: {ans}"
                self.result_label.config(text="Result: " + ans)
                self.silent_popup('Subtraction Result',result_str)
            else:
                mat_dict={'A': self.matrixA, 'B': self.matrixB, 'C' : self.matrixC}

                # checking if any matrix of eqn is of None type (i.e. value is not added in that matrix)
                if any(mat_dict.get(mat) is None for mat in eqn):
                    self.silent_popup('Error',f'One or more selected matrices are not initialized!')
                    self.new_window.destroy()
                    return

                # Ensuring all matrices have the same shape
                shape = mat_dict.get(eqn[0]).shape
                if not all(mat_dict.get(i).shape == shape for i in eqn):
                    messagebox.showerror("Error", "Matrices must have the same dimensions for subtraction!")
                    self.new_window.destroy()
                    return

                # Performing subtraction
                matrices = [mat_dict.get(i) for i in eqn]
                self.ans = matrices[0]- (np.sum(matrices[1:], axis=0))
                result_str = f"Subtraction Result:\n{self.ans}"
                self.result_label.config(text="Result: " + result_str)
                self.silent_popup('Subtraction Result',result_str)

        except Exception as e:
            error_msg = f'An error occured: {e}'
            self.silent_popup('Error',error_msg)
        self.new_window.destroy()
    
    def multiply_matrix(self):
        """Frontend portion of multiplying matrix"""
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title(f"Multiply Matrices")
        self.new_window.geometry("400x400")

        # Storing equation text
        self.equation_text = tk.StringVar()
        self.equation_text.set("")  # Initially empty
        
        # eqn stores the eqn value 
        eqn = []

        # to display how to use(htu) message
        htu = tk.Label(self.new_window,text='Press Button ', font=(16))
        htu.pack()

        # Buttons for Matrixs
        button_frame = tk.Frame(self.new_window)
        button_frame.pack()

        # Function to update equation
        def update_equation(matrix_name: str):
            current_text: str = self.equation_text.get()

            # for delete button
            if matrix_name == "D":    
                if current_text:
                    if len(current_text) < 2:
                        self.equation_text.set(current_text[:-1])  # Removing last character (mat)
                    else:
                        self.equation_text.set(current_text[:-4])  # Removing last 3 character ( _,-,mat,_ )
                    eqn.pop()
                return
            else:    
                eqn.append(matrix_name)
                if current_text:  
                    current_text += " x "  # Ensuring proper formatting
                
                self.equation_text.set(current_text + matrix_name)


        button_matrixA = tk.Button(button_frame, text="Matrix A", command=lambda: update_equation("A"))
        self.add_hover_effect(button_matrixA)
        button_matrixA.grid(row=0, column=0, padx=5, pady=5)

        button_matrixB = tk.Button(button_frame, text="Matrix B", command=lambda: update_equation("B"))
        self.add_hover_effect(button_matrixB)
        button_matrixB.grid(row=0, column=1, padx=5, pady=5)

        button_matrixC = tk.Button(button_frame, text="Matrix C", command=lambda: update_equation("C"))
        self.add_hover_effect(button_matrixC)
        button_matrixC.grid(row=0, column=2, padx=5, pady=5)

        # Equation label
        equation_label = tk.Label(self.new_window, textvariable=self.equation_text, font=("Arial", 12))
        equation_label.pack(pady=10)

        delete_button = tk.Button(self.new_window, text="DEL", width=5, height=1, command= lambda: update_equation("D"))
        self.add_hover_effect(delete_button)
        delete_button.pack()

        equalsto_button = tk.Button(self.new_window, text="=", width=5, height=1, command= lambda: self.multiply_matrix_backend(eqn))
        equalsto_button.pack()
        self.add_hover_effect(equalsto_button)
    
    def multiply_matrix_backend(self, eqn):
        """ Performs the matrix multiplication (Backend portion)"""
        try:
            if eqn == []:
                ans = '0'
                result_str = f"Multiplication Result: {ans}"
                self.result_label.config(text="Result: " + ans)
                self.silent_popup('Multiplication Result',result_str)
            else:
                mat_dict={'A': self.matrixA, 'B': self.matrixB, 'C' : self.matrixC}

                # checking if any matrix of eqn is of None type (i.e. value is not added in that matrix)
                if any(mat_dict.get(mat) is None for mat in eqn):
                    self.silent_popup('Error',f'One or more selected matrices are not initialized!')
                    self.new_window.destroy()
                    return

                # Ensuring matrices can be multiplied
                shape_A = mat_dict.get(eqn[0]).shape  # Shape of first matrix
                for i in range(1, len(eqn)):
                    shape_B = mat_dict.get(eqn[i]).shape  # Shape of next matrix in the equation
                    if shape_A[1] != shape_B[0]:  # Checking if columns of A match rows of B
                        messagebox.showerror("Error", "Matrix multiplication is not possible! Ensure A.columns == B.rows.")
                        self.new_window.destroy()
                        return
                    shape_A = (shape_A[0], shape_B[1])  # Updating shape for next multiplication

                # Performing multiplication
                matrices = [mat_dict.get(i) for i in eqn]
                result = matrices[0]
                for i in range(1, len(matrices)):
                    result  = np.dot(result, matrices[i])
                self.ans = result
                result_str = f"Multiplication Result:\n{self.ans}"
                self.result_label.config(text="Recent: " + result_str)
                self.silent_popup('Multiplication Result',result_str)

        except Exception as e:
            error_msg = f'An error occured: {e}'
            self.silent_popup('Error',error_msg)
        self.new_window.destroy()

    def inverse_matrix(self):
        """Function to find inverse of a matrix"""
        new_window  = tk.Toplevel(self.root)
        new_window.title("Inverse of Matrix")
        new_window.geometry('400x400')

        note = tk.Label(new_window, text="Select matrix to find Inverse", font=(16))
        note.pack()

        button_frame = tk.Frame(new_window)
        button_frame.pack()

        def inverse_func(matrix_name: str):
            mat_dict={'A': self.matrixA, 'B': self.matrixB, 'C' : self.matrixC}
            mat = mat_dict[matrix_name]
            if mat is None:
                messagebox.showerror("Error", "Selected matrices is not initialized!")
            elif np.linalg.det(mat) == 0:   # matrix having determinant don't have inverse
                messagebox.showerror("Error", f"Matrix {matrix_name} is singular and cannot be inverted.")
            else:
                result = np.linalg.inv(mat)
                msg = f"Inverse of {matrix_name} :\n{result}"
                self.result_label.config(text="Recent: " + msg)
                self.silent_popup('Inverse Result',msg)
            new_window.destroy()


        button_matrixA = tk.Button(button_frame, text="Matrix A", command=lambda: inverse_func("A"))
        self.add_hover_effect(button_matrixA)
        button_matrixA.grid(row=0, column=0, padx=5, pady=10)

        button_matrixB = tk.Button(button_frame, text="Matrix B", command=lambda: inverse_func("B"))
        self.add_hover_effect(button_matrixB)
        button_matrixB.grid(row=1, column=0, padx=5, pady=5)

        button_matrixC = tk.Button(button_frame, text="Matrix C", command=lambda: inverse_func("C"))
        self.add_hover_effect(button_matrixC)
        button_matrixC.grid(row=2, column=0, padx=5, pady=5)
    
    def transpose_matrix(self):
        """Function to find transpose of a matrix"""
        new_window  = tk.Toplevel(self.root)
        new_window.title("Transpose of Matrix")
        new_window.geometry('400x400')

        note = tk.Label(new_window, text="Select matrix to find Transpose", font=(16))
        note.pack()

        button_frame = tk.Frame(new_window)
        button_frame.pack()

        def transpose_func(matrix_name: str):
            mat_dict={'A': self.matrixA, 'B': self.matrixB, 'C' : self.matrixC}
            mat = mat_dict[matrix_name]
            if mat is None:
                messagebox.showerror("Error", "Selected matrices is not initialized!")
            else:
                result = np.transpose(mat)
                msg = f"Transpose of {matrix_name} :\n{result}"
                self.result_label.config(text="Recent:\n" + msg)
                self.silent_popup('Transpose Result',msg)
            new_window.destroy()

        button_matrixA = tk.Button(button_frame, text="Matrix A", command=lambda: transpose_func("A"))
        self.add_hover_effect(button_matrixA)
        button_matrixA.grid(row=0, column=0, padx=5, pady=10)

        button_matrixB = tk.Button(button_frame, text="Matrix B", command=lambda: transpose_func("B"))
        self.add_hover_effect(button_matrixB)
        button_matrixB.grid(row=1, column=0, padx=5, pady=5)

        button_matrixC = tk.Button(button_frame, text="Matrix C", command=lambda: transpose_func("C"))
        self.add_hover_effect(button_matrixC)
        button_matrixC.grid(row=2, column=0, padx=5, pady=5)
    
    def determinant_matrix(self):
        """Function to find determinant of a matrix"""
        new_window  = tk.Toplevel(self.root)
        new_window.title("Determinant of Matrix")
        new_window.geometry('400x400')

        note = tk.Label(new_window, text="Select matrix to find Determinant", font=(16))
        note.pack()

        button_frame = tk.Frame(new_window)
        button_frame.pack()

        def determinant_func(matrix_name: str):
            mat_dict={'A': self.matrixA, 'B': self.matrixB, 'C' : self.matrixC}
            mat = mat_dict[matrix_name]
            if mat is None:
                messagebox.showerror("Error", "Selected matrices is not initialized!")
            else:
                result = np.linalg.det(mat)
                msg = f"Determinant of {matrix_name} :\n{result}"
                self.result_label.config(text="Recent:\n" + msg)
                self.silent_popup('Determinant Result',msg)
            new_window.destroy()

        button_matrixA = tk.Button(button_frame, text="Matrix A", command=lambda: determinant_func("A"))
        self.add_hover_effect(button_matrixA)
        button_matrixA.grid(row=0, column=0, padx=5, pady=10)

        button_matrixB = tk.Button(button_frame, text="Matrix B", command=lambda: determinant_func("B"))
        self.add_hover_effect(button_matrixB)
        button_matrixB.grid(row=1, column=0, padx=5, pady=5)

        button_matrixC = tk.Button(button_frame, text="Matrix C", command=lambda: determinant_func("C"))
        self.add_hover_effect(button_matrixC)
        button_matrixC.grid(row=2, column=0, padx=5, pady=5)
    
    def eigen_matrix(self):
        """Function to find eigen value and eigen vector of a matrix"""
        new_window  = tk.Toplevel(self.root)
        new_window.title("Eigen of Matrix")
        new_window.geometry('400x400')

        note = tk.Label(new_window, text="Select matrix to find Eigen Value and Eigen Vector", font=(16))
        note.pack()

        button_frame = tk.Frame(new_window)
        button_frame.pack()

        def eigen_func(matrix_name: str):
            mat_dict={'A': self.matrixA, 'B': self.matrixB, 'C' : self.matrixC}
            mat = mat_dict[matrix_name]
            if mat is None:
                messagebox.showerror("Error", "Selected matrices is not initialized!")
            else:
                eigen_val, eigen_vector = np.linalg.eig(mat)
                msg = f"Eigen Value of {matrix_name} : {eigen_val}\nEigen Vector of {matrix_name} : {eigen_vector}"
                self.result_label.config(text="Recent:\n" + msg)
                self.silent_popup('Eigen Result',msg)
            new_window.destroy()

        button_matrixA = tk.Button(button_frame, text="Matrix A", command=lambda: eigen_func("A"))
        self.add_hover_effect(button_matrixA)
        button_matrixA.grid(row=0, column=0, padx=5, pady=10)

        button_matrixB = tk.Button(button_frame, text="Matrix B", command=lambda: eigen_func("B"))
        self.add_hover_effect(button_matrixB)
        button_matrixB.grid(row=1, column=0, padx=5, pady=5)

        button_matrixC = tk.Button(button_frame, text="Matrix C", command=lambda: eigen_func("C"))
        self.add_hover_effect(button_matrixC)
        button_matrixC.grid(row=2, column=0, padx=5, pady=5)

    def silent_popup(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("400x400")
        label = tk.Label(popup, text=message, font=("Arial", 12), padx=10, pady=10)
        label.pack()
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)
        return

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Matrix Calculator")
    root.geometry("500x720")  # Set window size
    # root.resizable(0,0) # width, height (can also pass True, False)
    app = Matrix(root)
    root.mainloop()
