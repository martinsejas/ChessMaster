'''
This script will take the path of a chess image as an input, and write out it's position.
'''
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import joblib
from PIL import Image
import numpy as np
from skimage.util.shape import view_as_blocks
from skimage import io, transform


# Function for popup
def show_alert(predicted_label):
    messagebox.showinfo("Predicted Label", predicted_label)


# Function for encoding label
def encode_label(label: str):
    #Splitting the label row by row
    rows = label.split("-")
    
    # Making a list of lists for my final encoded label
    # PreAllocating for good practice
    board = [None] * 8
    
    for row_id, row in enumerate(rows):
        encoded_row = [0] * 8
        row_item = 0  # Initialize row_item outside the loop
            
        for square in row:
            #not get index out of range
            if(row_item > 7):
                break
            
            #If it's a piece, map it according to dictionary
            if square in piece_dictionary:
                encoded_row[row_item] = piece_dictionary[square]
                row_item += 1
            
            #If it's empty squares, adjust accordingly the insertion of the row 
            else:       
                empty_spaces = int(square)
                if empty_spaces == 1:
                    row_item+=1
                else:
                    row_item+= empty_spaces
                          
        board[row_id] = encoded_row
        
    #convert to flat numpy array (for processing)
    return (np.array(board).flatten())


#Function for decoding label 
def decode_label(encoded_label: np.ndarray):
    encoded_label = encoded_label.reshape(8,8)
    
    label = '' #Final label
    
    for row in encoded_label:
        row_string = ''
        empty_count = 0
        for piece_id in row:
            if piece_id == 0:
                empty_count += 1
            else:
                if empty_count > 0:
                    row_string += str(empty_count)
                    empty_count = 0
                row_string += piece_reverse_dictionary[piece_id]
        if empty_count > 0:
            row_string += str(empty_count)
        label += row_string + '-'
    
    # Remove the trailing '-'
    label = label[:-1]
    return label

#Function for resizing_image
def resize_image(image_path:str):
    downsample_size = 200
    square_size = 200//8
    img_read = io.imread(image_path)
    img_read = transform.resize(
      img_read, (downsample_size, downsample_size), mode='constant')
    tiles = view_as_blocks(img_read, block_shape=(square_size, square_size, 3))
    tiles = tiles.squeeze(axis=2)
    return tiles.reshape(64, square_size, square_size, 3)

#This dictionary is for encoding
piece_dictionary = {}

#my pieces are: pnbrqkPNBRQK
piece_dictionary["p"] = 1
piece_dictionary["n"] = 2
piece_dictionary["b"] = 3
piece_dictionary["r"] = 4
piece_dictionary["q"] = 5
piece_dictionary["k"] = 6
piece_dictionary["P"] = 7
piece_dictionary["N"] = 8
piece_dictionary["B"] = 9
piece_dictionary["R"] = 10
piece_dictionary["Q"] = 11
piece_dictionary["K"] = 12

#This dictionary is for decoding
piece_reverse_dictionary = {
    0: '1',
    1: 'p',
    2: 'n',
    3: 'b',
    4: 'r',
    5: 'q',
    6: 'k',
    7: 'P',
    8: 'N',
    9: 'B',
    10: 'R',
    11: 'Q',
    12: 'K'
}

#C:/Users/Martin/Desktop/Class Exercises/AIS S3/ComputerVision/chess-positions/data/1B4R1-2K4p-8-8-R3n1k1-8-8-n4r1N.jpeg

#load model 

model = joblib.load("models/martin_chess.joblib")

root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select Chess Image",filetypes = (("jpeg files","*.jpeg"),("jpeg files","*.jpeg")))

print(root.filename)

image_path = root.filename

img = Image.open(image_path)
img.show()

processed_img = resize_image(image_path)

predicted_label = decode_label(model.predict(processed_img).argmax(axis=1))


#print("Your predicted label is: ", predicted_label)

show_alert(predicted_label)
