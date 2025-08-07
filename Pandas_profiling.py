import pandas as pd
import Methods_Pandas
import Performance


#dataframe = pd.read_csv(r'C:\Users\pio-tech\Polars-Pandas\synthetic_bank_transactions.csv')
def filtering_method(filepath) -> dict:
    dataframe = pd.read_parquet(filepath)
    print("--------------------------------------------------------")
    func = Methods_Pandas.filter_method
    args = [dataframe,"transaction_amount", 10, '>'] 

    start = Performance.start_time()
    largeTransactionAmount =  func(*args)
    end = Performance.end_time()
    print("Pandas Runtime: ", end-start)


    print("Pandas Resources Monitoring (Filtering): \n")
    memory_usage_filtering = Performance.monitor_memory_usage(func, args)
    cpu_usage_filtering = Performance.show_cpu_usage(func, args)
    return {
        'result': largeTransactionAmount,
        'runtime': end-start,
        'memory': memory_usage_filtering,
        'cpu': cpu_usage_filtering
    }



# def get_results_filtering() -> list:
#     return memory_usage_filtering, cpu_usage_filtering
# #Print.show_results(largeTransactionAmount)

def groupby_method(filepath) -> dict:
    dataframe=pd.read_parquet(filepath)
    operations_list_groupby = {
        "transaction_date" : ["print"],
        "transaction_amount" : ["sum", "mean", "median", "max"]
    }
    grouped_columns = ["country"]
    func = Methods_Pandas.group_by_aggregation
    args = [dataframe, grouped_columns, operations_list_groupby, "country"]


    start = Performance.start_time()

    group_by_country = func(*args)

    end = Performance.end_time()
    print("Pandas Runtime: ", end-start)

    print("Pandas Resources Monitoring (Aggregate Group by): \n")
    memory_usage_aggregation = Performance.monitor_memory_usage(func, args)
    cpu_usage_aggregation = Performance.show_cpu_usage(func, args)

    return {
        'result': group_by_country,
        'runtime': end-start,
        'memory': memory_usage_aggregation,
        'cpu':cpu_usage_aggregation
    }

# def get_results_aggregation() -> list:
#     return memory_usage_aggregation, cpu_usage_aggregation





# # operations_list_rolling = {
#     "transaction_amount": ["sum", "mean"]
# }
# 
#removed because transaction_date is not a datetime format
def window_method(filepath) -> dict:
    dataframe = pd.read_parquet(filepath)
    dataframe["transaction_date"] = pd.to_datetime(dataframe["transaction_date"], format="%Y-%m-%d %H:%M:%S.%f", errors="coerce")
    func = Methods_Pandas.rolling_window_aggregation
    operations_window ={
        "transaction_amount": ["sum", "mean"]
    }
    args = [dataframe, "transaction_date", "7D", operations_window]

    start = Performance.start_time()
    rolling_window_pandas = func(*args)
    end = Performance.end_time()
    print("Runtime (Aggregation): ", end-start)

    
    memory_usage_window = Performance.monitor_memory_usage(func, args)
    cpu_usage_window = Performance.show_cpu_usage(func,args)


    return{
        'result': rolling_window_pandas,
        'runtime': end-start,
        'memory': memory_usage_window,
        'cpu': cpu_usage_window
    }

    #Print.show_results(rolling_window_operation)44

if __name__ == "__main__":
    print("Filtering", filtering_method())
    print("Groupby", groupby_method())