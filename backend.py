# backend.py

import math
import json
#import pandas as pd


'''
Notes:
t_fab not considered in propagating bucling in DNV check?
Burst check, system test, derating has no impact on results? Check with DNV excel
Test Pmin and Ptest significance in Excel for bursting check
handle comma inputs and error when set the SMYS to 4.5MPa, the minWT comes back as a string
input validity checks
UI minimum vertical is off and the remove the dragging lines
'''
def print_dict(dictionary):
    rounded_values = {key: round(value, 5) if isinstance(value, (int, float)) else value for key, value in dictionary.items()}
    print(json.dumps(rounded_values, indent=4, sort_keys=False))
            

Barg_to_Pa = 1e5
Pa_to_Barg = 1e-5
MPa_to_Barg = 1e1
Barg_to_MPa = 1e-1
MPa_to_Pa = 1e6
Pa_to_MPa = 1e-6
GPa_to_Pa = 1e9
Pa_to_GPa = 1e-9
fraction_to_percent = 1e2
percent_to_fraction = 1e-2
N_to_kN = 1e-3
kN_to_n = 1e3
Nmm_to_kNm = 1e-6
mm_to_m = 1e-3


factors = {
    "gamma_SC": {
        "Pressure containment": {
            "Low": 1.046,
            "Medium": 1.138,
            "High": 1.308,
            "Very high": 1.593,
            "System test": 1.046,
            "All factors 1": 1
        },
        "other": {
            "Low": 1.04,
            "Medium": 1.14,
            "High": 1.26,
            "Very high": 1.5,
            "System test": 1.04,
            "All factors 1": 1
        }
    },
    "gamma_M": {
        "default": 1.15,
        "All factors 1": 1
    },
    "gamma_INC": {
        "default": 1.1,
        "All factors 1": 1
    },
    "alpha_U": {
        "default": 0.96,
        "System test": 1  # Check this
    }
}


config = {
    "Accuracy": 0.0004,
    "AddMaterialReq": False,
    "diameter_type": "OD [mm]",
    "DNV_material_selection": "DNV",
    
    "Pressure containment": {
        "operational": {
            "enable_corrosion": True,
            "enable_derating": True,
            "safety_class": "High"
        },
        "system test": {
            "enable_corrosion": True,
            "enable_derating": True,
            "safety_class": "System test"
        }
    },
    "Collapse": {
        "default": {
            "enable_corrosion": True,
            "enable_derating": True,
            "safety_class": "High"
        }
    },
    "Propagating buckling": {
        "default": {
            "enable_corrosion": True,
            "enable_derating": True,
            "safety_class": "High"
        }
    }
}


# Define parameters
parameters = {
    # Common:
    "g": 9.81,                # Acceleration due to gravity [m/s^2]
    
    # Pressures and Reference elevations for pressure levels:
    "P_design": 8.4,                    # Design Pressure [MPa]
    "P_min": 0,                         # Minimum Pressure [MPa] (not used ye)
    "P_test": 0,                        # Test Pressure [MPa]    (not used yet)

    "ref_el_design_pressure": 0,   # Elevation relative to Design Pressure [m]
    "ref_el_min_pressure": 0,      # Elevation relative to Minimum Pressure [m]
    "ref_el_test_pressure": 0,     # Elevation relative to Test Pressure [m]

    # Dimensions and Tolerances:
    "OD": 1025.6,             # Diameter OD [mm]
    "D": 1025.6,              # Diameter (undefined, entry for UI) [mm]
    "t": 28.6,                # Nominal thickness [mm]
    "t_cor": 9,               # Corrosion allowance [mm]
    "t_fab": 1,               # Fabrication tolerance [mm]
    "t_bendthin": 1,          # Bend thinning [mm]
    #"t_bendthin": self.ui.le_t_bendthin.text(),
    "alpha_fab": 0.85,        
    "alpha_gw": 0,            #  (not used yet)
    "fo": 0.005,              # Out-of-roundness [-]

    # Material Properties:
    "SMYS": 450.0,            # Specified minimum yield stress [MPa]
    "SMTS": 535.0,            # Specified minimum tensile strength [MPa]
    "fytemp": 9,              # Temperature derating for yield stress [MPa]
    "futemp": 9,              # Temperature derating for tensile strength [MPa]
    "E": 207e9,               # Young's modulus [Pa]
    "nu": 0.3,                # Poisson's ratio

    # Density:
    "rho_design": 98,         # Density of content in design/operation condition [kg/m^3]
    "rho_test": 1005,         # Density of content in system test [kg/m^3]
    "rho_min": 78,            # Density of content for minimum internal pressure [kg/m^3]   
    "rho_ext": 1005,          # Density of external fluid [kg/m^3]
    
    # Reference elevations relative to Mean Water Level (MWL):
    "water_depth": 10,        # Water Depth (from MWL) [m]
    "max_elevation": 0.5,     # Maximum Elevation Above MWL [m]
    "min_elevation": -0.5,    # Minimum Elevation Below MWL [m]

    # Other Parameters:
}
"""
def save_to_excel(data, file_path):
    with pd.ExcelWriter(file_path) as writer:
        df_factors = pd.DataFrame(data["factors"])
        df_factors.to_excel(writer, sheet_name="factors", index=False)
        
        df_config = pd.DataFrame(data["config"])
        df_config.to_excel(writer, sheet_name="config", index=False)
        
        df_parameters = pd.DataFrame(data["parameters"])
        df_parameters.to_excel(writer, sheet_name="parameters", index=False)

def read_from_excel(file_path):
    with pd.ExcelFile(file_path) as xls:
        data = {}
        data["factors"] = pd.read_excel(xls, sheet_name="factors").to_dict(orient='records')
        data["config"] = pd.read_excel(xls, sheet_name="config").to_dict(orient='records')
        data["parameters"] = pd.read_excel(xls, sheet_name="parameters").to_dict(orient='records')
        return data

# Example usage:
data = {
    "factors": factors,
    "config": config,
    "parameters": parameters
}

save_to_excel(data, 'data.xlsx')

data_from_excel = read_from_excel('data.xlsx')
factors_from_excel = data_from_excel["factors"]
config_from_excel = data_from_excel["config"]
parameters_from_excel = data_from_excel["parameters"]
"""


class DNV_F101_Verification:
    
    """
    Class for performing DNV-OS-F101 verification calculations.
    Code compliance design of submarine pipelines.
    """

    def __init__(self, par, conf):
        self.parameters = par.copy()
        self.config = conf
        self.factors = factors
        self.set_parameters()
        
        self.parameters["limit_state"] = self.limit_state
        self.parameters["condition"] = self.condition

    def set_parameters(self):
        self.parameters["enable_corrosion"] = self.config[self.limit_state][self.condition]["enable_corrosion"]
        self.parameters["enable_derating"] = self.config[self.limit_state][self.condition]["enable_derating"]
        self.parameters["safety_class"] = self.config[self.limit_state][self.condition]["safety_class"]

        self.gamma_inc() # Assign safety factor, gamma_inc.
        self.gamma_sc()  # Assign safety class factor, gamma_sc.
        self.gamma_m()   # Assign limit state factor, gamma_m.
        self.alpha_u()   # Assign alpha_U.
        self.code_wt()   # Calculate code verification wall thickness considering corrosion, fabrication tolerances.
        self.calculate_fy_fu() # Calculate yield strength (fy) and tensile strength (fu) considering derating.
        
    def calculate_fy_fu(self):
        """
        Calculate yield strength (fy) and tensile strength (fu) considering derating.
        """
        SMYS = self.parameters["SMYS"]
        SMTS = self.parameters["SMTS"]
        derating_enabled = self.parameters["enable_derating"]
    
        alpha_U = self.parameters["alpha_U"]
        fytemp = self.parameters["fytemp"] if derating_enabled else 0
        futemp = self.parameters["futemp"] if derating_enabled else 0

        self.parameters["fy"] = (SMYS - fytemp ) * alpha_U   # Yield strength [MPa]
        self.parameters["fu"] = (SMTS - futemp ) * alpha_U   # Tensile strength [MPa] 
    
    def local_pressure(self, pressure: float, density: float, depth: float) -> float: 
        """
        Calculate local pressure.

        Args:
            pressure (float): Pressure [MPa].
            density (float): Density [kg/m^3].
            depth (float): Depth [m].

        Returns:
            float: Local pressure [MPa].
        """
        h = depth if depth is not None else self.parameters["water_depth"]     # Depth [m]
        return pressure + (density * self.parameters["g"] * h) * Pa_to_MPa     # Local pressure [MPa]
    
    def internal_pressure(self, depth: float) -> float: 
        """
        Calculate local internal pressure.

        Args:
            depth (float): Depth [m].
        """
        self.parameters["Pl_i/t"] = self.local_pressure(self.parameters["Pressure"], self.parameters["rho_int"], depth)
        
    def external_pressure(self, depth: float) -> float: 
        """
        Calculate local external pressure.

        Args:
            depth (float): Depth [m].
        """
        self.parameters["Pe"] = self.local_pressure(0, self.parameters["rho_ext"], depth)


    def code_wt(self):
        """
        Calculate code verification wall thickness considering corrosion, fabrication tolerances.
        """
        corrosion_enabled = self.parameters["enable_corrosion"]
        t = self.parameters["t"]
        t_cor = self.parameters["t_cor"] if corrosion_enabled else 0
        t_fab = self.parameters["t_fab"]
        self.parameters["t_code"] = t - t_fab - t_cor  

    def gamma_sc(self):  
        """
        Assign safety class factor, gamma_sc.
        """
        self.parameters["gamma_sc"] = self.get_gamma_sc(self.limit_state, self.parameters["safety_class"], self.condition)

    def gamma_m(self):
        """
        Assign limit state factor, gamma_m.
        """
        self.parameters["gamma_m"] = self.get_gamma_m(self.parameters["safety_class"])

    def gamma_inc(self):
        """
        Assign safety factor, gamma_inc.
        """
        safety_class = self.parameters["safety_class"]
        self.parameters["gamma_inc"] = factors["gamma_INC"].get(safety_class, factors["gamma_INC"]["default"])
    
    def alpha_u(self):
        """
        Assign the value of alpha_U based on conditions.

        If material requirements are added, alpha_U is set to 1.
        """
        
        if self.config["AddMaterialReq"]:
            self.parameters["alpha_U"] = 1 
        else:
            condition = self.condition
            # Determine alpha_U based on the condition, using a default value if condition is not found
            self.parameters["alpha_U"] = factors["alpha_U"].get(condition, factors["alpha_U"]["default"]) # Check F101
    
    @staticmethod
    def get_gamma_sc(limit_state: str, safety_class: str, condition: str) -> float:
        """
        Get safety class factor.

        Args:
            limit_state (str): Limit state.
            safety_class (str): Safety class.
            condition (str, optional): System condition - "operational" or "system test". (not used)
            
        Returns:
            float: Safety class factor.
        """
        gamma_limit_state = factors["gamma_SC"].get(limit_state, factors["gamma_SC"]["other"])
        return gamma_limit_state.get(safety_class, None)

    @staticmethod
    def get_gamma_m(safety_class: str) -> float:
        """
        Get limit state factor.

        Args:
            safety_class (str): Safety class.

        Returns:
            float: Limit state factor.
        """
        return factors["gamma_M"].get(safety_class, factors["gamma_M"]["default"])
    
class BurstCriterion(DNV_F101_Verification):
    def __init__(self, par, conf, condition):
        self.limit_state = "Pressure containment"
        self.condition = condition
        super().__init__(par, conf)
        
    def min_wt_burst(self) -> float:
        """
        Returns minimum allowable WT wrt. pressure containment check.

        Returns:
            float: Minimum WT for Burst resistance [mm] (exclusive of tolerances, corrosion allowance).
        """
        
        OD = self.parameters["OD"]
        Pe = self.parameters["Pe"]
        fcb = self.parameters["fcb"]
        Pi = self.parameters["Pl_i/t"]
        gamma_m = self.parameters["gamma_m"]
        gamma_sc = self.parameters["gamma_sc"]
        P = Pi - Pe
        return (math.sqrt(3) * OD * gamma_m * gamma_sc * P) / (4 * fcb + math.sqrt(3) * gamma_m * gamma_sc * P)

    def dnv_excel_burst(self, t_cor: float):
        """
        Calculate pressure containment resistance and minimum wt (Excel).
        """
        t1 = self.parameters["t_code"]
        p_b = self.dnv_burst_check(t1)
        dnv_utility = self.dnv_utility(p_b)
        utility_burst = dnv_utility

        NumberOfIter = 1
        while abs(utility_burst - 1) > self.config["Accuracy"]:
            t1 = t1 * utility_burst ** 0.25
            p_b = self.dnv_burst_check(t1)
            utility_burst = self.dnv_utility(p_b)
            NumberOfIter += 1
            if NumberOfIter > 100:
                print("Minimum required nominal thickness with respect to burst during system pressure test not found; may be very small or very large.")
                t1 = float('nan')
                break
        dnv_min_wt = t1
        self.min_wt_dnv = dnv_min_wt + self.parameters["t_fab"] + t_cor
        self.utilisation_dnv = dnv_utility
        
    def dnv_burst_check(self, t: float) -> float:
        """
        Calculate pressure containment resistance (Excel).
        """
        OD = self.parameters["OD"]
        fcb = self.parameters["fcb"]
        #t = self.parameters["t_code"]
        
        p_b = (2 * t / (OD - t)) * fcb * (2 / (3 ** 0.5))
        #self.parameters["dnv_p_b"] = p_b
        return p_b
    
    def dnv_utility(self, p_b: float) -> float:
        """
        Calculate pressure containment utilisation (Excel).
        """
        Pl = self.parameters["Pl_i/t"]
        Pe = self.parameters["Pe"]
        gamma_m = self.parameters["gamma_m"]
        gamma_sc = self.parameters["gamma_sc"]
        #p_b = self.parameters["p_b"]
        
        utility = (Pl - Pe) * gamma_m * gamma_sc / p_b
        #self.parameters["dnv_utility"] = utility
        return utility

    def set_parameters_burst(self):
        if self.condition == "system test":
            self.parameters["rho_int"] = self.parameters["rho_test"]
            self.parameters["ref_el_pressure"] = self.parameters["ref_el_test_pressure"]
        else:  # operational
            self.parameters["rho_int"] = self.parameters["rho_design"]
            self.parameters["ref_el_pressure"] = self.parameters["ref_el_design_pressure"]


    def calculate_fcb(self):
        """
        Calculate and assign burst material strength, fcb.
        """
        SMYS = self.parameters["SMYS"]
        SMTS = self.parameters["SMTS"]

        if self.condition == "system test":
            fcb = min(SMYS, SMTS / self.parameters["gamma_m"])
        else:
            fy = self.parameters["fy"]
            fu = self.parameters["fu"]
            fcb =  min(fy, fu / self.parameters["gamma_m"])
        self.parameters["fcb"] = fcb
        
    def run(self):
        """
        Perform pressure containment criterion calculations for operational or system test conditions.
        """
        self.set_parameters_burst()

        PdD = self.parameters["P_design"]
        gamma_inc = self.parameters["gamma_inc"]
        
        if self.condition == "system test":
            self.parameters["Pressure"] = PdD * gamma_inc * 1.05  # Test pressure [MPa]
        else:  # Operational
            self.parameters["Pressure"] = PdD * gamma_inc         # Incidental pressure [MPa]

        t_code = self.parameters["t_code"]
        gamma_m = self.parameters["gamma_m"]
        gamma_sc = self.parameters["gamma_sc"]
        
        self.calculate_fcb()  # Calculate fcb based on condition

        depth_for_Pe = self.parameters["water_depth"] + self.parameters["min_elevation"]
        depth_for_Pi = self.parameters["water_depth"] + self.parameters["ref_el_pressure"]

        self.external_pressure(depth_for_Pe) # External pressure [MPa]
        self.internal_pressure(depth_for_Pi) # Internal pressure [MPa]
        
        Pe = self.parameters["Pe"]       # Local external pressure [MPa]
        Pl = self.parameters["Pl_i/t"]   # Local internal (incidental, Pli / test, Plt) pressure [MPa]

        min_wt = self.min_wt_burst()
        t_cor = self.parameters["t_cor"] if self.parameters["enable_corrosion"] else 0
        self.min_wt = min_wt + self.parameters["t_fab"] + t_cor
        self.utilisation = min_wt / t_code
        
        #print("min_wt = ", self.min_wt)
        #print("UR = ", self.utilisation)
        
        self.dnv_excel_burst(t_cor)
        print("DNV min_wt  = ", self.min_wt_dnv)
        print("DNV utility  = ", self.utilisation_dnv)
        
        #self.print_all_variables()


burst_operational = BurstCriterion(parameters, config, "operational")
burst_operational.run()



burst_test = BurstCriterion(parameters, config, "system test")
burst_test.run()

#print_dict(burst_operational.parameters)
#print_dict(burst_operational.config)

#print_dict(burst_test.parameters)
#print_dict(burst_operational.config)
import os
print(os.getcwd())