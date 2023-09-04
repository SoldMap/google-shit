import argparse
from editor import new_build, new_rebuild, new_deploy, new_move

'''
#################### 4 SEPARATE CMDLINE PARSERS #####################
1. BUILD
2. REBUILD
3. DEPLOY
4. MOVE
'''

def main(command_line=None):
    parser = argparse.ArgumentParser(description="Create/delete/move entries \
    in the Workstations worksheet")
    subparsers = parser.add_subparsers(dest="command", \
        help="DISPLAY HELP FOR A SUB-COMMAND")


    ### BUILD ####
    b_parser = subparsers.add_parser("build", help="To add a new entry \
        after completing new build")
    b_parser.add_argument("machine", help="specify the machine name: 'dt-NN'")
    b_parser.add_argument("asset", help="specify the asset tag")


    ### REBUILD ###
    r_parser = subparsers.add_parser("rebuild", help="Rebuild the older \
        machines, usually as 'dt-NN'")
    r_parser.add_argument("old", help="old name of the machine")
    r_parser.add_argument("new", help="new name of the machine")


    ### DEPLOY ###
    d_parser = subparsers.add_parser("deploy", help="Move machine from spares \
        to the the users section")
    d_parser.add_argument("machine", help="Machine to be moved to users")
    d_parser.add_argument("user", help="Username to attach to machine")
    d_parser.add_argument("location", help="Location to attach machine to")


    ### MOVE ###
    m_parser = subparsers.add_parser("move", help="move machine, update \
        location and a user")
    m_parser.add_argument("machine", help="Machine to be moved")
    m_parser.add_argument("user", help="Update user")
    m_parser.add_argument("location", help="Update location")
    
    ### INTERACTIVE ###
    interactive_parser = subparsers.add_parser("i", help="interactive mode")
    
    args = parser.parse_args()
    
    
    ################### ROUTER ###################
    
    if args.command == 'build':
        print(f"Adding machine '{args.machine}' with \
the asset tag '{args.asset}'")
        new_build(args.machine, args.asset)
        
    elif args.command == 'rebuild':
        print(f"Changing machine name '{args.old}' to '{args.new}'")
        new_rebuild(args.old, args.new)
        
    elif args.command == 'deploy':
        print(f"Deploying machine '{args.machine}. For \
'{args.user}' on the '{args.location}' location")
        new_deploy(args.machine, args.user, args.location)
    
    elif args.command == 'move':
        print(f"Moving machine... Updating user '{args.user}'... \
            Updating location '{args.location}'")
        new_move(args.machine, args.user, args.location)


if __name__ == '__main__':
    main()



