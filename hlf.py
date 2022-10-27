import ipfs
from executeCmd import execute_cmd

IPFS_FILES_PATH = "~/IPFS/files/"
HLF_PATH = "~/HLF/fabric/bin/"

def add_data_hlf(id, filename):
    """
    receives the unique ID and the filename with path e.g: ~/add.txt
    return 
    """
    cid = ipfs.add_data_ipfs(filename)
    cmd = HLF_PATH + "peer chaincode invoke -o atlas.omega.olympus.pt:7050 --tls --cafile ~/HLF/organizations/ordererOrganizations/omega.olympus.pt/msp/tlscacerts/ca-omega-olympus-pt-7054.pem -C main-channel -n occv3 -c '{\"Args\":[\"CreateAsset\",\"" + str(id) + "\",\"" + str(cid) + "\"]}'"
    response = execute_cmd(cmd)
    if "status:200" in response:
        return True
    else:
        return False

def delete_data_hlf(id):
    """
    receives the id
    """
    cmd = HLF_PATH + "peer chaincode invoke -o atlas.omega.olympus.pt:7050 --tls --cafile ~/HLF/organizations/ordererOrganizations/omega.olympus.pt/msp/tlscacerts/ca-omega-olympus-pt-7054.pem -C main-channel -n occv3 -c '{\"Args\":[\"ReadAsset\",\"" + str(id) + "\"]}'"
    response = execute_cmd(cmd)
    if "status:200" in response:
        lst_response = response.split("CID")
        response_cid = lst_response[-1]
        lst_response = response_cid.split("deleted")
        response_cid = lst_response[0]
        ipfs_cid = ""
        for char in response_cid:
            if char != "/" and char != "\"" and char != "\\" and char != ":" and char != ",":
                ipfs_cid = ipfs_cid + char

        if (ipfs.delete_data_ipfs(ipfs_cid) == True):
            pass
        else:
            return False
    else:
        return False

    cmd = HLF_PATH + "./peer chaincode invoke -o atlas.omega.olympus.pt:7050 --tls --cafile ~/HLF/organizations/ordererOrganizations/omega.olympus.pt/msp/tlscacerts/ca-omega-olympus-pt-7054.pem -C main-channel -n occv3 -c '{\"Args\":[\"DeleteAsset\",\"" + str(id) + "\"]}'"
    response = execute_cmd(cmd)
    if "status:200" in response:
        return True
    else:
        return False

def get_data_hlf(id):
    """
    receives the blockid
    return data_path stored in IPFS
    """
    cmd = HLF_PATH + "peer chaincode invoke -o atlas.omega.olympus.pt:7050 --tls --cafile ~/HLF/organizations/ordererOrganizations/omega.olympus.pt/msp/tlscacerts/ca-omega-olympus-pt-7054.pem -C main-channel -n occv3 -c '{\"Args\":[\"ReadAsset\",\"" + str(id) + "\"]}'"
    response = execute_cmd(cmd)
    if "status:200" in response:
        lst_response = response.split("CID")
        response_cid = lst_response[-1]
        lst_response = response_cid.split("deleted")
        response_cid = lst_response[0]
        ipfs_cid = ""
        for char in response_cid:
            if char != "/" and char != "\"" and char != "\\" and char != ":" and char != ",":
                ipfs_cid = ipfs_cid + char

        data_path = ipfs.get_data_ipfs(ipfs_cid)
    return data_path

def get_all_data_hlf():
    """
    returns path with all the data
    """    
    cmd = HLF_PATH + "peer chaincode invoke -o atlas.omega.olympus.pt:7050 --tls --cafile ~/HLF/organizations/ordererOrganizations/omega.olympus.pt/msp/tlscacerts/ca-omega-olympus-pt-7054.pem -C main-channel -n occv3 -c '{\"Args\":[\"GetAllAssets\"]}'"
    response = execute_cmd(cmd)
    if "status:200" in response and "payload" in response:
        lst_response = response.split("CID")
        lst_response = lst_response[1:]
        ipfs_cid = ""
        for response_cid in lst_response:
            lst_response = response_cid.split("deleted")
            response_cid = lst_response[0]
            for char in response_cid:
                if char != "/" and char != "\"" and char != "\\" and char != ":" and char != ",":
                    ipfs_cid = ipfs_cid + char
            ipfs.get_data_ipfs(ipfs_cid)
            ipfs_cid = ""
    return IPFS_FILES_PATH