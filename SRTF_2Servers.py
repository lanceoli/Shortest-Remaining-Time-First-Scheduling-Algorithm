from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = (240,30)
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np

df_list = []
df_list2 = []

arrival = [
    5, 12, 20, 27, 34, 41, 49, 56, 64, 70, 77, 85, 92, 99, 107, 113, 121, 129,
    135, 141, 147, 155, 161, 169, 175, 183, 189, 195, 203, 209, 217, 224, 230,
    238, 245, 253, 260, 268, 274, 280, 288, 296, 302, 309, 315, 322, 328, 335,
    342, 349, 357, 0, 6, 14, 20, 26, 32, 38, 46, 53, 61, 67, 75, 82, 88, 96, 103
]

burst = [
    4, 3, 6, 6, 2, 7, 5, 7, 7, 5, 2, 3, 3, 2, 5, 6, 6, 6, 2, 4, 7, 5, 5, 3, 5,
    4, 3, 7, 3, 4, 2, 7, 2, 5, 5, 6, 4, 2, 6, 4, 5, 2, 2, 5, 2, 3, 6, 7, 5, 2,
    5, 2, 5, 4, 6, 5, 4, 5, 7, 4, 5, 2, 3, 3, 2, 6, 6
]

arr_queue_index = []
burst_queue_index = []  # burstable

queue = []
queue2 = []

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
    if len(queue) <= len(queue2):
      queue.append("P"+str(burst.index(min(burstable_values))+1))
      df_list.append(dict(Task="P"+str(burst.index(min(burstable_values))+1),
                          # Start=len(queue)-1,
                          # End=len(queue)))
                          Start=time,
                          End=time+1))
    # add queue2
    else:
      queue2.append("P"+str(burst.index(min(burstable_values))+1))
      df_list2.append(dict(Task="P"+str(burst.index(min(burstable_values))+1),
                          # Start=len(queue2)-1,
                          # End=len(queue2)))
                          Start=time,
                          End=time+1))

    filter(None, burstable_values)
    burst[burst.index(min(burstable_values))] = (
            burst[burst.index(min(burstable_values))] - 1)

    # print
    # print("Time:", time)
    # print("Queue:", queue)
    # print("Queue2:", queue2)
    # print("Burstable:", burstable_values)

    if burstable_values[len(burstable_values) - 1] == 0:
        burstable_values[len(burstable_values) - 1] = None

# plot timeline
df = pd.DataFrame(df_list, columns=['Task', 'Start', 'End'])
print(df.to_string())

df2 = pd.DataFrame(df_list2, columns=['Task', 'Start', 'End'])
print(df2.to_string())

# merge dataframes
df_merged = df.merge(df2, how='outer')

persons_set = set(name.strip() for names in df_merged['Task'] for name in names.split(","))
persons = {p: i for i, p in enumerate(sorted(persons_set))}

for person in persons:
  periods = []
  for names, start, end in zip(df['Task'], df['Start'], df['End']):
      if person in set(name.strip() for name in names.split(",")):
          periods.append((start, end - start))
  plt.broken_barh(periods, (persons[person], 0.9),
                  facecolors=('tab:blue'))
  
for person in persons:
  periods = []
  for names, start, end in zip(df2['Task'], df2['Start'], df2['End']):
      if person in set(name.strip() for name in names.split(",")):
          periods.append((start, end - start))
  plt.broken_barh(periods, (persons[person], 0.9),
                  facecolors=('tab:green'))

plt.xticks(range(len(queue)*2+1))
plt.yticks(range(len(persons)), persons)
# if len(persons2) > len(persons):
#   plt.yticks(range(len(persons2)), persons2)
plt.xlabel("Time")
plt.ylabel("Jobs")
plt.title("Shortest-Remaining-Time-First Scheduling Algorithm")
plt.legend(loc="upper left")
plt.gca().legend(('server 1','server 2'))
ax = plt.gca()
leg = ax.get_legend()
leg.legendHandles[0].set_color('blue')
leg.legendHandles[1].set_color('green')
plt.gca().invert_yaxis()
plt.show()