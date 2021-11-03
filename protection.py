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

import nodes
import scriptjobs

def register_protection_script():
    '''
    register_protection_script()

    Puts a script job meant to delete problem nodes before they run.
    Will execute on the next file open

    usage:
    call with no args.  Meant for safe use inside userSetup.py.
    '''

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
        "Protective script-job has been added: {}.  Use \"pm.scriptJob( kill={}, force=True)\" to " 
        "remove it if needed.".format(av_job, av_job)
        )


def full_clean():
    '''
    full_clean()

    Run the entire sr_anti_viral suite in one go.
    '''

    nodes.clean_bad_nodes()
    scriptjobs.clean_jobs()
    return    


def backup_usersetup():
    '''
    Some problematic script nodes overwrite the usersetup.
    This holds onto a copy of it.
    '''

    suspect_lines = [
        "cmds.evalDeferred('leukocyte = vaccine.phage()')",
        "cmds.evalDeferred('leukocyte.occupation()')",
        "import vaccine",
        ]

    for line in suspect_lines:
        line = line.strip()

    us_path = (pm.internalVar(userAppDir=True) + 'scripts/userSetup.py')
    backup_name = (pm.internalVar(userAppDir=True) + 'scripts/backup_userSetup.py')

    f = open(us_path, 'r')
    clean_lines = []

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

    f.close()

    os.remove(us_path)
    fo = open(us_path, 'w')
    fo.writelines(clean_lines)
    fb = open(backup_name, 'w')
    fb.writelines(clean_lines)

    fo.close()
    fb.close()

    return


def restore_backup_usersetup():
    '''
    Copies the backup_usersetup.py that was stored at the start of the session.
    '''

    try:
        print("Loading old usersetup backup...")
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