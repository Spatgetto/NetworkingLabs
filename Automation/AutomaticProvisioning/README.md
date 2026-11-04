# Automatic Network Provisoner

## Objective

Use Ansible to assign IP addresses to point-to-point interfaces, configure loopback interfaces, and advertise the correct (non-management) networks into OSPF.

## Key Technologies

- Ansible

## Relevant Scripts

`hosts.yml` is an Ansible hosts file that defines the routers to configure.

`links.yml` contains interface information pertaining to the point-to-point links between routers.

`ip_provisioning.yml` is an Ansible playbook that automatically assigns IP addresses to routers based on the `links.yml` file.  

`configure_ospf.yml`

`create_loopbacks.yml`

## Verification

What commands are used to ensure everything is working

## Conclusion

Takeaways from completing this lab
