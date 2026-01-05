from dataclasses import dataclass
import math
from enum import Enum
from typing import Optional

class ModulationScheme(Enum):
    BPSK = "BPSK"
    QPSK = "QPSK"
    QAM16 = "16-QAM"
    QAM64 = "64-QAM"

class PropagationModel(Enum):
    AWGN = "AWGN"
    RAYLEIGH = "Rayleigh"
    RICIAN = "Rician"
    LOGNORMAL = "Log-normal"

@dataclass
class LinkBudgetParams:
    tx_power_dbm: float
    tx_gain_dbi: float
    rx_gain_dbi: float
    path_loss_db: float
    atm_loss_db: float
    sys_temp_k: float
    bandwidth_hz: float
    freq_ghz: float
    modulation: ModulationScheme
    propagation: PropagationModel
    required_ebn0_db: float

@dataclass
class LinkBudgetResults:
    received_power_dbm: float
    cnr_db: float
    ber: float
    link_margin_db: float
    warnings: list[str]

class LinkBudgetCalculator:
    # Boltzmann constant in dBm/K/Hz
    BOLTZMANN_CONSTANT = -198.6

    @staticmethod
    def calculate(params: LinkBudgetParams) -> LinkBudgetResults:
        warnings = []
        
        # Check propagation model
        if params.propagation != PropagationModel.AWGN:
            raise ValueError(
                f"The selected propagation model ({params.propagation.value}) is not yet implemented. "
                "Please select AWGN or check back in a future update."
            )

        # Calculate received power
        received_power_dbm = (
            params.tx_power_dbm +
            params.tx_gain_dbi +
            params.rx_gain_dbi -
            params.path_loss_db -
            params.atm_loss_db
        )

        # Calculate noise power
        noise_power_dbm = (
            LinkBudgetCalculator.BOLTZMANN_CONSTANT +
            10 * math.log10(params.sys_temp_k) +
            10 * math.log10(params.bandwidth_hz)
        )

        # Calculate C/N ratio
        cnr_db = received_power_dbm - noise_power_dbm

        # Calculate Eb/N0
        ebn0_db = cnr_db - 10 * math.log10(params.bandwidth_hz / (params.bandwidth_hz / 2))  # Assuming Nyquist rate

        # Calculate BER based on modulation scheme
        ber = LinkBudgetCalculator._calculate_ber(params.modulation, ebn0_db)

        # Calculate link margin
        link_margin_db = ebn0_db - params.required_ebn0_db

        # Check link margin
        if link_margin_db < 0:
            warnings.append("Warning: Negative link margin! The connection will be unstable.")
        elif link_margin_db < 3:
            warnings.append("Warning: Link margin below 3 dB! Consider improving system parameters.")

        return LinkBudgetResults(
            received_power_dbm=received_power_dbm,
            cnr_db=cnr_db,
            ber=ber,
            link_margin_db=link_margin_db,
            warnings=warnings
        )

    @staticmethod
    def _calculate_ber(modulation: ModulationScheme, ebn0_db: float) -> float:
        """Calculate Bit Error Rate based on modulation scheme and Eb/N0."""
        ebn0 = 10 ** (ebn0_db / 10)  # Convert from dB to linear
        
        if modulation == ModulationScheme.BPSK:
            # BER = Q(sqrt(2*Eb/N0))
            return 0.5 * math.erfc(math.sqrt(ebn0))
        
        elif modulation == ModulationScheme.QPSK:
            # BER = Q(sqrt(Eb/N0))
            return 0.5 * math.erfc(math.sqrt(ebn0 / 2))
        
        elif modulation == ModulationScheme.QAM16:
            # Approximate BER for 16-QAM
            return 0.75 * math.erfc(math.sqrt(ebn0 / 10))
        
        elif modulation == ModulationScheme.QAM64:
            # Approximate BER for 64-QAM
            return 0.75 * math.erfc(math.sqrt(ebn0 / 42))
        
        else:
            raise ValueError(f"Unsupported modulation scheme: {modulation}")

    @staticmethod
    def calculate_fspl(distance_km: float, freq_ghz: float) -> float:
        """Calculate Free Space Path Loss in dB."""
        return 92.45 + 20 * math.log10(freq_ghz) + 20 * math.log10(distance_km)

    @staticmethod
    def dbm_to_watts(power_dbm: float) -> float:
        """Convert power from dBm to Watts."""
        return 10 ** ((power_dbm - 30) / 10)

    @staticmethod
    def watts_to_dbm(power_watts: float) -> float:
        """Convert power from Watts to dBm."""
        return 10 * math.log10(power_watts * 1000)

