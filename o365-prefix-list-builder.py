#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests 
import xml.etree.ElementTree as ET


o365Services = {
	'MSFT-o365-v4':     ".//product/[@name='o365']/addresslist/[@type='IPv4']",
	'MSFT-o365-v6':     ".//product/[@name='o365']/addresslist/[@type='IPv6']",	
	'MSFT-LYO-v4':      ".//product/[@name='LYO']/addresslist/[@type='IPv4']",
	'MSFT-LYO-v6':      ".//product/[@name='LYO']/addresslist/[@type='IPv6']",
	'MSFT-Planner-v4':  ".//product/[@name='Planner']/addresslist/[@type='IPv4']",
	'MSFT-Planner-v6':  ".//product/[@name='Planner']/addresslist/[@type='IPv6']",
	'MSFT-Teams-v4':    ".//product/[@name='Teams']/addresslist/[@type='IPv4']",
	'MSFT-Teams-v6':    ".//product/[@name='Teams']/addresslist/[@type='IPv6']",
	'MSFT-Identity-v4': ".//product/[@name='Identity']/addresslist/[@type='IPv4']",
	'MSFT-Identity-v6': ".//product/[@name='Identity']/addresslist/[@type='IPv6']",
	'MSFT-OneNote-v4':  ".//product/[@name='OneNote']/addresslist/[@type='IPv4']",
	'MSFT-OneNote-v6':  ".//product/[@name='OneNote']/addresslist/[@type='IPv6']",
	'MSFT-Yammer-v4':   ".//product/[@name='Yammer']/addresslist/[@type='IPv4']",
	'MSFT-Yammer-v6':   ".//product/[@name='Yammer']/addresslist/[@type='IPv6']",
}


r = requests.get('https://support.content.office.net/en-us/static/O365IPAddresses.xml')
root = ET.fromstring(r.text)


def getPrefixes(match):
	if not root.findall(match):
		return None
	else:
		for node in root.findall(match):
			data = []
			for d in node.getchildren():
				if d.text:
					data.append(d.text)
			return data


def junosPrefixListSet(service, prefixes):
	for prefix in prefixes:
		config = "set prefix-list {} {}".format(service, prefix)
		return config


def junosPrefixListBracket(service, prefixes):
	config = "    prefix-list {} {{\n".format(service)
	for prefix in prefixes:
		config += "        {};\n".format(prefix)
	config += "    }\n"
	return config


def main():
	
    # This is before loop
	configBracket = "policy-options {\n"
	
	# Loop is starting
	for service, match in o365Services.items():
		prefixes = getPrefixes(match)
		if prefixes:
			configSet      = junosPrefixListSet(service, prefixes)
			configBracket += junosPrefixListBracket(service, prefixes)
	
	# The loop has completed. 
	configBracket += "}"
	print configBracket


if __name__ == '__main__':
    main()
