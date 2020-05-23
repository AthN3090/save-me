import click
import pyfiglet
import shutil
import zipfile
import ruamel.std.zipfile as zf
import pyrebase
import getpass

@click.command()
@click.option("-u","--username","username")
@click.option("-p","--path")
@click.option("-n","--name","zip_name")
def saveme(username, path, zip_name):
    #greeting default text
    error = False
    #some error checks for command line options
    if(username == None and path == None and zip_name == None):
        header = pyfiglet.figlet_format("SAVE ME", font = "isometric1") 
        description = "\n~~ Save me is a simple command line tool for instantly saving your work files to your cloud space ~~\n"
        description = "\n~~ Save me is a simple command line tool for instantly saving your work files to your cloud space ~~\n"
        click.echo(header)
        click.echo(description)
        error=True
    else:
        i = None
        for i in locals():
            if(locals()[i] == None):
                error=True
                click.echo("Invalid expression: " + i + " missing !")
    if(error):
        quit()
    else: #the main application logic goes here 
        shutil.make_archive(zip_name, 'zip', path)
        final_zip_name = zip_name + ".zip"
        file = zipfile.ZipFile(final_zip_name,"r")
        for name in file.namelist():
            if(name ==final_zip_name):
                zf.delete_from_zip_file(final_zip_name,file_names=[zip_name+".zip"])
        if(username != None):
            saveZip(username, final_zip_name)


#firebase setup
config = {
    "apiKey": "AIzaSyC-B3B9VbF-HHhJly2Djr_hsz-3FZV1BfY",
    "authDomain": "save-me-athn.firebaseapp.com",
    "databaseURL": "https://save-me-athn.firebaseio.com",
    "projectId": "save-me-athn",
    "storageBucket": "save-me-athn.appspot.com",
    "messagingSenderId": "433694545774",
    "appId": "1:433694545774:web:4ae188c2a5e13e6a9b137f",
    "measurementId": "G-41VG0D0BKE"

}


def saveZip(email, zip_atachment):
    firebase = pyrebase.initialize_app(config)
    password = getpass.getpass("Enter password :")
    auth = firebase.auth()
    try:
        user = auth.sign_in_with_email_and_password(email,password)
    except:
        click.echo("Invalid Password !  ")
    else:
        storage  = firebase.storage()
        path_on_cloud = email+"/"+zip_atachment       
        path_on_local = zip_atachment       
        storage.child(path_on_cloud).put(path_on_local,user['idToken'])

