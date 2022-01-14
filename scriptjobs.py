'''
scriptjobs.py

Matt Riche
2021

Module for reading the scriptjobs active and identifying ones you want removed before they run.
'''

import pymel.core as pm


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