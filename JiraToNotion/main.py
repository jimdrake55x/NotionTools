from cli_builder.cli_builder import print_CLI,action_CLI 
import sys

if __name__ == '__main__':
    if len(sys.argv) > 2:
        # Not implemented
        print("Chaining options is not implemented")
    elif len(sys.argv) == 2:
        action_CLI(sys.argv[1])
    else:
        print_CLI()
