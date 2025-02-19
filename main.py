import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox

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

        self.button_matrixA = tk.Button(self.button_frame, text="Matrix A", command=lambda: self.take_input('A'))
        self.button_matrixA.grid(row=0, column=0, padx=5, pady=5)
        self.add_hover_effect(self.button_matrixA)

        self.button_matrixB = tk.Button(self.button_frame, text="Matrix B", command=lambda: self.take_input('B'))
        self.button_matrixB.grid(row=0, column=1, padx=5, pady=5)
        self.add_hover_effect(self.button_matrixB)

        self.button_matrixC = tk.Button(self.button_frame, text="Matrix C", command=lambda: self.take_input('C'))
        self.button_matrixC.grid(row=0, column=2, padx=5, pady=5)
        self.add_hover_effect(self.button_matrixC)

        self.button_show = tk.Button(root, text="Show Matrix Data", command=self.show_matrix_data)
        self.button_show.pack(pady=5)
        self.add_hover_effect(self.button_show)

        self.button_add = tk.Button(root, text="Add Matrices", command=self.add_matrix)
        self.button_add.pack(pady=5)
        self.add_hover_effect(self.button_add)

        self.button_subtract = tk.Button(root, text="Subtract Matrices", command=self.subtract_matrix_backend)
        self.button_subtract.pack(pady=5)
        self.add_hover_effect(self.button_subtract)

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
        size_str = simpledialog.askstring("Matrix Size", f"Enter {matrix_name} size in n,m format:")
        try:
            size = tuple(map(int, size_str.split(',')))
            if len(size) != 2 or size[0] <= 0 or size[1] <= 0:
                messagebox.showerror("Invalid Input", "Please enter two positive integers separated by a comma (e.g., 2,3).")
                return

            # Create the matrix grid window
            self.grid_window = tk.Toplevel(self.root)
            self.grid_window.title(f"Enter Values for Matrix {matrix_name}")
            self.grid_window.geometry("400x400")
            
            self.entries = []  # To store the Entry widgets
            self.size = size

            # Create the grid of Entry widgets
            for i in range(size[0]):
                row_entries = []
                for j in range(size[1]):
                    entry = tk.Entry(self.grid_window, width=5)
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.entries.append(row_entries)

            # Add a button to save the input and close the grid window
            save_button = tk.Button(self.grid_window, text="Save Matrix", command=lambda: self.save_matrix(matrix_name))
            save_button.grid(row=size[0], column=0, columnspan=size[1], pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_matrix(self, matrix_name):
        """Function to save the values from the Entry widgets into the matrix"""
        try:
            matrix = np.zeros(self.size, dtype=int)
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    value = self.entries[i][j].get()
                    if value.isdigit():
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
            self.grid_window.destroy()  # Close the grid window after saving

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_matrix_data(self):
        """ Displays the matrix data in a dialog box """
        data_str = f"Matrix A:\n{self.matrixA}\n\nMatrix B:\n{self.matrixB}\n\nMatrix C:\n{self.matrixC}"
        # messagebox.showinfo("Matrix Data", data_str, icon = "none")
        self.silent_popup('Matrix Data',data_str)

    def add_matrix(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title(f"Add Matrices")
        self.new_window.geometry("400x400")

        # Store equation text
        self.equation_text = tk.StringVar()
        self.equation_text.set("")  # Initially empty
        
        # eqn stores the eqn value 
        eqn = []

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
                        self.equation_text.set(current_text[:-1])  # Remove last character (mat)
                    else:
                        self.equation_text.set(current_text[:-4])  # Remove last 3 character ( _,+,mat,_ )
                    eqn.pop()
                return  # Stop execution here, don't add anything after deleting
            else:    
                eqn.append(matrix_name)
                #  matrix button
                # if current_text and not current_text.endswith('+ '):
                if current_text:  
                    current_text += " + "  # Ensure proper formatting
                
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
        """ Performs the matrix addition """
        try:
            # print(f'eqn = {eqn}')
            if eqn == []:
                ans = '0'
                result_str = f"Addition Reult: {ans}"
                self.result_label.config(text="Result: " + ans)
                messagebox.showinfo("Addition Result", result_str)
            else:
                mat_dict={'A': self.matrixA, 'B': self.matrixB, 'C' : self.matrixC}

                # checking if any matrix of eqn is of None type (i.e. value is not added in that matrix)
                if any(mat_dict.get(mat) is None for mat in eqn):
                    messagebox.showerror("Error","One or more selected matrices are not initialized! ")
                    self.new_window.destroy()
                    return

                # Ensure all matrices have the same shape
                shape = mat_dict.get(eqn[0]).shape
                if not all(mat_dict.get(i).shape == shape for i in eqn):
                    messagebox.showerror("Error", "Matrices must have the same dimensions for addition!")
                    return

                # Perform addition
                matrices = [mat_dict.get(i) for i in eqn]
                self.ans = np.sum(matrices, axis=0)
                result_str = f"Addition Result:\n{self.ans}"
                self.result_label.config(text="Result: " + result_str)
                messagebox.showinfo("Addition Result", result_str)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        self.new_window.destroy()

    def subtract_matrix_backend(self):
        """ Performs the matrix subtraction """
        try:
            matrices = [self.matrixA, self.matrixB, self.matrixC]
            matrices = [mat for mat in matrices if mat is not None]

            if len(matrices) < 2:
                messagebox.showerror("Error", "Please initialize at least two matrices to subtract.")
                return

            # Ensure all matrices have the same shape
            shape = matrices[0].shape
            if not all(mat.shape == shape for mat in matrices):
                messagebox.showerror("Error", "Matrices must have the same dimensions for subtraction!")
                return

            # Perform subtraction
            self.ans = matrices[0] - np.sum(matrices[1:], axis=0)
            result_str = f"Subtraction Result:\n{self.ans}"
            self.result_label.config(text="Result: " + result_str)
            messagebox.showinfo("Subtraction Result", result_str)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def silent_popup(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("400x300")
        label = tk.Label(popup, text=message, font=("Arial", 12), padx=10, pady=10)
        label.pack()
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)
        popup.mainloop()

# silent_popup("Matrix Data", "Matrix A:\n1 2\n3 4")  # Example


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Matrix Calculator")
    root.geometry("400x500")  # Set window size
    app = Matrix(root)
    root.mainloop()
