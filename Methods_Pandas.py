import pandas as pd

def filter_method(dataframe: pd.DataFrame, column_name: str, filter_value, operation: str) -> int:
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

    return operations[operation](dataframe[column_name], filter_value).sum()


def value_in_column(dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
    return dataframe[column_name].value_counts().reset_index(name='count').rename(columns={'index': column_name})


def group_by_aggregation(
    dataframe: pd.DataFrame,
    group_by_columns: list,
    aggregation_operations: dict,
    sort_by: str,
    descending: bool = False
) -> pd.DataFrame:
    agg_dict = {}

    for column, operations in aggregation_operations.items():
        for op in operations:
            if op == 'print':
                continue
            key = f"{column}_{op}"
            agg_dict[key] = (column, op)

    grouped = dataframe.groupby(group_by_columns).agg(**agg_dict).reset_index()

    if sort_by:
        return grouped.sort_values(by=sort_by, ascending=not descending)
    return grouped


def rolling_window_aggregation(
    dataframe: pd.DataFrame,
    index_column: str,
    period: str,
    aggregation_operations: dict
) -> pd.DataFrame:
    df = dataframe.copy()
    df[index_column] = pd.to_datetime(df[index_column])
    df = df.sort_values(index_column).set_index(index_column)

    result = pd.DataFrame(index=df.index)

    for column, operations in aggregation_operations.items():
        for op in operations:
            rolled = df[column].rolling(period)
            if op == 'sum':
                result[f"{column}_sum"] = rolled.sum()
            elif op == 'mean':
                result[f"{column}_mean"] = rolled.mean()
            elif op == 'count':
                result[f"{column}_count"] = rolled.count()
            elif op == 'median':
                result[f"{column}_median"] = rolled.median()
            elif op == 'max':
                result[f"{column}_max"] = rolled.max()
            elif op == 'min':
                result[f"{column}_min"] = rolled.min()
            elif op == 'print':
                result[column] = df[column]

    result = result.reset_index()
    return result
