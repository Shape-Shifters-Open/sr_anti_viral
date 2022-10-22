'''
protection.py

Matt Riche
2021

Part of sr_anti_viral
Sets up script nodes that run after file load, hoping to delete problematic nodes before they can
deliver their 'payload'
'''

import pymel.core as pm
import os

from . import nodes
from . import scriptjobs

def register_protection_script():
    '''
    register_protection_script()

    Puts a script job meant to delete problem nodes before they run.
    Will execute on the next file open

    usage:
    call with no args.  Meant for safe use inside userSetup.py.
    '''

    print("Registering sr_anti_viral protection script.")

    # Backup userSetup.py
    backup_usersetup()

    # Create a script job that calls the clean-up modules.
    av_job = pm.scriptJob(
        event=['PostSceneRead', 'sr_anti_viral.protection.full_clean()'], pro=True, ro=False
        )

    av_early_job = pm.scriptJob(
        event=['SceneOpened', 'sr_anti_viral.protection.full_clean()'], pro=True, ro=False
        )

    av_reading_job = pm.scriptJob(
        ct=['readingFile', 'sr_anti_viral.protection.full_clean()'], pro=True, ro=False
        )

    # av_aggressive_job = pm.scriptJob(
    #    event=['DagObjectCreated', 'sr_anti_viral.protection.full_clean()'], pro=True, ro=False
    #    )
    
    print (
        "Protective 'post-scene-read' script-job has been added: {}.  Use \"pm.scriptJob( kill={}, force=True)\" to " 
        "remove it if needed.".format(av_job, av_job)
        )

    print (
        "Protective 'scene-opened' script-job has been added: {}.  Use \"pm.scriptJob( kill={}, force=True)\" to " 
        "remove it if needed.".format(av_early_job, av_early_job)
        )

    print (
        "Protective 'pre-scene-read' script-job has been added: {}.  Use \"pm.scriptJob( kill={}, force=True)\" to " 
        "remove it if needed.".format(av_reading_job, av_reading_job)
        )

    return
    

def full_clean():
    '''
    full_clean()

    Run the entire sr_anti_viral suite in one go.
    '''

    print("SR_ANTI_VIRAL is working now-- Messages will be in triplicate for pre-read, during read "
        "and post read.")

    nodes.clean_bad_nodes()
    scriptjobs.clean_jobs()
    scriptjobs.clean_viewport_updates()
    
    return 


def backup_usersetup():
    '''
    Some problematic script nodes overwrite the usersetup.
    This holds onto a copy of it.
    '''

    print("SR_ANTI_VIRAL is backing up your userSetup.py...")

    suspect_lines = [
        "cmds.evalDeferred('leukocyte = vaccine.phage()')",
        "cmds.evalDeferred('leukocyte.occupation()')",
        "import vaccine",
        ]

    for line in suspect_lines:
        line = line.strip()

    us_path = (pm.internalVar(userAppDir=True) + 'scripts/userSetup.py')
    backup_name = (pm.internalVar(userAppDir=True) + 'scripts/backup_userSetup.py')

    print("...SR_ANTI_VIRAL: Opening {}".format(us_path))
    try:
        f = open(us_path, 'r')
        clean_lines = []
    except:
        print("Couldn't open {}".format(us_path))
        pm.error("SR_ANTI_VIRAL critical failure.  It might not be safe to continue working.  See "
        "script editor.")

    print("...SR_ANTI_VIRAL: Reading your usersetup.py line by line...")
    # Read userSetup line by line looking for problem code.
    for line in f:
        if(line.strip() in suspect_lines):
            print(
                "Found a suspicious line in {}...\n{} <-- Linked to a problematic scriptjob.".
                format(us_path, line)
                )
            pm.confirmDialog(
                title='ShaperRigs Anti-Viral', 
                message=("Found a suspicious line in {}; Linked to a problematic scriptjob.".
                    format(us_path, line)), 
                    button=['OK'], 
                    defaultButton='Okay', 
                    dismissString='No' )
        else:
            clean_lines += line
    print("...SR_ANTI_VIRAL: Done reading usersetup.py...")
    f.close()

    try:
        os.remove(us_path)
    except:
        print("SR_ANTI_VIRAL: Couldn't delete old {}".format(us_path))
        pm.error("SR_ANTI_VIRAL critical failure.  It might not be safe to continue working.  See "
        "script editor.")

    try:
        fo = open(us_path, 'w')
    except:
        print("SR_ANTI_VIRAL: Couldn't write new {}".format(us_path))
        pm.error("SR_ANTI_VIRAL critical failure.  It might not be safe to continue working.  See "
        "script editor.")
        

    fo.writelines(clean_lines)

    try:
        fb = open(backup_name, 'w')
    except:
        print("SR_ANTI_VIRAL: Couldn't open backup; {}".format(us_path))
        pm.error("SR_ANTI_VIRAL critical failure.  It might not be safe to continue working.  See "
        "script editor.")
    fb.writelines(clean_lines)

    fo.close()
    fb.close()

    return


def restore_backup_usersetup():
    '''
    Copies the backup_usersetup.py that was stored at the start of the session.
    '''

    print("Loading old usersetup backup...")
    try:
        back_path = (pm.internalVar(userAppDir=True) + 'scripts/backup_userSetup.py')
    except:
        print("There was no backed up usersetup.py.")
        return

    us_path = (pm.internalVar(userAppDir=True) + 'scripts/userSetup.py')
    f = open(back_path, 'r')
    fout = open(us_path, 'w')

    content = f.readlines()
    fout.writelines(content)

    f.close()
    fout.close()

    return
