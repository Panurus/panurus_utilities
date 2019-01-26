def install_module(module, install = True, conda_or_pip = "pip", print_terminal = True, verbose = False):
    """Allows installation of a module directly from a notebook or script.
    Improves reproducibility of scripting/ notebook usage, where installed modules may differ between users.
        
    Arguments:
        module -- string. The name of the module intended to be installed.
        install -- bool. Install the module (True) or check if already installed (False)
        conda_or_pip -- string. Only required if install = True. Must be either 'conda' or 'pip'.
        print_terminal -- bool. Print the terminal output resulting from installing module, or not.
                                If verbose = False, print_terminal is overridden.
        
    Returns:
        "True" if module is available for import, "False" if not.
    """
    
    # Import libraries:
    # importlib.import_module to allow import via a string argument.
    # subprocess.getstatusoutput to allow printing of terminal output and to check zero or non-zero exit status.
    # logging for... yep, logging
    from importlib import import_module as im
    from subprocess import getstatusoutput as sub
    import logging
    
    # Set inital state for progress and success/failure messaging.
    state = 0
    
    # Set out to default, in case no terminal output to display
    out = {
        1:"No terminal output to display"
    }
    
    # Create inverse of pip or conda for messaging
    if conda_or_pip == "conda":
        inv_conda_or_pip = "pip"
    elif conda_or_pip == "pip":
        inv_conda_or_pip = "conda"
    
    # Check whether module is available for import and adjust messaging state
    try:
        im(module)
    except(ImportError):
        state = 1
        if install == True:
            assert conda_or_pip in ["conda","pip"], 'the attribute conda_or_pip needs to be one of "conda" or "pip"'
            if verbose:
                print(module, "not installed")
                print("automatically installing", module, "using", conda_or_pip, "...please wait.")
                
            # Install module using conda
            if conda_or_pip == "conda":
                out = sub("conda install " + module + " -y")
                
            # Install module using pip
            elif conda_or_pip == "pip":
                out = sub("pip install " + module)
                
            # If non-zero exit, adjust state
            if out[0] != 0:
                state = 2
                
            # If zero exit, reset state
            if out[0] == 0:
                state = 0
                
            # If module still can't be imported, adjust state
                try:
                    im(module)
                except(ImportError):
                    state = 3
    
    # Messaging based on state
    if state == 0:
        if verbose:
             print(module 
                   + " is installed and available for import.")
    elif state == 1:
        logging.error(module 
                      + " not installed. Please install using pip or conda before importing. \n"
                      +"(Run this function again with the 'conda_or_pip' attribute set to either 'conda' or 'pip' and 'install' set to 'True').")
    elif state == 2:
        logging.error(module 
                        + " could not be installed using " 
                        + conda_or_pip 
                        + ". Try using " 
                        + inv_conda_or_pip 
                        + ". If both fail, check module spelling.")
    elif state == 3:
        logging.error(module 
                        + " is installed but not importable. Install using " 
                        + inv_conda_or_pip 
                        + " and try again.")
    
    # Print terminal output
    if verbose:
        if print_terminal:
            print("-"*18 + "\n Terminal output \n" + "-"*18)
            print(out[1])

    # Set exit status
        if state == 0:
            return True
        else:
            return False

def get_zipped_repo(repozip, destination, zipped, unzipped):
    """
    Retrieves and unzips a github repository.
    
        Arguments:
    repozip -- string. URL of the repo zip file.
    destination -- string. Local file path to download the zip file to.
    zipped --  string. The name to be attributed to the zipfile locally.
    unzipped -- string. The name to be attributed to the unzipped file.   
    """
    
    import os
    import urllib.request
    import zipfile
    import re
    
    zipped = destination+zipped
    unzipped = destination+unzipped
    
    if os.path.exists(destination):
        print("Stage 1 of 2: local repository directory exists")
    else:
        print("Stage 1 of 2: creating local repository directory")
        os.makedirs(destination)
    
    if all([not os.path.exists(unzipped), not os.path.isfile(zipped)]):
        print("Stage 2 of 2: downloading repository zip file, unzipping and removing zip file")
        urllib.request.urlretrieve(repozip, zipped)
        with zipfile.ZipFile(zipped, "r") as zippy:
            internal_file_name = destination + re.split("/", re.sub("<ZipInfo filename='","", str(zippy.filelist[0])))[0]
            zippy.extractall(destination)
            os.rename(internal_file_name, unzipped)
            os.remove(zipped)
            print("done")
    elif os.path.isfile(zipped) and os.path.exists(unzipped):
        print("Stage 2 of 2: repository zip file exists and is unzipped, removing zip file")
        os.remove(zipped)
        print("done")
    elif os.path.isfile(zipped):
        print("Stage 2 of 2: repository zip file exists, unzipping and removing zip file")
        with zipfile.ZipFile(zipped, "r") as zippy:
            internal_file_name = destination + re.split("/", re.sub("<ZipInfo filename='","", str(zippy.filelist[0])))[0]
            zippy.extractall(destination)
            os.rename(internal_file_name, unzipped)
            os.remove(zipped)
            print("done")
    elif os.path.exists(unzipped):
        print("Stage 2 of 2: model repository already unzipped")
        print("done")
		
		
def append_mod_to_sys(locs):
    """
    Appends module directory/directories to sys.path
        Arguments:
    -- locs: string or list of strings. The absolute filepath/s to the module to be imported.
    """
    
    import sys
    import os
    
    if type(locs) != list:
        locs = [locs]
    for i in range(0, len(locs)):
        b = list(range(0,len(sys.path)))
        for j in b:
            if(sys.path[j] == locs[i]):
                b[j] = True
            else:
                b[j] = False
        if(any(b)):
            print(locs[i] + ' is already on sys.path')
        else:
            sys.path.append(locs[i])
            print(locs[i] + ' added to sys.path. This will be removed once this notebook has been shutdown.')
    
    return None