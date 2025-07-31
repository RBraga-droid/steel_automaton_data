@echo off
set "sourceFolder=D:\scritturaTesiMagistrale\sample_for_input"
set "destinationFolder=D:\scritturaTesiMagistrale\VM\MalwareAnalysis\shared\samples"
set "vmName=MalwareAnalysis"
set "snapshotName=PROCDUMP_AUTOMATIC_INIT"
set "startupTimeout=50"  
rem Itera attraverso ogni file nella cartella di origine



set "nuovaEstensione=.7z"

for %%f in ("%sourceFolder%\*") do (

	ren "%%f" "%%~nf%nuovaEstensione%"

)

for %%i in ("%sourceFolder%\*") do (
	rem Ripristina lo snapshot
	del /q "%destinationFolder%\*.*"
	echo %time%: Restoring...
	C:\Programmi\Oracle\VirtualBox\VBoxManage snapshot %vmName% restore %snapshotName%
	timeout /t 10 >nul
	rem Accensione macchina
	C:\Programmi\Oracle\VirtualBox\VBoxManage startvm "%vmName%" 
	rem Attendi che la macchina virtuale sia operativa
	echo %time%: Waiting the complete bootstrap...
    timeout /t 60 >nul
	
	rem Esegui le operazioni necessarie (sostituisci con i tuoi comandi)
	echo %time%: Working the VM while dumping...
	rem Copia il file nella cartella di destinazione
    copy "%%i" "%destinationFolder%"
	start C:\Programmi\Oracle\VirtualBox\VBoxManage guestcontrol %vmName% run --username student --password reverse --exe C:\Users\student\AppData\Local\Programs\Python\Python311\python.exe C:\Users\student\Desktop\automated_dump.py 
	
	rem C:\Programmi\Oracle\VirtualBox\VBoxManage.exe guestcontrol MalwareAnalysis run --username student --password reverse --exe C:\Users\student\AppData\Local\Programs\Python\Python311\python.exe -- python.exe C:\Users\student\Desktop\automated_dump.py
	
	rem :attendi_file
	rem if exist "%destinationFolder%\*.*" (
	rem	echo Il file e' presente in %destinationFolder%. Attendo...
	rem 	ping -n 6 127.0.0.1 > nul  :: Attendi 5 secondi (puoi modificare il numero di secondi a tuo piacimento)
	rem	goto attendi_file
	rem )
	rem echo Il file %destinationFolder%\%i% non e' presente. Proseguo...

	rem Attendi un po' prima di procedere con lo spegnimento
	timeout /t %startupTimeout% >nul
	echo %time%: Dump complete...

	rem C:\Programmi\Oracle\VirtualBox\VBoxManage guestcontrol %vmName% run --username student --password reverse --exe C:\\Windows\\System32\\Taskmgr.exe -- "taskkill /IM python.exe"
	echo %time%: Powering off...
	rem Esegui lo spegnimento della macchina virtuale
	
    C:\Programmi\Oracle\VirtualBox\VBoxManage controlvm "%vmName%" poweroff
	timeout /t 10 >nul
	rem taskkill /F /FI "WINDOWTITLE eq cmd /c *Virtual*"
	taskkill /F /IM VBoxSDS.exe
	taskkill /F /IM VBoxSVC.exe
	taskkill /F /IM VBoxManage.exe
	taskkill /F /IM VirtualBoxVM.exe
    rem Attendi finché la macchina virtuale non è spenta (controlla ogni 5 secondi)
	echo %time%: Waiting the complete shutdown...
	
    timeout /t 5 >nul
)

echo Operazione completata.




    

