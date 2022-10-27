from executeCmd import execute_cmd

IPFS_FILES_PATH = "~/IPFS/files/"

def add_data_ipfs(filename):
    """
    receives the filename in e.g: ~/mypath/add.txt
    return new content identifier
    """

    #convert input to string
    filename = str(filename)

    cmd = "cp " + filename + " " + IPFS_FILES_PATH
    execute_cmd(cmd)

    #add filename to ipfs and send hash to temporary file
    cmd = "ipfs-cluster-ctl add " + filename
    cmd_return = execute_cmd(cmd)

    #ipfs-cluster-ctl add return format -> added hash1010101 txt.txt
    list_cmd_return = cmd_return.split()
    ipfs_hash = list_cmd_return[1]

    cmd = "ipfs get " + ipfs_hash 
    execute_cmd(cmd)

    cmd = "mv " + ipfs_hash + " " + IPFS_FILES_PATH
    execute_cmd(cmd)

    filename = filename.split("/")
    cmd = "rm " + IPFS_FILES_PATH + filename[-1]
    execute_cmd(cmd)

    return ipfs_hash

def delete_data_ipfs(cid):
    """
    receives the content identifier of the data to be deleted
    """

    #convert input to string
    cid = str(cid)

    #unpin filename from ipfs and run garbage collector to delete from cluster
    cmd = "ipfs-cluster-ctl pin rm " + cid 
    execute_cmd(cmd)

    cmd = "ipfs-cluster-ctl ipfs gc"
    execute_cmd(cmd)
    
    cmd = "rm " + IPFS_FILES_PATH + cid
    execute_cmd(cmd)

    return True

def get_data_ipfs(cid):
    """
    send ipfs content identifier
    return content path
    """

    #convert input to string
    cid = str(cid)

    #get data from ipfs
    cmd = "ipfs get " + cid
    execute_cmd(cmd)

    cmd = "mv " + cid + " " + IPFS_FILES_PATH
    execute_cmd(cmd)

    return IPFS_FILES_PATH + cid