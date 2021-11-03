'''
nodes.py

Part of sr_anti_viral

Find problematic script nodes in the scene and eliminate them.
Using pre-defined names.
'''

import pymel.core as pm
import os

import protection

# We may want to pull the names of nodes from a file at some point.  Some regular text-file that
# artists can quickly edit.


def clean_bad_nodes():
    '''
    Check all nodes in the scene looking for targets.

    Was considering checking only for scriptNodes, but sometimes "unknown nodes" could be 
    responsible.
    '''

    # hard code node names:
    targets = ['vaccine_gene', 'breed_gene']

    nodes_to_scan = pm.ls(type='script')
    for name in targets:
        print (name)

    count = 0
    for node in nodes_to_scan:
        if(node.name() in targets):
            print(
                "Deleted \"{}\", a {} node known to cause issues.".format(node.name(), node.type())
                )

            pm.confirmDialog(
                title='ShaperRigs Anti-Viral', 
                message=("Deleted \"{}\", a {} node known to cause issues."
                    .format(node.name(), node.type())), 
                    button=['OK'], 
                    defaultButton='Okay', 
                    dismissString='No' )
            count += 1
            pm.delete(node)

        if(node.name() == 'vaccine_gene'):
            # Special procedure for vaccine.py
            vaccine_path = pm.internalVar(userAppDir=True) + 'scripts/vaccine.py'
            os.system('del {}'.format(vaccine_path))
            os.system('type nul > {}'.format(vaccine_path))
            os.remove(vaccine_path)

            protection.backup_usersetup()

    if(count > 0):
        pm.warning(
            "Deleted {} problematic nodes from this scene.  Check script editor for details.".format(
                count
                )
            )

