# -*- coding: utf-8 -*-

from PIL import Image
from numpy import *
import os 

def asc_convert(brightness):
    """
    

    Parameters
    ----------
    brightness : float
        the absolute brightness of the 'pixel' on a scale of 0-255

    Returns
    -------
    str
        the ascii character with corresponding boldness

    """
    asc_char = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"     #ascii value 'table'
    position = round((brightness / 255)*64)     #uses the brightness of pixel to infer which ascii character to use
    return asc_char[position]
    
print("Welcome to the image->ASCII converter. Smaller images generally give better results. After answering some questions, you'll have your very own ASCII art!")
dir_path = os.path.dirname(os.path.realpath(__file__))        #finds the path of the python file
ext = input("Do you want the ascii in a .txt or .html file? Enter the desired file extension: ")
if ext == ".html":
    rgb = input("Do you want a greyscale, or colour ASCII image? Please specify 'colour' or 'bw': ")
opacity = input("Now please choose the algorithm to calculate pixel opacity. Either 'average', 'maxmin', 'luminosity', or 'help' for more info: ")
if opacity == "help":
    print("The 'average' algorithm calculates the character opacity based on the average value of the RGB data.")
    print("The 'maxmin' algorithm calculates the opacity by the average of the highest and lowest RGB values.")
    print("The 'luminosity' algorithm takes a weighted average of the RGB data to account for human perception.")
    print("There isn't much difference between the output of the 3 algorithms. If there are large blocks of single colour, I recommend luminosity.")
    opacity = input("Now please choose the algorithm to calculate pixel opacity. Either 'average', 'maxmin', or 'luminosity': ")
text_file = open(dir_path+"/ASCII-output"+ext, "w", encoding='utf-8')     #creates a text file in the python file directory
file_name = input("Please enter the name of the file to be converted: ")     #asks user to enter image file name - image must be in python file directory
im = Image.open(file_name)
print("This is a", im.format, "of size", im.size, "pixels, and colour format", im.mode) # prints some info about the image
print("The program is generating the ASCII image now. Please wait.")


#following lines create the arrays that will be used throughout the code
colour = zeros((im.size[0], im.size[1]), dtype=tuple)       #stores the colour of each pixel according to its x and y
brightness = zeros((im.size[0], im.size[1]))            #stores the 'boldness' of each pixel
output = zeros((im.size[0], im.size[1]), dtype=str)     #stores the corresponding ascii character of each pixel

for x in range(im.size[0]):
    for y in range(im.size[1]):
        colour[x, y] = im.getpixel((x, y))      #finds colour of each pixel

if im.mode == "RGBA":   #bug fixes non-rgb images
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            colour[x, y] = colour[x, y][:3]

#following code computes the boldness of each 'pixel' according to chosen algorithm
if opacity == "average":
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            r, g, b = colour[x, y]
            brightness[x, y] = (r + g + b) / 3      #computes brightness of each ascii character from pixel
elif opacity == "maxmin":
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            r, g, b = colour[x, y]
            brightness[x, y] = (max(r, g, b) + min(r, g, b)) / 2        #computes brightness of each ascii character from pixel
else:
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            r, g, b = colour[x, y]
            brightness[x, y] = 0.21 * r + 0.72 * g + 0.07 * b        #computes brightness of each ascii character from pixel


for x in range(im.size[0]):
    for y in range(im.size[1]):
        output[x, y] = asc_convert(brightness[x, y])        #stores the array of ascii characters that will become the image

line = ""       #creates the basis of the output
if ext == ".html":
    if rgb == "colour":
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                r, g, b = colour[x, y]
                r, g, b = str(r), str(g), str(b)        #turns float to str
                line += '<span style="color: rgb(' + r + "," + g + "," + b + ')">' + 2 * output[x, y] + "</span>"
                #above line uses the str rgb values to make the corresponding ascii character that colour. 
                #twice the output is used to avoid 'squishing' of the image
            line += "<br>"          #new line command in html
    else:
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                line += 2 * output[x, y]        #twice the output is used to avoid 'squishing' of the image
            line += "<br>"          #new line command in html
    text_file.write('<html style="background-color: black; font-family:consolas; color: white">')     #initiates the html, and the black background
    text_file.write(line)               #pastes the entire ascii text
    text_file.write("</html>")          #finishes the text
    text_file.close()
else:
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            line += 2 * output[x, y]        #twice the output is used to avoid 'squishing' of the image
        line += "\n"          #new line command
    text_file.write(line)               #pastes the entire ascii text
    text_file.close()
print("All done! Please check the file directory for the output file :)")