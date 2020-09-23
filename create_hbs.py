from vnc_api import *
from vnc_api.vnc_api import VncApi
from vnc_api.vnc_api import Project
from vnc_api.vnc_api import VirtualNetwork
from vnc_api.vnc_api import NetworkIpam
from vnc_api.vnc_api import VnSubnetsType
from vnc_api.vnc_api import IpamSubnetType
from vnc_api.vnc_api import SubnetType
from vnc_api.vnc_api import HostBasedService
from vnc_api.vnc_api import ServiceVirtualNetworkType
from vnc_api.exceptions import NoIdError
from vnc_api.gen.resource_xsd import QuotaType

hbs_name = 'hbs'
project_name = 'k8s-hbs'
admin_user = 'admin'
admin_password = 'contrail123'
admin_project = 'admin'
api_node_ip = ''
api_node_port = '8082'
default_domain = 'default-domain'

if __name__ == "__main__":
    api = VncApi(
        username=admin_user,
        password=admin_password,
        tenant_name=admin_project,
        api_server_host=api_node_ip,
        api_server_port=api_node_port)
    try:
        project = api.project_read(fq_name=[default_domain, project_name])
        project.set_quota(QuotaType(host_based_service=1))
        api.project_update(project)
    except NoIdError:
        project = Project(name=project_name)
        puuid = api.project_create(project)
        project = api.project_read(fq_name=[default_domain, project_name])
    try:
        hbs = api.host_based_service_read(fq_name=project.fq_name + [hbs_name])
        hbs_created = False
    except NoIdError:
        hbs = HostBasedService(hbs_name, parent_obj=project)
        hbs_created = True
    if hbs_created:
        api.host_based_service_create(hbs)
    else:
        api.host_based_service_update(hbs)
