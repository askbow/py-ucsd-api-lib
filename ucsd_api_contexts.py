'''
This lists context constants to be used with UCSD API

based on http://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/ucs-director/rest-api-guide/5-0/b_Cisco_UCS_Director_REST_Developer_Guide_50/b_Cisco_UCS_Director_REST_Developer_Guide_41_chapter_01100.html

'''


#Administrative Contexts
CONTEXT_TYPE_GLOBAL= "global"
CONTEXT_TYPE_GLOBAL_ADMIN = "global-admin"
CONTEXT_TYPE_GLOBAL_SERVICES = "global-services"
CONTEXT_TYPE_CLOUD = "cloud"
CONTEXT_TYPE_HOSTNODE = "hostnode"
CONTEXT_TYPE_CLUSTER = "cluster"

#End User Contexts
CONTEXT_TYPE_GROUP = "group"
CONTEXT_TYPE_VM = "vm"
CONTEXT_TYPE_VDC = "vdc"
CONTEXT_TYPE_SR = "servicerequest"

#Data Center Contexts
CONTEXT_TYPE_PHYSICAL_DATACENTER = "datacenter"

#NetApp Report Contexts
CONTEXT_TYPE_STORAGE_ACCOUNTS= " storage_accounts"
CONTEXT_TYPE_STORAGE_FILERS = " netapp_filer"
CONTEXT_TYPE_STORAGE_AGGREGATES = " storage_aggregates"
CONTEXT_TYPE_STORAGE_VOLUMES = "storage_volumes"
CONTEXT_TYPE_STORAGE_LUNS = "luns"
CONTEXT_TYPE_STORAGE_VFLIERS = "netapp_v_flier"

#UCS Report Contexts
CONTEXT_TYPE_INFRA_COMPUTE_UCSM_ACCOUNT= " ucsm"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_FABRIC_INTERCONNECT = " compute_fbi"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_CHASSIS = " compute_chassis"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_SERVER = "compute_server"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_SERVICE_PROFILE = "service_profile"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_PORT_CHANNEL = "ucs_portchannel"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_ORGANIZATION = "ucs_org"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_SERVICE_PROFILE_TEMPLATE = "ucs_service-profile-template"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_BOOT_POLICY = "ucs_boot_policy"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_VNIC_TEMPLATE = "ucs_vnictemplate"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_MAC_POOL = "ucs_mac"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_UUID_POOL = "ucs_uuid"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_WWNN_POOL = "ucs_wwnn"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_WWPN_POOL = "ucs_wwpn"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_SERVICE_PROFILE_VHBA = "ucs_sp_vhba"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_SERVICE_PROFILE_VNIC = "ucs_sp_vnic"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_IOMODULE = "ucs_iomodule"
CONTEXT_TYPE_INFRA_COMPUTE_UCS_SERVER_ADAPTER_UNIT = "compute_server_adapter_unit"

#Network Report Contexts
CONTEXT_TYPE_INFRA_NETWORK_DEVICE= "network_device"
CONTEXT_TYPE_INFRA_NET_DEVICE_N1K = " net_device_n1k"
CONTEXT_TYPE_INFRA_NET_DEVICE_FAB_IC = " net_device_fab_ic"
CONTEXT_TYPE_INFRA_NET_DEVICE_N5K = "net_device_n5k"
CONTEXT_TYPE_INFRA_NETWORK_DEVICE_VLAN = "net_device_vlan"
CONTEXT_TYPE_INFRA_NETWORK_DEVICE_VSAN = "net_device_vsan"
CONTEXT_TYPE_INFRA_NETWORK_DEVICE_INTERFACE = "net_device_interface"
CONTEXT_TYPE_INFRA_NETWORK_DEVICE_PORT_PROFILE = "net_device_port_profile"
CONTEXT_TYPE_INFRA_NETWORK_DEVICE_ZONE = "net_device_zone"
CONTEXT_TYPE_INFRA_NET_QOS_POLICY = "net_device_qos_policy"

