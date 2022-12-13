gasse_2019_scip_params = {
    'separating/maxrounds': 0,    # separate (cut) only at root node
    'presolving/maxrestarts': 0,  # disable solver restarts
    'limits/time': 60 * 60,       # solver time limit
    'timing/clocktype': 1,        # 1: CPU user seconds, 2: wall clock time
    # 'limits/gap': 3e-4,         # 0.03% relative primal-dual gap (default: 0.0)
    # 'limits/nodes': -1,
}