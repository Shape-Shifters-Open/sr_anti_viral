'''
scriptjobs.py

Matt Riche
2021

Module for reading the scriptjobs active and identifying ones you want removed before they run.
'''

import pymel.core as pm
import re


def clean_viewport_updates(targets=[r'DCF_updateViewportList;']):
    '''
    clean_viewport_updates
    '''

    must_restart = False
    # First we acquire the common configuration node:
    if pm.objectExists("uiConfigurationScriptNode"):

        node = pm.PyNode("uiConfigurationScriptNode")
        print("Working on the node {}".format(node))

        bs_content = pm.scriptNode(node, q=True, bs=True)

        for target in targets:
            if(target in bs_content):
                cleaned_content = re.sub((target), '', bs_content)
                pm.scriptNode(node, e=True, bs=cleaned_content)
                pm.scriptNode(node, eb=True)
                must_restart = True

        if(must_restart):    
            pm.confirmDialog(
                title='ShaperRigs Anti-Viral', 
                message=("Found a problem in uiConfigurationScriptNode: \"DCF_updateViewportList\".\n"
                "This can create serious issues with the viewport in this session.  This file has" 
                "been cleaned, and you may save an iteration now.  This session however should"
                "be restarted immediately after saving."), 
                    button=['OK'], 
                    defaultButton='Okay', 
                    dismissString='No' )
    
    return



def clean_jobs(targets=['breed_gene']):
    '''
    clean_jobs

    Checks a list of all active scriptJobs looking for ones listed in the block file.

    usage:
    clean_jobs(targets=target_list)
    target_list - type:list - list of strings that are distinct tokens found in bad script-jobs.
    '''

    # Add reading of the block file later, for now we are hard coding what we are looking for.

    print("SR_ANTIVIRAL is looking for known problem script jobs...")

    jobs = pm.scriptJob(lj=True)

    count = 0

    for job in jobs:
        for target in targets:
            if(target in job):
                # We found an example, get the number.
                print("Found this suspicious script-job:")
                print('\"{}\"'.format(job))
                job_number = int(job.split(':')[0])
                # Kill the job by number...
                pm.scriptJob(kill=job_number, force=True)
                print ("Job {} deleted from stack.".format(job_number))
                count += 0

    if(count > 0):
        pm.warning("Deleted {} suspicious script-jobs.".format(count))
    else:
        print("...SR_ANTI_VIRAL found no suspicious script jobs...")

    return