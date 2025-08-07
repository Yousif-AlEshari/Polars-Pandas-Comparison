import matplotlib.pyplot as plt
import numpy as np
import Polars_profiling
import Pandas_profiling
if __name__ == "__main__":

    files = [
        r"synthetic_bank_transactions-6.parquet",
        r"synthetic_bank_transactions-5.parquet",
        r"synthetic_bank_transactions-4.parquet"
       # r"combined.parquet"
    ]

    sizes = ["10k","500k", "2.5m"]#, "10m"]

    polars_results=[]
    pandas_results=[]

    for f in files:
        polars_results.append({
            "filter": Polars_profiling.filtering(f),
            "groupby": Polars_profiling.groupby(f),
            "window": Polars_profiling.window(f)
        })
        pandas_results.append({
            "filter": Pandas_profiling.filtering_method(f),
            "groupby": Pandas_profiling.groupby_method(f),
            "window": Pandas_profiling.window_method(f)
        })


    # Plot runtime comparison
    filter_times_polars = [r["filter"]["runtime"] for r in polars_results]
    filter_times_pandas = [r["filter"]["runtime"] for r in pandas_results]
    group_times_polars  = [r["groupby"]["runtime"] for r in polars_results]
    group_times_pandas  = [r["groupby"]["runtime"] for r in pandas_results]
    window_times_polars = [r["window"]["runtime"] for r in polars_results]
    window_times_pandas = [r["window"]["runtime"] for r in pandas_results]

    x = np.arange(len(sizes))
    width = 0.12

    fig, ax = plt.subplots(figsize=(8,6))
    ax.bar(x - width/2, filter_times_polars, width, label="Polars Filter", color="#1f77b4")
    ax.bar(x + width/2, filter_times_pandas, width, label="Pandas Filter", color="#ff7f0e")
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_ylabel("Runtime (s)")
    ax.set_title("Filter Runtime: Polars vs Pandas")
    ax.legend()
    plt.tight_layout()
    plt.show()



    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, group_times_polars, width, label="Polars GroupBy", color="#2ca02c")
    ax.bar(x + width/2, group_times_pandas, width, label="Pandas GroupBy", color="#d62728")
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_ylabel("Runtime (s)")
    ax.set_title("GroupBy Runtime: Polars vs Pandas")
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, window_times_polars, width, label="Polars Window", color="pink")
    ax.bar(x + width/2, window_times_pandas, width, label="Pandas Window", color="#27bcd6")
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_ylabel("Runtime (s)")
    ax.set_title("Rolling Window Runtime: Polars vs Pandas")
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()



# ----------------------------
# ✅ Memory Usage Processing
# ----------------------------
def extract_memory(samples):
    """Extract Initial, Max, Final from memory usage list"""
    if not samples or len(samples) < 3:
        return [0, 0, 0]
    return [samples[0], max(samples), samples[-1]]

# Collect memory stats
polars_filter_mem = [extract_memory(r["filter"]["memory"]) for r in polars_results]
pandas_filter_mem = [extract_memory(r["filter"]["memory"]) for r in pandas_results]
polars_group_mem  = [extract_memory(r["groupby"]["memory"]) for r in polars_results]
pandas_group_mem  = [extract_memory(r["groupby"]["memory"]) for r in pandas_results]
polars_window_mem = [extract_memory(r["window"]["memory"]) for r in polars_results]
pandas_window_mem = [extract_memory(r["window"]["memory"]) for r in pandas_results]

# Labels
mem_labels = ["Initial", "Max", "Final"]
x = np.arange(len(mem_labels))
width = 0.12  # bar width


# Plot memory usage
# ----------------------------
for i, size in enumerate(sizes):
    fig, ax = plt.subplots(figsize=(10, 6))

    bars_data = [
        (-1.5*width, polars_filter_mem[i], '#1f77b4', 'Polars - Filter'),
        (1.5*width, pandas_filter_mem[i], '#ff7f0e', 'Pandas - Filter'),
        (-0.5*width, polars_group_mem[i], '#2ca02c', 'Polars - GroupBy'),
        (2.5*width, pandas_group_mem[i], "red", 'Pandas - GroupBy'),
        (0.5*width, polars_window_mem[i], 'pink', "Polars - Window"),
        (3.5*width, pandas_window_mem[i], '#27bcd6', "Pandas - Window")
    ]
    
    for offset, values, color, label in bars_data:
        bars = ax.bar(x + offset, values, width, label=label, color=color)
        for j, val in enumerate(values):
            ax.text(x[j] + offset, val + 1, f'{val:.1f}', ha='center', va='bottom', fontsize=8)
    
    ax.set_ylabel("Memory Usage (MB)")
    ax.set_title(f"Memory Usage (Polars vs Pandas) - File Size: {size}")
    ax.set_xticks(x)
    ax.set_xticklabels(mem_labels)
    ax.legend()
    plt.tight_layout()
    plt.show()


# CPU Utilization Line Charts
# ----------------------------
import matplotlib.pyplot as plt
import numpy as np

for i, size in enumerate(sizes):
    polars_filter_cpu = polars_results[i]["filter"]["cpu"]
    pandas_filter_cpu = pandas_results[i]["filter"]["cpu"]
    polars_group_cpu  = polars_results[i]["groupby"]["cpu"]
    pandas_group_cpu  = pandas_results[i]["groupby"]["cpu"]
    polars_window_cpu = polars_results[i]["window"]["cpu"]
    pandas_window_cpu = pandas_results[i]["window"]["cpu"]

    ticks_filter = list(range(len(polars_filter_cpu)))
    ticks_group  = list(range(len(polars_group_cpu)))
    ticks_window = list(range(len(polars_window_cpu)))

    plt.figure(figsize=(12, 6))
    plt.plot(ticks_group, polars_group_cpu, label='Polars - GroupBy', color='#2ca02c', linestyle='-')
    plt.plot(ticks_group, pandas_group_cpu, label='Pandas - GroupBy', color='#d62728', linestyle='--')
    plt.plot(ticks_filter, polars_filter_cpu, label='Polars - Filter', color='#1f77b4', linestyle='-')
    plt.plot(ticks_filter, pandas_filter_cpu, label='Pandas - Filter', color='#ff7f0e', linestyle='--')
    plt.plot(ticks_window, polars_window_cpu, label="Polars - Window", color = 'pink', linestyle='-')
    plt.plot(ticks_window, pandas_window_cpu, label="Pandas - Window", color="#27bcd6", linestyle="--")


    plt.title(f'CPU Utilization Over Time (Filtering & GroupBy) - File Size: {size}')
    plt.xlabel('Time Tick (~0.02s each)')
    plt.ylabel('CPU Usage (%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

#def old_method():
    # polars_aggregation = polars_filtering = Polars_profiling.filtering()
    # pandas_aggregation = pandas_filtering = Pandas_profiling.filtering_method()

    # polars_memory_filtering=polars_filtering['memory']
    # pandas_memory_filtering=pandas_filtering['memory']

    # polars_memory_groupby=polars_aggregation['memory']
    # pandas_memory_groupby=pandas_aggregation['memory']

    # polars_filter_mem = [polars_memory_filtering[0], max(polars_memory_filtering), polars_memory_filtering[-1]]
    # pandas_filter_mem = [pandas_memory_filtering[0], max(pandas_memory_filtering), pandas_memory_filtering[-1]]

    # polars_groupby_mem = [polars_memory_groupby[0], max(polars_memory_groupby), polars_memory_groupby[-1]]
    # pandas_groupby_mem = [pandas_memory_groupby[0], max(pandas_memory_groupby), pandas_memory_groupby[-1]]

    # labels = ['Start', 'Max', 'Final']
    # x = np.arange(len(labels))  # [0, 1, 2]
    # width = 0.2

    # fig, ax = plt.subplots(figsize=(10, 6))

    # # Bar positions
    # positions = [
    #     (-1.5 * width, polars_filter_mem, '#1f77b4', 'Polars - Filter'),
    #     (+0.5 * width, pandas_filter_mem, '#ff7f0e', 'Pandas - Filter'),
    #     (-0.5 * width, polars_groupby_mem, '#2ca02c', 'Polars - GroupBy'),
    #     (+1.5 * width, pandas_groupby_mem, '#d62728', 'Pandas - GroupBy')
    # ]

    # # Plot and annotate each group
    # for offset, values, color, label in positions:
    #     bars = ax.bar(x + offset, values, width, label=label, color=color)
    #     for i, val in enumerate(values):
    #         ax.text(x[i] + offset, val + 10, f'{val:.1f}', ha='center', va='bottom', fontsize=8)

    # # Formatting
    # ax.set_ylabel('Memory Usage (MB)')
    # ax.set_title('Memory Usage Comparison: Polars vs Pandas')
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels)
    # ax.legend()

    # plt.tight_layout()
    # plt.show()
    # #############################################################################################

    # # Example data — replace these with your actual CPU samples
    # polars_filter_cpu =  polars_filtering['cpu']
    # pandas_filter_cpu =  pandas_filtering['cpu']

    # polars_groupby_cpu = polars_aggregation['cpu']
    # pandas_groupby_cpu = pandas_aggregation['cpu']

    #     # def to_floats(lst):
    #     # return [float(x) for x in list]
    #     # polars_memory_filtering = to_floats(polars_memory_filtering)
    #     # pandas_memory_filtering = to_floats(pandas_memory_filtering)
    #     # polars_memory_groupby = to_floats(polars_memory_groupby)
    #     # pandas_memory_groupby = to_floats(pandas_memory_groupby)


    # # Generate time axis (e.g., ticks every 0.05s if you used interval=0.05)
    # ticks = list(range(len(polars_filter_cpu)))  # same for all lists

    # plt.figure(figsize=(12, 6))

    # # Plot each line
    # plt.plot(ticks, polars_filter_cpu, label='Polars - Filter', color='#1f77b4', linestyle='-')
    # plt.plot(ticks, pandas_filter_cpu, label='Pandas - Filter', color='#ff7f0e', linestyle='--')
    # plt.plot(ticks, polars_groupby_cpu, label='Polars - GroupBy', color='#2ca02c', linestyle='-')
    # plt.plot(ticks, pandas_groupby_cpu, label='Pandas - GroupBy', color='#d62728', linestyle='--')

    # # Labeling
    # plt.title('CPU Usage Over Time (Polars vs Pandas)')
    # plt.xlabel('Time Tick (each = ~0.02s)')
    # plt.ylabel('CPU Usage (%)')
    # plt.legend()
    # plt.grid(True, linestyle='--', alpha=0.6)
    # plt.tight_layout()
    # plt.show()
