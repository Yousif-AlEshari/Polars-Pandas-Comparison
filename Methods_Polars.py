import polars as pl

def filter_method(dataframe: pl.DataFrame, column_name: str, filter_value, operation: str) -> pl.DataFrame:
    operations = {
        '>': lambda col, val: col > val,
        '<': lambda col, val: col < val,
        '==': lambda col, val: col == val,
        '!=': lambda col, val: col != val,
        '>=': lambda col, val: col >= val,
        '<=': lambda col, val: col <= val
    }

    if operation not in operations:
        raise ValueError(f"Unsupported Operation {operation}")  

    return dataframe.filter(operations[operation](pl.col(column_name), filter_value))
    
def value_in_column(dataframe: pl.DataFrame, column_name: str) -> pl.DataFrame:
    return dataframe.select(pl.col(column_name).value_counts())
    

def group_by_aggregation(
    dataframe: pl.DataFrame,
    group_by_columns: list, 
    aggregation_operations: dict,
    sort_by: str,
    descending: bool = False
) -> pl.DataFrame:
    """
    Group the dataframe by the specified columns and apply the aggregation operations.

    :param dataframe: The input Polars DataFrame.
    :param group_by_columns: List of columns to group by.
    :param aggregation_operations: A dictionary where keys are column names and values are lists of aggregation functions to apply.
    :return: A Polars DataFrame with the grouped and aggregated data.
    """
    aggregation_exprs = []
    
    # For each column that needs to be aggregated, apply the specified operations
    for column, operations in aggregation_operations.items():
        for op in operations:
            if op == 'sum':
                aggregation_exprs.append(pl.col(column).sum().alias(f"{column}_sum"))
            elif op == 'mean':
                aggregation_exprs.append(pl.col(column).mean().alias(f"{column}_mean"))
            elif op == 'count':
                aggregation_exprs.append(pl.col(column).count().alias(f"{column}_count"))
            elif op == 'median':
                aggregation_exprs.append(pl.col(column).median().alias(f"{column}_median"))
            elif op == 'max':
                aggregation_exprs.append(pl.col(column).max().alias(f"{column}_max"))
            elif op == 'min':
                aggregation_exprs.append(pl.col(column).min().alias(f"{column}_min"))
            elif op == 'print':
                aggregation_exprs.append(pl.col(column))

    # Apply the groupby and aggregation
    result = dataframe.group_by(group_by_columns).agg(aggregation_exprs)
    if sort_by:
        return result.sort(sort_by, descending=descending)
    return result

def rolling_window_aggregation(
    dataframe: pl.DataFrame,
    index_column: str,
    period: str,
    aggregation_operations: dict
    ) -> pl.DataFrame:

    aggregation_expressions = []

    for column, operations in aggregation_operations.items():
        for op in operations:
            if op == 'sum':
                aggregation_expressions.append(pl.col(column).sum().alias(f"{column}_sum"))
            elif op == 'mean':
                aggregation_expressions.append(pl.col(column).mean().alias(f"{column}_mean"))
            elif op == 'count':
                aggregation_expressions.append(pl.col(column).count().alias(f"{column}_count"))
            elif op == 'median':
                aggregation_expressions.append(pl.col(column).median().alias(f"{column}_median"))
            elif op == 'max':
                aggregation_expressions.append(pl.col(column).max().alias(f"{column}_max"))
            elif op == 'min':
                aggregation_expressions.append(pl.col(column).min().alias(f"{column}_min"))
            elif op == 'print':
                aggregation_expressions.append(pl.col(column))
    return dataframe.rolling(index_column=index_column, period=period).agg(aggregation_expressions)
