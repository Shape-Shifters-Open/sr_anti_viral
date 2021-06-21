'''
nodes.py

Part of sr_anti_viral

Find problematic script nodes in the scene and eliminate them.
Using pre-defined names.
'''

import pymel.core as pm

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

    print ("sr_anti_viral is looking for 'viral' script-nodes and other bad things...")
    nodes_to_scan = pm.ls(type='script')

    print ("Looking for the presence of...")
    for name in targets:
        print (name)

    count = 0
    for node in nodes_to_scan:
        if(node.name() in targets):
            print(
                "Deleted \"{}\", a {} node known to cause issues.".format(node.name(), node.type())
                )
            count += 1
            pm.delete(node)

    if(count > 0):
        pm.warning(
            "Deleted {} problematic nodes from this scene.  Check script editor for details.".format(
                count
                )
            )
    else:
        print (
            "sr_anti_viral found nothing strange in this file. (From a list of {} known problem "
            "nodes.)".format(len(targets))
            )

