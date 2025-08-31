#!/usr/bin/env python3
import cryptos
import typer
import filemanaging as fm
import getpass

app = typer.Typer()

# """Simple Password Manager (SPM). Allows you to manage your passwords."""
@app.command()
def init():
    """Create master password"""
    if fm.check_master() == False:
        print("OK, make your own cool password")
        master = getpass.getpass("Enter master password: ")
        cryptos.init_pass(master)
    else:
        print("Master password has been already initialized")
@app.command()
def add(service: str):
    """Add your service """
    if fm.check_master() == False:
        print("Firstly initialized an master password")
        return
    master = getpass.getpass("Enter master password: ")
    if cryptos.get_master(master) is None:
        return
    serv_pass = getpass.getpass("Enter service password: ")
    try:
        cryptos.add_service(master,service,serv_pass)
    except:
        print("Oops, something is gone wrong!")
        return
    print("Service has been successfully added")
@app.command()
def delete(service: str):
    """Delete your service"""
    if fm.check_master() == False:
        print("Firstly initialized an master password")
        return
    master = getpass.getpass("Enter master password: ")
    if cryptos.get_master(master) is None:
        return
    try:
        cryptos.delete_service(master,service)
    except:
        print("Oops, something is gone wrong!")
        return
    print("Service ",service," has been removed")
@app.command()
def get(service: str):
    """Get password for service"""
    if fm.check_master() == False:
        print("Firstly initialized an master password")
        return
    master = getpass.getpass("Enter master password: ")
    if cryptos.get_master(master) is None:
        return
    try:
        cryptos.decrypt_and_CopyAES(master,service)
    except:
        print("Oops, something is gone wrong!")
        return
app()
