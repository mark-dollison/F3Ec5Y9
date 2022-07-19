
from azure. identity import ClientSecretCredential 
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
from datetime import datetime, timedelta
import time
import sys
sys.path


def print_item(group):
    """Print an Azure object instance."""
    print("Name: {}".format(group.name))
    print("Id: {}".format(group.id))
    if hasattr(group, 'location'):
        print("Location: {}".format(group.location))
    if hasattr(group, 'tags'):
        print("Tags: {}".format(group.tags))
    if hasattr(group, 'properties'):
        print_properties(group.properties)

def print_properties(props):
    """Print a ResourceGroup properties instance."""
    if props and hasattr(props, 'provisioning_state') and props.provisioning_state:
        print("Properties:")
        print("Provisioning State: {}".format(props.provisioning_state))
    print("\n\n")

def print_activity_run_details(activity_run):
    """Print activity run details."""
    print("\nActivity run details\n")
    print("Activity run status: {}".format(activity_run.status))
    if activity_run.status == 'Succeeded':
        print("Number of bytes read: {}".format(activity_run.output['dataRead']))
        print("Number of bytes written: {}".format(activity_run.output['dataWritten']))
        print("Copy duration: {}".format(activity_run.output['copyDuration']))
    else:
        print("Errors: {}".format(activity_run.error['message']))


def main():
    
    # Azure subscription ID
    subscription_id = '9e963904-d6da-4cac-a44c-bb9ccaffe88f'

    # This program creates this resource group. If it's an existing resource group, comment out the code that creates the resource group
    rg_name = 'ta-poc-rsgroup'

    # The data factory name. It must be globally unique.
    df_name = '1ta1-df'
    
    rg_params = {'location':'East US'}
    df_params = {'location':'East US'}
    
    # Specify your Active Directory client ID, client secret, and tenant ID
    credentials = ClientSecretCredential(client_id='accd34c8-8ba8-4a96-82b0-e53427f19eeb', client_secret='.oH8Q~hHAryoucKBuwlLCtxCHW03lXJp~kSr4ctc', tenant_id='c765a151-1467-4c15-b0c5-6a66b03f412a') 
    resource_client = ResourceManagementClient(credentials, subscription_id)
    adf_client = DataFactoryManagementClient(credentials, subscription_id)
    
    
    # Create an Azure Storage linked service
    ls_name = 'AzureBlobStorage1'
    # IMPORTANT: specify the name and key of your Azure Storage account.
    storage_string = SecureString(value='DefaultEndpointsProtocol=https;AccountName=1ta1strgacc;AccountKey=9EWT+ZwjHMHNPtKZBeTU+SpM/Ve5u+G9Fw41LhNk5YrSbAuOMtPkLFzcGsR/4ojL0GFmXIqhTPFv+AStGcY16A==;EndpointSuffix=core.windows.net')
    ls_azure_storage = LinkedServiceResource(properties=AzureStorageLinkedService(connection_string=storage_string)) 
    ls = adf_client.linked_services.create_or_update(rg_name, df_name, ls_name, ls_azure_storage)
    print_item(ls)
    

# Start the main method
main()