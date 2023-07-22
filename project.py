# importing the required modules  
import tkinter as tk
from tkinter import *                     
from tkinter import messagebox as mb     
from tkinter import filedialog as fd     
import os                                 
import shutil                             
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import pandas
from pathlib import Path
import hashlib
import time 
# function to open a file  
def openFile():  
   # selecting the file using the askopenfilename() method of filedialog  
   the_file = fd.askopenfilename(  
      title = "Select a file of any type",  
      filetypes = [("All files", "*.*")]  
      )  
   opener = "xdg-open"
   subprocess.call([opener, the_file]) 
   # os.startfile(os.path.abspath(the_file))  
  
# function to copy a file  
def copyFile():  
   # using the filedialog's askopenfilename() method to select the file  
   fileToCopy = fd.askopenfilename(  
      title = "Select a file to copy",  
      filetypes=[("All files", "*.*")]  
      )   
   directoryToPaste = fd.askdirectory(title = "Select the folder to paste the file")  
  
   # using the try-except method  
   try:  
      # using the copy() method of the shutil module to  
      shutil.copy(fileToCopy, directoryToPaste)  
      mb.showinfo(  
         title = "File copied!",  
         message = "The selected file has been copied to the selected location."  
         )  
   except:   
      mb.showerror(  
         title = "Error!",  
         message = "Selected file is unable to copy to the selected location. Please try again!"  
         )  
#Function to generate insights on type of files and number of files of each type using os.scandir() method
def list_all_files(directory):
    all_files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            all_files.append(entry.path)
        elif entry.is_dir():
            all_files.extend(list_all_files(entry.path))
    return all_files

def generateInsights():
    directory = fd.askdirectory(title="Select the folder to generate insights")
    all_files = list_all_files(directory)
    
    file_types = {}
    files_sizes = {}
    total_files = 0
    total_size = 0
    for file in all_files:
        total_files += 1
        total_size += os.path.getsize(file)
        file_type = os.path.splitext(file)[1]
        if file_type != "":
         if file_type not in file_types.keys():
               file_types[file_type] = 1
               files_sizes[file_type] = os.path.getsize(file)
         else:
               files_sizes[file_type] += os.path.getsize(file)
               file_types[file_type] += 1
    #Generate bar graph using matplotlib and tkinter
    file_types = dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True))
    file_types2 = file_types.copy()
    file_types = dict(list(file_types.items())[:10])
    file_types["Others"] = sum(list(file_types2.values())[10:])
    #Add y value on top of each bar
    #figure, axis = plt.subplots(2, 2)
    plt.subplot(1,2,1)
    #ax1 = plot1.add_subplot(111)
    bars = plt.bar(file_types.keys(), file_types.values())
    c=0
    for bar in bars:
       if c%2==0:
          bar.set_color('#29689e')
       else:
            bar.set_color('#c6c991')
       c+=1
    for i, v in enumerate(file_types.values()):
      plt.text(i - 0.25, v + 0.01, str(v))

    plt.title("Number of Files per File Type")
    #fig1.show()

    files_sizes = dict(sorted(files_sizes.items(), key=lambda x: x[1], reverse=True))
    file_types2 = files_sizes.copy()
    if len(list(files_sizes.values())) > 5:
      files_sizes = dict(list(files_sizes.items())[:5])
      files_sizes["Others"] = sum(list(file_types2.values())[5:])
    
    #plot2 = plt.add_subplot(111)
    #ax2 = plot2.add_subplot(111)
    piechart_colors = ['#F66D44','#FEAE65','#E6F69D','#AADEA7','#64C2A6','#2D87BB']
    plt.subplot(1,2,2)
    plt.pie(files_sizes.values(), labels=files_sizes.keys(), autopct='%1.1f%%', shadow=True, colors=piechart_colors)
    plt.title("Percentage of Files by Size")
    plt.tight_layout()
    plt.show()

    display_text = ""
    for file_type, number_of_files in file_types.items():
        display_text = display_text + "\n" + file_type + ": " + str(number_of_files)
    # using the showinfo() method to display success message
    T=Text(win_root,height=10,width=30)
    l=Label(win_root,text="Insights generated!", padx=3, pady=3, bg="#3C3D3D", fg="#FFFFFF", font="Verdana 10 bold")
    b2 = Button(win_root, text = "Close",command = lambda: [T.pack_forget(),l.pack_forget(),b2.pack_forget()])
    l.pack()
    T.pack(pady=20)
    T.insert(END, "Total number of files: " + str(total_files) + "\n" + "Total size of files: " + str(format_size(total_size)) + "\n" + "File types and number of files of each type: " + "\n" + str(display_text))
    b2.pack(pady=20)

    

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0 
# function to delete a file  
def deleteFile():  
   the_file = fd.askopenfilename(  
      title = "Choose a file to delete",  
      filetypes = [("All files", "*.*")]  
      )   
   os.remove(os.path.abspath(the_file))   
   mb.showinfo(title = "File deleted!", message = "The selected file has been deleted.")  


#Function to delete files of a particular type using os.scandir() method
def select_extension():
   select_extension_window = Toplevel(win_root)
   select_extension_window.title("Select Extension")
   select_extension_window.geometry("300x100+300+250")
   select_extension_window.resizable(0, 0)
   select_extension_window.configure(bg = "#F6EAD7")

   select_extension_label = Label(
      select_extension_window,
      text = "Enter the extension:",
      font = ("verdana", "8"),
      bg = "#F6EAD7",
      fg = "#000000"
      )
   select_extension_label.pack(pady = 4)

   select_extension_field = Entry(
      select_extension_window,
      width = 26,
      textvariable = enteredExtension,
      relief = GROOVE,
      font = ("verdana", "10"),
      bg = "#FFFFFF",
      fg = "#000000"
      )
   select_extension_field.pack(pady = 4, padx = 4)

   submitButton = Button(
      select_extension_window,
      text = "Submit",
      command = delete_extension,
      width = 12,
      relief = GROOVE,
      font = ("verdana", "8"),
      bg = "#C8F25D",
      fg = "#000000",
      activebackground = "#709218",
      activeforeground = "#FFFFFF"
      )
   submitButton.pack(pady = 2)

def delete_extension():
   file_type=enteredExtension.get()
   directory = fd.askdirectory(title="Select the folder to delete files of type: " + file_type)
   all_files = list_all_files(directory)
   deleted_files = 0
   ext_name_size = file_type.__len__()
   for file in all_files:
      if file_type == file[-ext_name_size:]:
         os.remove(os.path.abspath(file))
         deleted_files += 1
   mb.showinfo(title = "Deletion Complete", message = "Deleted " + str(deleted_files) + " files of type: " + file_type + ".")
   
# function to rename a file  
def renameFile():   
   rename_window = Toplevel(win_root)  
   rename_window.title("Rename File")   
   rename_window.geometry("1000x300+300+250")  
   rename_window.resizable(0, 0)   
   rename_window.configure(bg = "#F6EAD7")  
     
   # creating a label  
   rename_label = Label(  
      rename_window,  
      text = "Enter the new file name:",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      )   
   rename_label.pack(pady = 4)  
     
   # creating an entry field  
   rename_field = Entry(  
      rename_window,  
      width = 26,  
      textvariable = enteredFileName,  
      relief = GROOVE,  
      font = ("verdana", "10"),  
      bg = "#FFFFFF",  
      fg = "#000000"  
      )  
   rename_field.pack(pady = 4, padx = 4)  
  
   # creating a button  
   submitButton = Button(  
      rename_window,  
      text = "Submit",  
      command = submitName,  
      width = 12,  
      relief = GROOVE,  
      font = ("verdana", "8"),  
      bg = "#C8F25D",  
      fg = "#000000",  
      activebackground = "#709218",  
      activeforeground = "#FFFFFF"  
      )   
   submitButton.pack(pady = 2)  
  
# defining a function get the file path  
def getFilePath():   
   the_file = fd.askopenfilename(title = "Select the file to rename", filetypes = [("All files", "*.*")])  
   return the_file  
  
# defining a function that will be called when submit button is clicked  
def submitName():  
   renameName = enteredFileName.get()  
   enteredFileName.set("")   
   fileName = getFilePath()   
   newFileName = os.path.join(os.path.dirname(fileName), renameName + os.path.splitext(fileName)[1])   
   os.rename(fileName, newFileName)   
   mb.showinfo(title = "File Renamed!", message = "The selected file has been renamed.")  
     
# defining a function to open a folder  
def openFolder():    
   the_folder = fd.askdirectory(title = "Select Folder to open")   
   subprocess.run(['nautilus',f'{the_folder}'])
   # os.startfile(the_folder)  
  
# defining a function to delete the folder  
def deleteFolder():  
   folderToDelete = fd.askdirectory(title = 'Select Folder to delete')  
   os.rmdir(folderToDelete)  
   mb.showinfo("Folder Deleted!", "The selected folder has been deleted!")  
  
# defining a function to move the folder  
def moveFolder():   
   folderToMove = fd.askdirectory(title = 'Select the folder you want to move')  
   mb.showinfo(message = 'Folder has been selected to move. Now, select the desired destination.')  
   des = fd.askdirectory(title = 'Destination')  
   try:  
      shutil.move(folderToMove, des)   
      mb.showinfo("Folder moved!", 'The selected folder has been moved to the desired Location')  
   except:   
      mb.showerror('Error!', 'The Folder cannot be moved. Make sure that the destination exists')  
  
# defining a function to list all the files available in a folder  
def listFilesInFolder():  
   i = 0    
   the_folder = fd.askdirectory(title = "Select the Folder") 
   all_files = list_all_files(the_folder)
   listFilesWindow = Toplevel(win_root)   
   listFilesWindow.title(f'Files in {the_folder}')   
   listFilesWindow.geometry("1000x300+300+200")  
   listFilesWindow.resizable(0, 0)    
   listFilesWindow.configure(bg = "#EC2FB1")   
   the_listbox = Listbox(  
      listFilesWindow,  
      selectbackground = "#F24FBF",  
      font = ("Verdana", "10"),  
      background = "#FCFFB2"  
      )    
   the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)    
   the_scrollbar = Scrollbar(  
      the_listbox,  
      orient = VERTICAL,  
      command = the_listbox.yview  
      )  
   the_scrollbar.pack(side = RIGHT, fill = Y)    
   the_listbox.config(yscrollcommand = the_scrollbar.set)  
   i=0
   for file in all_files:
      the_listbox.insert(END, "[" + str(i+1) + "] " + str(file))
      i += 1
   the_listbox.insert(END, "")  
   the_listbox.insert(END, "Total Files: " + str(i))  



def free_space_on_disk():
   root="/"
   
   total,used,free=shutil.disk_usage(root)

   used=total-free

   categories = ['Used Space', 'Free Space']
   sizes = [(used*100.0)/total,(free*100.0)/total]
   # Create the pie chart
   plt.figure(figsize=(6,6))  # Adjust the figure size as needed
   plt.title('Disk Usage')
   plt.pie(sizes, labels=categories,autopct='%1.1f%%', startangle=69)
   proxy_artists = [plt.Rectangle((-1, -1), 0.5, 0.5, fc='C0'),
                 plt.Rectangle((-1, -1), 0.5, 0.5, fc='C1')]
   legend_labels=[format_size(used),format_size(free)]
   plt.legend(proxy_artists, legend_labels, loc='upper left')
   plt.show()


def show_space_used():

   the_path = fd.askdirectory(title = "Select Folder to check the size of") 

   # folder_space_usage=get_size(str(the_path))

   ret = subprocess.run(["du","-sh",f"{the_path}"],capture_output=True, text=True, check=True)
   ret1=ret.stdout.strip().split('\t')
   ret=ret1[0]
   # print(ret)

   # folder_space_usage = (folder_space_usage / (2**30))
   # print(the_path)
   # print(folder_space_usage / (2**30))

      
   ShowFolderSpaceUsage = Toplevel(win_root)  
   ShowFolderSpaceUsage.title(f'Usage of {the_path}')  
   # specifying the size and position of the window  
   ShowFolderSpaceUsage.geometry("400x200+300+200")  
   # disabling the resizable option  
   ShowFolderSpaceUsage.resizable(1, 1)  
   ShowFolderSpaceUsage.configure(bg = "#EC2FB1")  
  
   # creating a list box  
   the_listbox = Listbox(  
      ShowFolderSpaceUsage,  
      selectbackground = "#FFFFFF",  
      font = ("Verdana", "10"),  
      background = "#FCFFB2"  
      )  
   # placing the list box on the window  
   the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
     
   # creating a scroll bar  
   the_scrollbar = Scrollbar(  
      the_listbox,  
      orient = VERTICAL,
      command = the_listbox.yview  
      )  
   # placing the scroll bar to the right side of the window  
   the_scrollbar.pack(side = RIGHT, fill = Y)  
  
   # setting the yscrollcommand parameter of the listbox's config() method to the scrollbar  
   the_listbox.config(yscrollcommand = the_scrollbar.set)  

   the_listbox.insert(END,f"Space Utilisation : {ret} ")

def detect_duplicate():
   parent_folder = fd.askdirectory(title="Select a folder to search for duplicates")
   all_files = list_all_files(parent_folder)
   hash_dictionary = dict()
   duplicates = []
   for file in all_files:
      file_path = Path(file)
      hash = hashlib.md5(open(file_path,'rb').read()).hexdigest()
      if hash in hash_dictionary.keys():
         first = hash_dictionary[hash]
         second = file_path
         tic1 = time.ctime(os.path.getctime(first))
         tic2 = time.ctime(os.path.getctime(second))
         if(tic1 > tic2):
            duplicates.append(first)
            hash_dictionary[hash] = second
         else:
            duplicates.append(second)
            hash_dictionary[hash] = first
      else:
         hash_dictionary[hash] = file_path
   
   if len(duplicates) == 0:
      mb.showinfo(title = "No duplicates found!", message = "No duplicates found in the selected folder.")
   else:
      # creating an object of Toplevel class  
      listFilesWindow = Toplevel(win_root)  
      listFilesWindow.title(f'Duplicates in {parent_folder}')  
      listFilesWindow.geometry("1000x300+300+200")    
      listFilesWindow.resizable(0, 0)  
      listFilesWindow.configure(bg = "#EC2FB1")  
   
      # creating a list box  
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FCFFB2"  
         )  
      # placing the list box on the window  
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      #creating a scroll bar  
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )   
      the_scrollbar.pack(side = RIGHT, fill = Y)  
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0
      while i < len(duplicates):    
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(duplicates[i]))
         the_listbox.insert(END, "Original File: " + str(hash_dictionary[hashlib.md5(open(duplicates[i],'rb').read()).hexdigest()])) 
         i += 1  
       
      the_listbox.insert(END, "Total Files: " + str(len(duplicates))) 
   
def deleteDuplicates():
   parent_folder = fd.askdirectory(title="Select a folder to search for duplicates")
   all_files = list_all_files(parent_folder)
   hash_dictionary = dict()
   duplicates = []

   for file in all_files:
      file_path = Path(file)
      hash = hashlib.md5(open(file_path,'rb').read()).hexdigest()
      if hash in hash_dictionary.keys():
         first = hash_dictionary[hash]
         second = file_path
         tic1 = time.ctime(os.path.getctime(first))
         tic2 = time.ctime(os.path.getctime(second))
         if(tic1 > tic2):
            duplicates.append(first)
            os.remove(first)
            hash_dictionary[hash] = second
         else:
            duplicates.append(second)
            os.remove(second)
            hash_dictionary[hash] = first
      else:
         hash_dictionary[hash] = file_path
   
   if len(duplicates) == 0:
      mb.showinfo(title = "No duplicates found!", message = "No duplicates found in the selected folder.")
   else:
      # creating an object of Toplevel class  
      listFilesWindow = Toplevel(win_root)  
      listFilesWindow.title(f'Following duplicates deleted {parent_folder}')  
      listFilesWindow.geometry("1000x300+300+200")    
      listFilesWindow.resizable(0, 0)  
      listFilesWindow.configure(bg = "#EC2FB1")  
   
      # creating a list box  
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FCFFB2"  
         )  
      # placing the list box on the window  
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      #creating a scroll bar  
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )   
      the_scrollbar.pack(side = RIGHT, fill = Y)  
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0
      while i < len(duplicates):    
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(duplicates[i])) 
         #the_listbox.insert(END, "Original File: " + str(hash_dictionary[hashlib.md5(open(duplicates[i],'rb').read()).hexdigest()])) 
         i += 1  
      the_listbox.insert(END, "")  
      the_listbox.insert(END, "Total Files: " + str(len(duplicates))) 


def search_by_extension():  
   # creating another window  
   rename_window = Toplevel(win_root)   
   rename_window.title("Extension")    
   rename_window.geometry("300x300+300+250")  
   rename_window.resizable(0, 0)  
   rename_window.configure(bg = "#F6EAD7")  
   rename_label = Label(  
      rename_window,  
      text = "Enter the extension:",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      )   
   rename_label.pack(pady = 4)   
   rename_field = Entry(  
      rename_window,  
      width = 26,  
      textvariable = enteredExtension,  
      relief = GROOVE,  
      font = ("verdana", "10"),  
      bg = "#FFFFFF",  
      fg = "#000000"  
      )  
   rename_field.pack(pady = 4, padx = 4)  
   submitButton = Button(  
      rename_window,  
      text = "Submit",  
      command = submitName2,  
      width = 12,  
      relief = GROOVE,  
      font = ("verdana", "8"),  
      bg = "#C8F25D",  
      fg = "#000000",  
      activebackground = "#709218",  
      activeforeground = "#FFFFFF"  
      )    
   submitButton.pack(pady = 2)  
  
def getFolder():  
   the_folder = fd.askdirectory() 
   return the_folder  
  
# defining a function that will be called when submit button is clicked  
def submitName2():   
   renameName = enteredExtension.get()  
   enteredExtension.set("")   
   folder = getFolder()  
   all_files = list_all_files(folder)
   res = []
   filepaths = []
   for file in all_files:
      if file.endswith(renameName):
         temp=file.split("\\")
         res.append(temp[-1])
         filepaths.append(Path(file))
   if len(res) == 0:
      mb.showinfo(title = "No files found!", message = "No files found in the selected folder with the given extension.")
   else:
      # creating an object of Toplevel class  
      listFilesWindow = Toplevel(win_root)   
      listFilesWindow.title(f'Files with extension {renameName} in {folder}')   
      listFilesWindow.geometry("1000x300+300+200")  
      listFilesWindow.resizable(0, 0)  
      listFilesWindow.configure(bg = "#EC2FB1")   
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FCFFB2"  
         )  
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )   
      the_scrollbar.pack(side = RIGHT, fill = Y)   
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0 
      while i < len(res):  
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(res[i]) + " (path: " + str(filepaths[i]) + ")")  
         i += 1  
      the_listbox.insert(END, "")  
      the_listbox.insert(END, "Total Files: " + str(len(res))) 
   
def searchLargeFiles():
   folder = fd.askdirectory(title="Select a folder to search for large files")
   all_files = list_all_files(folder)
   largefiles = []
   size = []
   paths = []
   for file in all_files:
      file_path = Path(file)
      if file_path.stat().st_size > 100*1024*1024:
         temp=file.split("\\")
         largefiles.append(temp[-1])
         paths.append(file_path)
         size.append(format_size(file_path.stat().st_size))
   if len(largefiles) == 0:
      mb.showinfo(title = "No large files found!", message = "No large files found in the selected folder.")
   else:
      listFilesWindow = Toplevel(win_root)   
      listFilesWindow.title(f'Large files in {folder}')   
      listFilesWindow.geometry("1000x300+300+200")   
      listFilesWindow.resizable(0, 0)  
      listFilesWindow.configure(bg = "#EC2FB1")  
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FCFFB2"  
         )   
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )  
      the_scrollbar.pack(side = RIGHT, fill = Y)  
      # print(largefiles)
      # setting the yscrollcommand parameter of the listbox's config() method to the scrollbar  
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0
      while i < len(largefiles):  
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(largefiles[i]) + " (size: " + str(size[i]) + ")" + " (path: " + str(paths[i]) + ")")
         i += 1  
      the_listbox.insert(END, "")  
      the_listbox.insert(END, "Total Files: " + str(len(largefiles))) 

def filteredSearch():
   rename_window = Toplevel(win_root)  
   rename_window.title("Enter filters")  
   rename_window.geometry("300x300+300+250")   
   rename_window.resizable(0, 0)  
   rename_window.configure(bg = "#F6EAD7")  
     
   # creating a label  
   size_label = Label(  
      rename_window,  
      text = "Enter the size:(in MBs)",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      )  
   size_label.pack(pady = 4)  
     
   # creating an entry field  
   size_field = Entry(  
      rename_window,  
      width = 26,  
      textvariable = enteredFileName, 
      relief = GROOVE,  
      font = ("verdana", "10"),  
      bg = "#FFFFFF",  
      fg = "#000000"  
      )  
   size_field.pack(pady = 4, padx = 4)  
   extension_label = Label(  
      rename_window,  
      text = "Enter the extensions:(comma seperated)",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      ) 
   extension_label.pack(pady=4)

   extension_field = Entry(  
      rename_window,  
      width = 26,  
      textvariable = enteredExtension,  
      relief = GROOVE,  
      font = ("verdana", "10"),  
      bg = "#FFFFFF",  
      fg = "#000000"  
      )
   extension_field.pack(pady=4)  
   submitButton = Button(  
      rename_window,  
      text = "Submit",  
      command = submitName3,  
      width = 12,  
      relief = GROOVE,  
      font = ("verdana", "8"),  
      bg = "#C8F25D",  
      fg = "#000000",  
      activebackground = "#709218",  
      activeforeground = "#FFFFFF"  
      )  
   submitButton.pack(pady = 2)  
   
# defining a function get the file path  
def getFolder():  
   the_folder = fd.askdirectory()  
   return the_folder  
  
# defining a function that will be called when submit button is clicked  
def submitName3():   
   size = enteredFileName.get()
   if(size == ""):
      size = 0
   size = float(size)
   size = size*1024*1024
   enteredFileName.set("")  
   extension = enteredExtension.get()
   enteredExtension.set("")
   extension = extension.split(",")
   folder = getFolder()  
   all_files = list_all_files(folder)
   arr = []
   arr2 = []
   paths = []
   for file in all_files:
         res = len(extension) == 0
         for ext in extension:
            if(file.endswith(ext)):
               res = True
               break
         if not res:
            continue
         file_path = Path(file)
         if(file_path.stat().st_size >= size):
            temp=file.split("\\")
            arr.append(temp[-1])
            paths.append(file_path)
            arr2.append(format_size(file_path.stat().st_size))
   if len(arr) == 0:
      mb.showinfo(title = "No files found!", message = "No files found in the selected folder with the given filters.")
   else:
      listFilesWindow = Toplevel(win_root)   
      listFilesWindow.title(f'Files with selected filters in {folder}')  
      listFilesWindow.geometry("1000x300+300+200") 
      listFilesWindow.resizable(0, 0)   
      listFilesWindow.configure(bg = "#EC2FB1")  
      # creating a list box  
      the_listbox = Listbox(  
         listFilesWindow,  
         selectbackground = "#F24FBF",  
         font = ("Verdana", "10"),  
         background = "#FCFFB2"  
         )   
      the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
      
      # creating a scroll bar  
      the_scrollbar = Scrollbar(  
         the_listbox,  
         orient = VERTICAL,  
         command = the_listbox.yview  
         )  
      the_scrollbar.pack(side = RIGHT, fill = Y)  
   
      # setting the yscrollcommand parameter of the listbox's config() method to the scrollbar  
      the_listbox.config(yscrollcommand = the_scrollbar.set)  
      i=0 
      while i < len(arr):  
         # using the insert() method to insert the file details in the list box  
         the_listbox.insert(END, "[" + str(i+1) + "] " + str(arr[i]) + " (size: " +  arr2[i] + ") (path: " + str(paths[i]) + ")")
         i += 1  
      the_listbox.insert(END, "")  
      the_listbox.insert(END, "Total Files: " + str(len(arr)))



def least_accessed_files():
   the_path = fd.askdirectory(title = "Select folder to check last access of files") 
   if type(the_path) is tuple:
      return
   ShowLeastAccessedFiles = Toplevel(win_root)  
   ShowLeastAccessedFiles.title(f'Least Accessed files in {the_path}')  
   ShowLeastAccessedFiles.geometry("1000x800+100+100")   
   ShowLeastAccessedFiles.resizable(1, 1)    
   ShowLeastAccessedFiles.configure(bg = "#FCFFB2")  
  
   tree = ttk.Treeview(ShowLeastAccessedFiles)
   tree["columns"] = ("Column 1", "Column 2", "Column 3")
   tree.heading("#0", text="", anchor=tk.W)  # Index column
   tree.column("#0", anchor=tk.W, width=10)
   tree.heading("Column 1", text="Index")
   tree.column("Column 1", anchor=tk.W, width=60)
   tree.heading("Column 2", text="File Name")
   tree.column("Column 2", anchor=tk.W, width=400)
   tree.heading("Column 3", text="Date Accessed")
   tree.column("Column 3", anchor=tk.W, width=200)
   # tree.heading("Column 4", text="Time Accessed")
   # tree.column("Column 4", anchor=tk.W, width=200)
   cnt=0
   lis=[]
   for file_name in os.listdir(the_path):
      file_path=the_path+"/"+str(file_name)
      if(os.path.isfile(file_path)):
         cnt+=1
         # print(file_name)
         ret = subprocess.run(["stat",f"{file_path}"],capture_output=True, text=True, check=True)
         ret1=ret.stdout.strip().split('\n')
         ret2=ret1[4].split(' ')
         # the_listbox.insert(END,"{:>50} {:>50} {:>50}".format(f"{file_path}",f"{ret2[1]}",f"{ret2[2]}"))
         # tree.insert("",END,iid=cnt,values=(f"[{cnt}]",f"{file_path}",f"{ret2[1]}",f"{ret2[2]}"))
         ret3=ret2[1].split('-')
         ret3=ret3[0]+"/"+ret3[1]+"/"+ret3[2]
         lis.append([f"{file_path}",ret3])

   df = pandas.DataFrame(data=lis,columns=["File Name","Date Modified"])
   # print(df)
   df.sort_values(['Date Modified'],inplace=True)
   # print(df)
   lisn = df.to_numpy().tolist()
   for index, row in enumerate(lisn, start=1):
      row.insert(0,"["+str(index)+"]")
      tree.insert("", tk.END, values=row)
   # print(lisn)
   tree.pack()

if __name__ == "__main__":   
   win_root = Tk()   
   win_root.title("Wizard Of Systems Programming")  
   #win_root.geometry("500x700+650+250") 
   win_root.resizable(1, 1) 
   width = win_root.winfo_screenwidth()  # Getting the height and width of the screen
   height = win_root.winfo_screenheight() 
   win_root.geometry("%dx%d" % (780, height/1.2))  # Opening the window in full screen 
   win_root.configure(bg = "#3C3D3D")  
  
   # creating the frames using the Frame() widget  
   header_frame = Frame(win_root, bg = "#3C3D3D")  
   buttons_frame = Frame(win_root, bg = "#3C3D3D")  
  
   # using the pack() method to place the frames in the window  
   header_frame.pack(fill = "both")  
   buttons_frame.pack(expand = TRUE, fill = "both")  
  
   # creating a label using the Label() widget  
   header_label = Label(  
      header_frame,  
      text = "File Manager",  
      font = ("verdana", "16"),  
      bg = "#3C3D3D",  
      fg = "#FFFFFF"  
      )  
  
   # using the pack() method to place the label in the window  
   header_label.pack(expand = TRUE, fill = "both", pady = 12)  
  
   # creating the buttons using the Button() widget  
   # open button  
   color1="#3C3D3D"
   color2="#FFFFFF"
   color3="#FC5B05"
   color4="#000000"
   open_button = Button(  
      buttons_frame,  
      text = "Open a File",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = openFile,
      )  
   
   disk_space_usage = Button(  
      buttons_frame,  
      text = "Check Disk Usage",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = free_space_on_disk  
      )  
  
   show_space_usage = Button(  
      buttons_frame,  
      text = "Check Folder's Space Usage",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = show_space_used 
      )  
   least_access = Button(  
      buttons_frame,  
      text = "Check least accessed files",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = least_accessed_files 
      )  
   
   # copy button  
   copy_button = Button(  
      buttons_frame,  
      text = "Copy a File",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = copyFile  
      )  
  
   # delete button  
   delete_button = Button(  
      buttons_frame,  
      text = "Delete a File",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = deleteFile  
      )  
  
   # rename button  
   rename_button = Button(  
      buttons_frame,  
      text = "Rename a File",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = renameFile  
      )  
  
   # open folder button  
   # open_folder_button = Button(  
   #    buttons_frame,  
   #    text = "Open a Folder",  
   #    font = ("verdana", "10"),  
   #    width = 26,  
   #    bg = color1,  
   #    fg = color2,  
   #    relief = GROOVE,  
   #    activebackground = color3,  
   #    activeforeground = color4,  
   #    command = openFolder  
   #    )  
  
   # delete folder button  
   # delete_folder_button = Button(  
   #    buttons_frame,  
   #    text = "Delete a Folder",  
   #    font = ("verdana", "10"),  
   #    width = 26,  
   #    bg = color1,  
   #    fg = color2,  
   #    relief = GROOVE,  
   #    activebackground = color3,  
   #    activeforeground = color4,  
   #    command = deleteFolder  
   #    )  
  
   # move folder button  
   move_folder_button = Button(  
      buttons_frame,  
      text = "Move a Folder",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = moveFolder  
      )  
  
   # list all files button  
   list_button = Button(  
      buttons_frame,  
      text = "List all files in Folder",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command = listFilesInFolder  
      )  
   detect_duplicate_button = Button(  
      buttons_frame,  
      text = "Duplicates in Folder",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command =  detect_duplicate
      ) 
   
   search_extension_button = Button(  
      buttons_frame,  
      text = "Search by Extension",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command =  search_by_extension
      ) 
   search_largefile_button = Button(  
      buttons_frame,  
      text = "List Large Files",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command =  searchLargeFiles
      ) 
   filtered_search_button = Button(  
      buttons_frame,  
      text = "Filtered Search",  
      font = ("verdana", "10"),  
      width = 26,  
      bg = color1,  
      fg = color2,  
      relief = GROOVE,  
      activebackground = color3,  
      activeforeground = color4,  
      command =  filteredSearch
      )
   generate_insights_button = Button(
        buttons_frame,
        text = "Generate Insights",
        font = ("verdana", "10"),
        width = 26,
        bg = color1,
        fg = color2,
        relief = GROOVE,
        activebackground = color3,
        activeforeground = color4,
        command = generateInsights
    )
   delete_files_of_type_button = Button(
        buttons_frame,
        text = "Delete by extension",
        font = ("verdana", "10"),
        width = 26,
        bg = color1,
        fg = color2,
        relief = GROOVE,
        activebackground = color3,
        activeforeground = color4,
        command = select_extension
      )
   delete_duplicates_button = Button(
        buttons_frame,
        text = "Delete Duplicates",
        font = ("verdana", "10"),
        width = 26,
        bg = color1,
        fg = color2,
        relief = GROOVE,
        activebackground = color3,
        activeforeground = color4,
        command = deleteDuplicates
      )

   # using the pack() method to place the buttons in the window  
   #open_button.pack(pady = 8)  
   # copy_button.pack(pady = 8)  
   # #delete_button.pack(pady = 8)  
   # rename_button.pack(pady = 8)  
   # open_folder_button.pack(pady = 8)  
   # delete_folder_button.pack(pady = 8)  
   # move_folder_button.pack(pady = 8)  
   list_button.grid(row=0,column=0,padx=3,pady = 5)  
   disk_space_usage.grid(row=0,column=1,padx=3,pady=5)
   show_space_usage.grid(row=0,column=2,padx=3,pady=10)
   least_access.grid(row=1,column=0,padx=3,pady=5)
   detect_duplicate_button.grid(row=1,column=1,padx=3,pady = 5)
   generate_insights_button.grid(row=1,column=2,padx=3,pady = 10)
   search_extension_button.grid(row=2,column=0,padx=3,pady = 10)
   search_largefile_button.grid(row=2,column=1,padx=3,pady = 5)
   filtered_search_button.grid(row=2,column=2,padx=3,pady = 5)
   delete_files_of_type_button.grid(row=3,column=0,padx=15,pady = 10)
   delete_duplicates_button.grid(row=3,column=2,padx=15,pady = 10)
   open_button.grid(row=4,column=0,padx=3,pady = 5)
   copy_button.grid(row=4,column=1,padx=3,pady = 5)
   delete_button.grid(row=4,column=2,padx=3,pady = 10)
   rename_button.grid(row=3,column=1,padx=3,pady = 5)
   # open_folder_button.grid(row=5,column=1,padx=3,pady = 5)
   # delete_folder_button.grid(row=5,column=2,padx=3,pady = 5)
   # creating an object of the StringVar() class  
   enteredFileName = StringVar()  
   enteredExtension = StringVar()
   

   # running the window  
   win_root.mainloop()  