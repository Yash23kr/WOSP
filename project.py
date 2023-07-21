# importing the required modules  
import tkinter as tk
from tkinter import *                   # importing all the widgets and modules from tkinter  
from tkinter import messagebox as mb    # importing the messagebox module from tkinter  
from tkinter import filedialog as fd    # importing the filedialog module from tkinter  
import os                               # importing the os module  
import shutil                           # importing the shutil module  
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import pandas
  
# ----------------- defining functions -----------------  
# function to open a file  
def openFile():  
   # selecting the file using the askopenfilename() method of filedialog  
   the_file = fd.askopenfilename(  
      title = "Select a file of any type",  
      filetypes = [("All files", "*.*")]  
      )  
   # opening a file using the startfile() method of the os module  
   os.startfile(os.path.abspath(the_file))  
  
# function to copy a file  
def copyFile():  
   # using the filedialog's askopenfilename() method to select the file  
   fileToCopy = fd.askopenfilename(  
      title = "Select a file to copy",  
      filetypes=[("All files", "*.*")]  
      )  
   # using the filedialog's askdirectory() method to select the directory  
   directoryToPaste = fd.askdirectory(title = "Select the folder to paste the file")  
  
   # using the try-except method  
   try:  
      # using the copy() method of the shutil module to  
      # paste the select file to the desired directory  
      shutil.copy(fileToCopy, directoryToPaste)  
      # showing success message using the messagebox's showinfo() method  
      mb.showinfo(  
         title = "File copied!",  
         message = "The selected file has been copied to the selected location."  
         )  
   except:  
      # using the showerror() method to display error  
      mb.showerror(  
         title = "Error!",  
         message = "Selected file is unable to copy to the selected location. Please try again!"  
         )  
  
# function to delete a file  
def deleteFile():  
   # selecting the file using the filedialog's askopenfilename() method  
   the_file = fd.askopenfilename(  
      title = "Choose a file to delete",  
      filetypes = [("All files", "*.*")]  
      )  
   # deleting the file using the remove() method of the os module  
   os.remove(os.path.abspath(the_file))  
   # displaying the success message using the messagebox's showinfo() method  
   mb.showinfo(title = "File deleted!", message = "The selected file has been deleted.")  
  
# function to rename a file  
def renameFile():  
   # creating another window  
   rename_window = Toplevel(win_root)  
   # setting the title  
   rename_window.title("Rename File")  
   # setting the size and position of the window  
   rename_window.geometry("300x100+300+250")  
   # disabling the resizable option  
   rename_window.resizable(0, 0)  
   # setting the background color of the window to #F6EAD7  
   rename_window.configure(bg = "#F6EAD7")  
     
   # creating a label  
   rename_label = Label(  
      rename_window,  
      text = "Enter the new file name:",  
      font = ("verdana", "8"),  
      bg = "#F6EAD7",  
      fg = "#000000"  
      )  
   # placing the label on the window  
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
   # placing the entry field on the window  
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
   # placing the button on the window  
   submitButton.pack(pady = 2)  
  
# defining a function get the file path  
def getFilePath():  
   # selecting the file using the filedialog's askopenfilename() method  
   the_file = fd.askopenfilename(title = "Select the file to rename", filetypes = [("All files", "*.*")])  
   # returning the file path  
   return the_file  
  
# defining a function that will be called when submit button is clicked  
def submitName():  
   # getting the entered name from the entry field  
   renameName = enteredFileName.get()  
   # setting the entry field to empty string  
   enteredFileName.set("")  
   # calling the getFilePath() function  
   fileName = getFilePath()  
   # creating a new file name for the file  
   newFileName = os.path.join(os.path.dirname(fileName), renameName + os.path.splitext(fileName)[1])  
   # using the rename() method to rename the file  
   os.rename(fileName, newFileName)  
   # using the showinfo() method to display a message box to show the success message  
   mb.showinfo(title = "File Renamed!", message = "The selected file has been renamed.")  
     
# defining a function to open a folder  
def openFolder():  
   # using the filedialog's askdirectory() method to select the folder  
   the_folder = fd.askdirectory(title = "Select Folder to open")  
   # using the startfile() of the os module to open the selected folder  
   os.startfile(the_folder)  
  
# defining a function to delete the folder  
def deleteFolder():  
   # using the filedialog's askdirectory() method to select the folder  
   folderToDelete = fd.askdirectory(title = 'Select Folder to delete')  
   # using the rmdir() method of the os module to delete the selected folder  
   os.rmdir(folderToDelete)  
   # displaying a success message using the showinfo() method  
   mb.showinfo("Folder Deleted!", "The selected folder has been deleted!")  
  
# defining a function to move the folder  
def moveFolder():  
   # using the askdirectory() method to select the folder  
   folderToMove = fd.askdirectory(title = 'Select the folder you want to move')  
   # using the showinfo() method to dislay  
   mb.showinfo(message = 'Folder has been selected to move. Now, select the desired destination.')  
   # using the askdirectory() method to select the destination  
   des = fd.askdirectory(title = 'Destination')  
  
   #using the try-except method  
   try:  
      # using the move() method of the shutil module to move the folder to the requested location  
      shutil.move(folderToMove, des)  
      # displaying the success message using the messagebox's showinfo() method  
      mb.showinfo("Folder moved!", 'The selected folder has been moved to the desired Location')  
   except:  
      # displaying the failure message using the messagebox's showerror() method  
      mb.showerror('Error!', 'The Folder cannot be moved. Make sure that the destination exists')  
  
# defining a function to list all the files available in a folder  
def listFilesInFolder():  
   # declaring a variable with initial value 0  
   i = 0  
   # using the askdirectory() method to select the folder  
   the_folder = fd.askdirectory(title = "Select the Folder")  
   # using the listdir() method to list all the files in the directory  
   the_files = os.listdir(os.path.abspath(the_folder))  
  
   # creating an object of Toplevel class  
   listFilesWindow = Toplevel(win_root)  
   # specifying the title of the pop-up window  
   listFilesWindow.title(f'Files in {the_folder}')  
   # specifying the size and position of the window  
   listFilesWindow.geometry("300x500+300+200")  
   # disabling the resizable option  
   listFilesWindow.resizable(0, 0)  
   # setting the background color of the window to #EC2FB1  
   listFilesWindow.configure(bg = "#EC2FB1")  
  
   # creating a list box  
   the_listbox = Listbox(  
      listFilesWindow,  
      selectbackground = "#F24FBF",  
      font = ("Verdana", "10"),  
      background = "#FFCBEE"  
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
  
   # iterating through the files in the folder  
   while i < len(the_files):  
      # using the insert() method to insert the file details in the list box  
      the_listbox.insert(END, "[" + str(i+1) + "] " + the_files[i])  
      i += 1  
   the_listbox.insert(END, "")  
   the_listbox.insert(END, "Total Files: " + str(len(the_files)))  



def free_space_on_disk():
   root="/"
    
   # ShowDiskUsageWindow = Toplevel(win_root)  
   # # specifying the title of the pop-up window  
   # ShowDiskUsageWindow.title(f'Your Disk Usage')  
   # # specifying the size and position of the window  
   # ShowDiskUsageWindow.geometry("300x500+300+200")  
   # # disabling the resizable option  
   # ShowDiskUsageWindow.resizable(1, 1)  
   # # setting the background color of the window to #EC2FB1  
   # ShowDiskUsageWindow.configure(bg = "#EC2FB1")  
  
   # # creating a list box  
   # the_listbox = Listbox(  
   #    ShowDiskUsageWindow,  
   #    selectbackground = "#F24FBF",  
   #    font = ("Verdana", "10"),  
   #    background = "#FFCBEE"  
   #    )  
   # # placing the list box on the window  
   # the_listbox.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)  
     
   # # creating a scroll bar  
   # the_scrollbar = Scrollbar(  
   #    the_listbox,  
   #    orient = VERTICAL,
   #    command = the_listbox.yview  
   #    )  
   # # placing the scroll bar to the right side of the window  
   # the_scrollbar.pack(side = RIGHT, fill = Y)  
  
   # # setting the yscrollcommand parameter of the listbox's config() method to the scrollbar  
   # the_listbox.config(yscrollcommand = the_scrollbar.set)  

   total,used,free=shutil.disk_usage(root)

   total = total / (2**30)
   used = used / (2**30)
   free = free / (2**30)
   used=total-free

   categories = ['Used Space', 'Free Space']
   sizes = [(used*100.0)/total,(free*100.0)/total]
   # Create the pie chart
   plt.figure(figsize=(6,6))  # Adjust the figure size as needed
   plt.title('Disk Usage')
   plt.pie(sizes, labels=categories,autopct='%1.1f%%', startangle=69)
   plt.show()

   # canvas = FigureCanvasTkAgg(plt.gcf(), master=ShowDiskUsageWindow)
   # canvas.draw()

   # the_listbox.window_create(tk.END, window=canvas.get_tk_widget())

   # the_listbox.insert(END,f"Total : {total} GB")
   # the_listbox.insert(END,f"Used : {used} GB")
   # the_listbox.insert(END,f"Free : {free} GB")



   # total_used = get_size(root)
   # the_listbox.insert(END, f"Total : {total_used / (2**30)} GB")


def show_space_used():

   the_path = fd.askdirectory(title = "Select Folder to check the size of") 

   # folder_space_usage=get_size(str(the_path))

   ret = subprocess.run(["du","-sh",f"{the_path}"],capture_output=True, text=True, check=True)
   ret1=ret.stdout.strip().split('\t')
   ret=ret1[0]
   ret=ret[:-1]
   # print(ret)

   # folder_space_usage = (folder_space_usage / (2**30))
   # print(the_path)
   # print(folder_space_usage / (2**30))

      
   ShowFolderSpaceUsage = Toplevel(win_root)  
   # specifying the title of the pop-up window  
   ShowFolderSpaceUsage.title(f'Usage of {the_path}')  
   # specifying the size and position of the window  
   ShowFolderSpaceUsage.geometry("300x500+300+200")  
   # disabling the resizable option  
   ShowFolderSpaceUsage.resizable(1, 1)  
   # setting the background color of the window to #EC2FB1  
   ShowFolderSpaceUsage.configure(bg = "#EC2FB1")  
  
   # creating a list box  
   the_listbox = Listbox(  
      ShowFolderSpaceUsage,  
      selectbackground = "#F24FBF",  
      font = ("Verdana", "10"),  
      background = "#FFCBEE"  
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

   the_listbox.insert(END,f"Space Utilisation : {ret} GB")


def least_accessed_files():
   the_path = fd.askdirectory(title = "Select folder to check last access of files") 
   ShowLeastAccessedFiles = Toplevel(win_root)  
   # specifying the title of the pop-up window  
   ShowLeastAccessedFiles.title(f'Least Accessed files in {the_path}')  
   # specifying the size and position of the window  
   ShowLeastAccessedFiles.geometry("300x500+300+200")  
   # disabling the resizable option  
   ShowLeastAccessedFiles.resizable(1, 1)  
   # setting the background color of the window to #EC2FB1  
   ShowLeastAccessedFiles.configure(bg = "#EC2FB1")  
  
   tree = ttk.Treeview(ShowLeastAccessedFiles)
   tree["columns"] = ("Column 1", "Column 2", "Column 3")
   # tree.heading("Column 1", text="Index", anchor=tk.W)  # Index column
   # tree.column("Column 1", anchor=tk.W, width=60)
   tree.heading("Column 1", text="File Name")
   tree.column("Column 1", anchor=tk.W, width=200)
   tree.heading("Column 2", text="Date Accessed")
   tree.column("Column 2", anchor=tk.W, width=200)
   tree.heading("Column 3", text="Time Accessed")
   tree.column("Column 3", anchor=tk.W, width=200)
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
         lis.append([f"{file_path}",ret3,f"{ret2[2]}"])

   df = pandas.DataFrame(data=lis,columns=["File Name","Date Modified","Time Modified"])
   # print(df)
   df.sort_values(['Date Modified'],inplace=True)
   # print(df)
   lisn = df.to_numpy().tolist()
   for index, row in enumerate(lisn, start=1):
      tree.insert("", tk.END, values=row)
   # print(lisn)
   tree.pack()

# main function  
if __name__ == "__main__":  
   # creating an object of the Tk() class  
   win_root = Tk()  
   # setting the title of the main window  
   win_root.title("Wizard Of Systems Programming")  
   # set the size and position of the window  
   win_root.geometry("500x600+650+250")  
   # disabling the resizable option  
   win_root.resizable(0, 0)  
   # setting the background color to #D8E9E6  
   win_root.configure(bg = "#D8E9E6")  
  
   # creating the frames using the Frame() widget  
   header_frame = Frame(win_root, bg = "#D8E9E6")  
   buttons_frame = Frame(win_root, bg = "#D8E9E6")  
  
   # using the pack() method to place the frames in the window  
   header_frame.pack(fill = "both")  
   buttons_frame.pack(expand = TRUE, fill = "both")  
  
   # creating a label using the Label() widget  
   header_label = Label(  
      header_frame,  
      text = "File Explorer",  
      font = ("verdana", "16"),  
      bg = "#D8E9E6",  
      fg = "#1A3C37"  
      )  
  
   # using the pack() method to place the label in the window  
   header_label.pack(expand = TRUE, fill = "both", pady = 12)  
  
   # creating the buttons using the Button() widget  
   # open button  
   open_button = Button(  
      buttons_frame,  
      text = "Open a File",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = openFile  
      )  
   
   disk_space_usage = Button(  
      buttons_frame,  
      text = "Check Disk Usage",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = free_space_on_disk  
      )  
  
   show_space_usage = Button(  
      buttons_frame,  
      text = "Check Folder's Space Usage",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = show_space_used 
      )  
   least_access = Button(  
      buttons_frame,  
      text = "Check least accessed files",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = least_accessed_files 
      )  
   
   # copy button  
   copy_button = Button(  
      buttons_frame,  
      text = "Copy a File",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = copyFile  
      )  
  
   # delete button  
   delete_button = Button(  
      buttons_frame,  
      text = "Delete a File",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = deleteFile  
      )  
  
   # rename button  
   rename_button = Button(  
      buttons_frame,  
      text = "Rename a File",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = renameFile  
      )  
  
   # open folder button  
   open_folder_button = Button(  
      buttons_frame,  
      text = "Open a Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = openFolder  
      )  
  
   # delete folder button  
   delete_folder_button = Button(  
      buttons_frame,  
      text = "Delete a Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = deleteFolder  
      )  
  
   # move folder button  
   move_folder_button = Button(  
      buttons_frame,  
      text = "Move a Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = moveFolder  
      )  
  
   # list all files button  
   list_button = Button(  
      buttons_frame,  
      text = "List all files in Folder",  
      font = ("verdana", "10"),  
      width = 18,  
      bg = "#6AD9C7",  
      fg = "#000000",  
      relief = GROOVE,  
      activebackground = "#286F63",  
      activeforeground = "#D0FEF7",  
      command = listFilesInFolder  
      )  
  
   # using the pack() method to place the buttons in the window  
   open_button.pack(pady = 8)  
   copy_button.pack(pady = 8)  
   delete_button.pack(pady = 8)  
   rename_button.pack(pady = 8)  
   open_folder_button.pack(pady = 8)  
   delete_folder_button.pack(pady = 8)  
   move_folder_button.pack(pady = 8)  
   list_button.pack(pady = 8)  
   disk_space_usage.pack(pady=8)
   show_space_usage.pack(pady=8)
   least_access.pack(pady=8)
  
   # creating an object of the StringVar() class  
   enteredFileName = StringVar()  
  
   # running the window  
   win_root.mainloop()  