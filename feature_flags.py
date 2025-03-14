import ldclient
from ldclient import Context
from ldclient.config import Config

def initialize_ldclient(sdk_key):
    """Initialize the LaunchDarkly client"""
    ldclient.set_config(Config(sdk_key))
    return ldclient.get().is_initialized()

def get_flag_value(flag_key, default_value=False):
    """Get the value of a feature flag"""
    context = Context.builder("example-user-key").kind("user").name("Sandy").build()
    return ldclient.get().variation(flag_key, context, default_value)

def show_evaluation_result(key, value):
    """Print the evaluation result of a feature flag"""
    print()
    print(f"*** The {key} feature flag evaluates to {value}") 
    