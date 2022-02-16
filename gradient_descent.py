from asyncio.windows_events import NULL
import auxiliary as aux

def gradient_descent():
    df = aux.import_data_fifa(110)
    curr_sol = aux.get_random_solution(df)

    print('Starting')
    print(curr_sol)
    print(aux.get_std(df, curr_sol))

    while(True):
        curr_std = aux.get_std(df, curr_sol)

        best_std = curr_std
        best_sol = curr_sol

        neighborhood = aux.get_neighborhood(curr_sol)
        for neighbor_sol in neighborhood:
            neighbor_std = aux.get_std(df, curr_sol)
            if neighbor_std[0] < best_std[0]:
                best_std = neighbor_std
                best_sol = neighbor_sol

        if best_sol == curr_sol:
            break

        curr_sol = best_sol           

    print('DONE')
    print(curr_sol)
    print(aux.get_std(df, curr_sol))

gradient_descent()