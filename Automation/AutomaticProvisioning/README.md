# Automatic Network Provisoner

## Objective

Use Ansible to assign IP addresses to point-to-point interfaces, configure loopback interfaces, and advertise the correct (non-management) networks into OSPF.

## Key Technologies

- Ansible

## Relevant Scripts

`hosts.yml` is an Ansible hosts file that defines the routers to configure.

`links.yml` contains interface information pertaining to the point-to-point links between routers.

`ip_provisioning.yml` is an Ansible playbook that automatically assigns IP addresses to routers based on the `links.yml` file.  

`configure_ospf.yml` is an Ansible playbook that configures OSPF and verifies that neighborships have formed by printing the output of `show ip ospf neighbor` to the console.

`create_loopbacks.yml` is an Ansible playbook that creates loopback interfaces on all devices with the addressing scheme: `"ip address 10.255.router_id.router_id 255.255.255.255"`.  The loopback interfaces are then advertised into OSPF.

`write_mem.yml` is an Ansible playbook that saves the running-config.

## Verification

What commands are used to ensure everything is working

## Conclusion

Takeaways from completing this lab
