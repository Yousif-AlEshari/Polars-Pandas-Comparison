import Methods_Polars
import Performance
import polars as pl



#dataframe = pl.read_csv(r'C:\Users\pio-tech\Polars-Pandas\synthetic_bank_transactions.csv')
def filtering(filepath) -> dict:
    dataframe=pl.read_parquet(filepath)
    print("--------------------------------------------------------")
    func = Methods_Polars.filter_method
    args = [dataframe, "transaction_amount", 10, '>']
    start = Performance.start_time()
    largeTransactionAmount = func(*args)
    #largeTransactionAmount = dataframe.filter((pl.col("transaction_amount") > 10))
    end = Performance.end_time()
    print("Polars Runtime: ", end-start)

    print("Polars Resources Monitoring (Filtering): \n")


    memory_usage_filtering = Performance.monitor_memory_usage(func, args)
    cpu_usage_filtering = Performance.show_cpu_usage(func, args)

    return {
    'result': largeTransactionAmount,
    'runtime': end-start,
    'memory':memory_usage_filtering,
    'cpu':cpu_usage_filtering
    }

# # def get_results_filtering() -> list:
#     return memory_usage_filtering, cpu_usage_filtering



def groupby(filepath) -> dict:
    dataframe=pl.read_parquet(filepath)
    print("----------------------------------------------------------------------")
    #Print.show_results(largeTransactionAmount) #Any Transactions with an amount of $1000+ will be saved in this object\
    #print(largeTransactionAmount.shape)
    #Print.show_results(values_in_account_status)
    operations_list_groupby = {
        "transaction_date" : ["print"],
        "transaction_amount" : ["sum", "mean", "median", "max"]
    }
    grouped_columns = ["country"]
    func = Methods_Polars.group_by_aggregation
    args = [dataframe, grouped_columns, operations_list_groupby, "country"]

    start = Performance.start_time()

    group_by_country = func(*args)

    end = Performance.end_time()
    print("Polars Runtime: ", end-start)


    print("Polars Resources Monitoring (Aggregate Group by): \n")
    memory_usage_aggregation = Performance.monitor_memory_usage(func, args)
    cpu_usage_aggregation = Performance.show_cpu_usage(func, args)
    return{
        'result': group_by_country,
        'runtime': end-start,
        'memory': memory_usage_aggregation,
        'cpu':cpu_usage_aggregation
    }

# def get_results_aggregation() -> list:
#     return memory_usage_aggregation, cpu_usage_aggregation




#Print.show_results(group_by_country)


# operations_list_rolling = {
#     "transaction_amount": ["sum", "mean"]
# }
#removed because transaction_date is not a datetime format
def window(filepath) -> dict:
    dataframe = pl.read_parquet(filepath)
    dataframe = dataframe.with_columns(
    pl.col("transaction_date").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S%.f", strict=False)
)

    func = Methods_Polars.rolling_window_aggregation
    operations_rolling = {
        "transaction_amount": ["sum", "mean"]
    }
    args = [dataframe, "transaction_date", "1w", operations_rolling]

    start = Performance.start_time()
    rolling_window_operation = func(*args)
    end = Performance.end_time()
    print("Runtime (Aggregation): ",end-start)

    memory_usage_window = Performance.monitor_memory_usage(func, args)
    cpu_usage_window = Performance.show_cpu_usage(func,args)


    return{
        'result': rolling_window_operation,
        'runtime': end-start,
        'memory': memory_usage_window,
        'cpu': cpu_usage_window
    }

#Print.show_results(rolling_window_operation)

if __name__ == "__main__":
    print("Filtering: ", filtering())
    print("GroupBy: ", groupby())
    print("Rolling Window", window() )

