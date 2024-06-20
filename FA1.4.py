from matplotlib import pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df_list = []

arrival = [2, 1, 4, 6, 0]
burst = [5, 1, 3, 4, 7]

arr_queue_index = []
burst_queue_index = []  # burstable

queue = []

for time in range(sum(burst)):

    for i in range(len(arrival)):
        if time == arrival[i]:
            arr_queue_index.append(i)
            burst_queue_index.append(i)

    # create burstable_values list
    burstable_values = []
    for i in range(len(burst_queue_index)):
        if burst[burst_queue_index[i]] == 0:
            continue
        burstable_values.append(burst[burst_queue_index[i]])

    # add queue
    queue.append("P"+str(burst.index(min(burstable_values))+1))
    df_list.append(dict(Task="P"+str(burst.index(min(burstable_values))+1),
                        Start=len(queue)-1,
                        End=len(queue)))

    filter(None, burstable_values)
    burst[burst.index(min(burstable_values))] = (
            burst[burst.index(min(burstable_values))] - 1)

    # print
    print("Time:", time)
    print("Queue:", queue)

    if burstable_values[len(burstable_values) - 1] == 0:
        burstable_values[len(burstable_values) - 1] = None

# plot timeline
df = pd.DataFrame(df_list, columns=['Task', 'Start', 'End'])
print(df)

persons_set = set(name.strip() for names in df['Task'] for name in names.split(","))
persons = {p: i for i, p in enumerate(sorted(persons_set))}

for person in persons:
    periods = []
    for names, start, end in zip(df['Task'], df['Start'], df['End']):
        if person in set(name.strip() for name in names.split(",")):
            periods.append((start, end - start))
    plt.broken_barh(periods, (persons[person] - 0.45, 0.9),
                    facecolors=plt.cm.plasma(persons[person] / len(persons)))

plt.xticks(range(len(queue)+1))
plt.yticks(range(len(persons)), persons)
plt.xlabel("Time")
plt.ylabel("Jobs")
plt.title("Shortest-Remaining-Time-First Scheduling Algorithm")
plt.gca().invert_yaxis()
plt.show()