from dataclasses import dataclass
from typing import Optional

@dataclass
class DataBudgetParams:
    data_rate_mbps: float  # Payload data generation rate in Mbps
    storage_capacity_gb: float  # Storage capacity in GB
    downlink_rate_mbps: float  # Downlink transmission rate in Mbps
    pass_duration_min: float  # Ground station pass duration in minutes
    passes_per_day: int  # Number of passes per day

@dataclass
class DataBudgetResults:
    daily_data_gb: float  # Total data generated per day in GB
    daily_downlink_capacity_gb: float  # Available downlink capacity per day in GB
    storage_usage_gb: float  # Current storage usage in GB
    backlog_gb: float  # Expected data backlog in GB
    storage_exceeded: bool  # Whether storage capacity will be exceeded
    days_until_full: Optional[float]  # Days until storage is full (if applicable)

class DataBudgetCalculator:
    BITS_TO_BYTES = 8
    BYTES_TO_GB = 1e9
    SECONDS_PER_DAY = 86400  # 24 * 60 * 60
    
    @staticmethod
    def calculate(params: DataBudgetParams) -> DataBudgetResults:
        # Calculate daily data generation in GB
        bits_per_day = params.data_rate_mbps * 1e6 * DataBudgetCalculator.SECONDS_PER_DAY
        daily_data_gb = bits_per_day / (DataBudgetCalculator.BITS_TO_BYTES * DataBudgetCalculator.BYTES_TO_GB)
        
        # Calculate daily downlink capacity in GB
        total_pass_seconds = params.pass_duration_min * 60 * params.passes_per_day
        total_downlink_bits = params.downlink_rate_mbps * 1e6 * total_pass_seconds
        daily_downlink_capacity_gb = total_downlink_bits / (DataBudgetCalculator.BITS_TO_BYTES * DataBudgetCalculator.BYTES_TO_GB)
        
        # Calculate storage usage and backlog
        daily_deficit = daily_data_gb - daily_downlink_capacity_gb
        storage_exceeded = False
        days_until_full = None
        
        if daily_deficit <= 0:
            # We can downlink more than we generate
            storage_usage_gb = min(daily_data_gb, params.storage_capacity_gb)
            backlog_gb = 0
        else:
            # We generate more than we can downlink
            storage_usage_gb = params.storage_capacity_gb
            backlog_gb = daily_deficit
            storage_exceeded = True
            
            # Calculate days until storage is full
            if daily_deficit > 0:
                days_until_full = params.storage_capacity_gb / daily_deficit
        
        return DataBudgetResults(
            daily_data_gb=daily_data_gb,
            daily_downlink_capacity_gb=daily_downlink_capacity_gb,
            storage_usage_gb=storage_usage_gb,
            backlog_gb=backlog_gb,
            storage_exceeded=storage_exceeded,
            days_until_full=days_until_full
        ) 