'''
protection.py
Matt Riche, June 2021 
with Shaper Rigs Team & Burlington Interactive Solutions

Part of sr_anti_viral
Sets up script nodes that run after file load, hoping to delete problematic nodes before they can
deliver their 'payload'
'''

import pymel.core as pm

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

    # Create a script job that calls the clean-up modules.
    av_job = pm.scriptJob(
        ct=['opening', 'sr_anti_viral.protection.full_clean()'], pro=True, ro=True
        )
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
