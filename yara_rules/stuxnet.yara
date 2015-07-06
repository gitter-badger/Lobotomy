rule Stuxnet 
{
    meta:
        description = "Stuxnet"
        author = "Wim Venhuizen"
        last_modified = "2015-07-06"
    
    strings:
        $string1 = "mrx"
		$string2 = "HKEY_LOCAL_MACHINE?SYSTEM?CurrentControlSet?Services?MRxCls"
		$file1 = "mdmcpq3.PNF"
		$file2 = "mdmeric3.PNF"
		$file3 = "oem6C.PNF"
		$file4 = "oem7A.PNF"
		$file5 = "mrxnet.sys"
		$file6 = "mrxcls.sys"
		$file7 = "mrxsmb.sys"

        
    condition:
       any of ($string*) or all of ($file*)
}
