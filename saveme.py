import click
import pyfiglet
import shutil
import zipfile
import ruamel.std.zipfile as zf
import requests
import hashlib
import platform
import os
from getpass import getpass

@click.command(options_metavar = "<options>")
@click.option("-u","--username","username", help="username of a registered user", metavar="<string>")
@click.option("-f","--file","path", help="name of the zip containing files to be saved", metavar="<string>")
#@click.option("-n","--name","final_name", help="name for the final output final",metavar="<string>")
@click.option("-r","--register","register", is_flag=True, help="new user registration")
@click.option("-l","--list","list_files",is_flag=True, help="List all the files from the cloud")
@click.option("-s","--save","save", help="name of the file to be downloaded")
@click.option("-da","--deleteall","delall",is_flag=True,help="empty the cloud directory")
@click.option("-d", "--delete","delete", help="name of the file to be deleted", metavar="<string>")
def saveme(username, path,register, list_files, save, delete, delall):
    #greeting default text
    """
    Commands: 

    saveme [-u user] [-f filename]\n
    saveme [-u user] -l\n
    saveme [-u user] [-s filename]\n
    saveme -r\n
    saveme [-u user] [-d filename]\n
    saveme [-u user] -da\n
    """
    #some error checks for command line options
    if(username == None and path == None and register== False and list_files == False and save == None and delete == None and delall == False) :
        header = pyfiglet.figlet_format("SAVE ME", font = "slant") 
        description = """~~~ version 1.0.0
        \n~~~ \'Save me\' is a simple command line application for instantly saving your work files to an allocated cloud space. \n\n~~~ For more details on how to use saveme, try :\n\n    saveme --help\n\n~~~ For details on it's working, visit:  https://github.com/AthN3090/save-me\n"""
        click.echo(header)
        click.echo(description)
    elif(register == True):
        if(username == None and path == None  and list_files == False and save == None and delete == None and delall == False):
            add_user()
        else:
            quit("Invalid expression")
             #registering new user 
    elif(list_files == True):
        if(username != None and path == None  and register== False and save == None and delete == None and delall == False):
            display_files(username)
        else:
            quit("Invalid Expression")
    elif(save != None):
        if(username != None and path == None  and register== False and list_files == False and delete == None and delall == False):
            save_files(username, save)
        else:
            quit("Invalid Expression")
    elif(delete != None):
        if(username != None and path == None  and register== False and list_files == False and save == None and delall == False):
            delete_file(username, delete)
        else:
            quit("Invalid Expression")
    elif(delall == True):
        if(username != None and path == None  and register== False and list_files == False and save == None and delete == None):
            empty(username)
        else:
            quit("Invalid Expression")
    elif(username != None and path != None and register== False and list_files == False and save == None and delete == None and delall == False):
        upload_files(username, path)
        """try:
            shutil.make_archive(final_name, 'zip', path)
        except:
            quit("\nError => "+ path + " is not a directory")

        final_final_name = final_name + ".zip"
        file = zipfile.ZipFile(final_final_name,"r")
        for name in file.namelist():
            if(name ==final_final_name):
                zf.delete_from_zip_file(final_final_name,file_names=[final_name+".zip"])
        upload_files(username, final_final_name)
    else:
        quit("Invalid Expression")"""
    
        
        """if(error):
            quit()
        else: #the main application logic goes here 
            try:
                shutil.make_archive(final_name, 'zip', path)
            except:
                quit("\nError => "+ path + " is not a directory")
            final_final_name = final_name + ".zip"
            file = zipfile.ZipFile(final_final_name,"r")
            for name in file.namelist():
                if(name ==final_final_name):
                    zf.delete_from_zip_file(final_final_name,file_names=[final_name+".zip"])
            if(username != None):
                upload_files(username, final_final_name)"""

def upload_files(username, file_name):
    response = authentication(username)
    if(response == "GOOD"):
        try:
            file = open(file_name, 'rb')
        except IsADirectoryError:
            click.echo("The given path '" + file_name + "' is a directory ! it needs to be file !")
        else:
            r = requests.post("https://saveme-athn3090.herokuapp.com/upload",data = { 'username' : username}, files = { 'file' :file } )
            click.echo(r.text)
    elif(response == "BAD"):
        click.echo("\n Error => Bad credentials")


    #r = requests.post("https://saveme-athn3090.herokuapp.com/upload",data = { 'username' : username}, files = { 'file':file } )
#def add_user():
#    click.echo("registered")
#    quit()

def display_files(username):
    response = authentication(username)
    if(response == "GOOD"):
        r = requests.post("https://saveme-athn3090.herokuapp.com/listfiles",data = { 'username' : username})
        response = r.json()
        files = response['files']
        click.echo("Your files : \n")
        count = 0 
        for file in files :
            count+=1
            click.echo(str(count) + ". " + file.replace(username+ "/", ""))
        click.echo("\nTotal files => " + str(count))    
        quit()
    elif(response == "BAD"):
        quit("\n ERROR => Bad credentials !")

def save_files(username, filename):
    response = authentication(username)
    if(response == "GOOD"):
        r = requests.post("https://saveme-athn3090.herokuapp.com/download",data = { 'username' : username, 'filename' : filename}, stream = True)
        if(r.status_code == 404):
            click.echo("\n ERROR => Check if the file you want to download actually exist on your cloud storage ! \n Try listing your files : saveme -u [username] -l \n")
            quit()
        with open("./" + filename, 'wb') as out_file:
            out_file.write(r.content)
        click.echo("Download Complete !")    
        quit()
            
    elif(response == 'BAD'):
        click.echo('\n Error => Bad credentials !')
        quit()


def authentication(username):
    input_pass = getpass('Password :')
    encrypt_pass = md5(input_pass)
    r = requests.post("https://saveme-athn3090.herokuapp.com/authenticate", data = {'username': username, 'password' : encrypt_pass })
    return r.text


def add_user():
    click.echo('Creating new user : \n')
    username = input('Enter a username :')
    password = getpass('Create password :')
    cpassword = getpass('Confirm password:')
    if(password == cpassword):
        encrypt_pass = md5(password)
        r = requests.post("https://saveme-athn3090.herokuapp.com/register", data = {'username': username, 'password' : encrypt_pass, 'os' : platform.system()})

        if(r.text == 'SUCCESS'):
            click.echo('\nUser registeration successfull')
        elif(r.text == "FAIL"):
            click.echo("\nUser already exist")
    else:
        click.echo('Passwords doesn\'t match ')

def md5(password):
    encrypt_pass = hashlib.md5(password.encode())
    return encrypt_pass.hexdigest()

def delete_file(username, filename):
    response = authentication(username)
    if(response == "GOOD"):
        r = requests.post("https://saveme-athn3090.herokuapp.com/delete",data = { 'username' : username, 'filename' : filename})
        if(r.status_code == 404):
            click.echo("ERROR => No such file '"+ filename+ "' in your cloud storage")
            quit()
        else:
            click.echo(r.text)
            quit()
    elif(response == 'BAD'):
        click.echo('\n ERROR => Bad credentials !')
        quit()

def empty(username):
    response = authentication(username)
    if(response == "GOOD"):
        r = requests.post("https://saveme-athn3090.herokuapp.com/empty",data = { 'username' : username})
        click.echo(r.text)
        quit()
    elif(response == 'BAD'):
        click.echo('\n ERROR => Bad credentials !')
        quit()
