# done in 2 stages - dt and then ws entries

from connection import initialize_connection


wsh = initialize_connection()

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and \
            int(arr[j][0].split('-', 1)[1]) > int(key[0].split('-', 1)[1]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

if __name__ == "__main__":
    data = []
    print(type(data))
    # change rows to update - here from 75 to 116 (incl)
    for i in range(75, 117):
        data.append(wsh.get_row(i))
    
    insertion_sort(data)
    # change cell to start updating from - here A75
    wsh.update_values('A75', data)