

# Versa CLI
- By default, exporter is adding a global prefix `vsg_` for all metrics keys
- all `-` or `SPACE/SPACES` in the versa metrics key is replaced wtih `_` (underscore) as prometheus will not accept it
## `show dhcp statistics global`

| Stats Name | Description |
|:------------|:-----------|
| `intf-match-fail-cnt` | No routing instance found for this or Tenant ID could not be identified |
| `unknown-type-cnt`    | dhcpd packet could not be parsed successfully |
| `intf-ignore-cnt` | dhcpd packet ignore on unsupported interface |
| `dhcp6-intf-match-fail-cnt` | No routing instance found for this or Tenant ID could not be identified | 
| `dhcp6-unknown-type-cnt` | dhcpd packet could not be parsed successfully |
| `dhcp6-intf-ignore-cnt` | dhcpd packet ignore on unsupported interface |
| `snoop-ack-packets` | DHCP snoop ack packets received | 
| `snoop-ack-packets-success` | Successful snoop; All the fields are parsed successfully and send to other processes for subscriber update | 
| `snoop-relay-ip-missing-cnt` | IPv4 relay IP missing, it generally gets incremented for unicast acks, this alone does not lead to ignoring of packet |
| `snoop-opt-82-agent-info-missing` | self-explanatory |
| `snoop-opt-82-subopt-2-rmt-id-info-missing` | self-explanatory |
| `snoop-opt-32-subopt-51-lease-info-missing` | self-explanatory |
| `dhcp6-snoop-ack-packets` | DHCPv6 snoop ack packets received |
| `dhcp6-snoop-ack-packets-success` | Successful v6 snoop. i.e. all the fields are parsed successfully and send to other processes for subscriber update |
| `dhcp6-snoop-relay-ip-missing-cnt` | IPv6 relay IP missing |
| `dhcp6-snoop-opt-1-client-id-missing` | self-explanatory |
| `dhcp6-snoop-opt-3-ia-na-info-missing` | self-explanatory |
| `dhcp6-snoop-opt-3-subopt-5-ia-na-missing` | self-explanatory |
| `dhcp6-snoop-opt-25-subopt-26-ia-pd-missing` | self-explanatory |
| `dhcp6-snoop-opt-17-vendor-info-missing` | self-explanatory |
| `dhcp6-snoop-opt-17-subopt-1026-cm-mac-addr-missing` | self-explanatory |
| `dhcp6-snoop-error-detecting-device-type` | Need more information [Kuldeep: In case of dhcpv6, for cm and mta, the inner vendor specific |information would be present, if it is present, then boot file option also should be present, if boot file option 33 is missing this is incremented and packet will be ignored. In case of CPE, the inner vendor specific option won’t be present, and that is how we consider that as CPE device type |
| `snoop-renew-ack-packets` | self-explanatory |
| `snoop-device-mac-missing` | Device MAC field has invalid MAC address or NULL. From the trial sample lab packets, we found that this will be NULL string in case of Ack response for Lease Active Query, this will lead to dhcp packet ignore |
| `dhcp6-snoop-device-mac-missing` | Device MAC field has invalid MAC address or NULL, thus will lead to dhcp packet ignore |

## `show orgs org-services comcast tdf statistics`

| Stats Name | Description |
|:------------|:-----------|
| `num-sub-update-from-dhcp` | Number of subscriber updates recieved from dhcp server side in fast path and mirrored to dhcp service |
| `num-sub-update-from-submgr` | Number of subscriber updates recieved from Submgr |
| `num-sub-update-from-test` | Number of subscriber updates recieved from Submgr test commands |
| `num-sub-delete-from-submgr` | Number of subscriber deletes recieved from Submgr |
| `num-sub-delete-from-test` | Number of subscriber deletes recieved from Submgr test commands|
| `unknown-sub-flow-cnt` | Number of subscriber unknown flow |
| `dhcp-failed-to-mirror-cnt` | dhcp packet received from external side or from dhcp server side in fast path and failed to mirror to dhcp service for snooping |
| `dhcpv4-mirror-cnt` | dhcp packet received from external side or from dhcp server side in fast path and mirrored to dhcp service for snooping, it is not necessarily only ACK packet | 
| `dhcpv6-mirror-cnt` | dhcp packet received from external side or from dhcp server side in fast path and mirrored to dhcp service for snooping, it is not necessarily only ACK packet |

## `show alarms statistics brief`

| Stats Name | Description |
|:------------|:-----------|
| | |

## `show orgs org-services comcast tdf vsg statistics`

| Stats Name | Description |
|:------------|:-----------|
| | |

## `show orgs org-services comcast lef statistics`

| Stats Name | Description |
|:------------|:-----------|
| | |


## `show orgs org comcast sessions summary`

| Stats Name | Description |
|:------------|:-----------|
| | |

## `show interfaces statistics`

- In addition to the global prefix `vsg_`, `interface_` prefix is added to the metrics collected.

| Stats Name | Description |
|:------------|:-----------|
| | |

# Versa VSM debug cli

## `show vsm statistics thrm  detail`
- In addition to the global prefix `vsg_`, `vnf_` prefix is added to the metrics collected

| Stats Name | Description |
|:------------|:-----------|
| | |