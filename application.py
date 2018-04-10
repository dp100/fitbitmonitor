# -*- coding: utf-8 -*-
import dashGraph, sys
from vaultClient import *

inputs = sys.argv[1:]
# inputs are:
#   user, pass

dG = dashGraph.dashGraph()

if __name__ == '__main__':
    dG.app.run_server(debug=True, host='0.0.0.0')
