// WinDbg JavaScript sample
// Shows how to call a debugger command and display results
"use strict";

function RunCommands()
{
	var output;
var ctl = host.namespace.Debugger.Utility.Control;   
// Esegue coomando lm
try{
	output = ctl.ExecuteCommand("lm");
}catch(e){
	host.diagnostics.debugLog("Errore durante l'esecuzione del comando: " + e +"\n");
}
host.diagnostics.debugLog("***> Displaying command output \n");
// estrapola la prima riga, il sample
//var line = output[1]
var longest_line = "a";
var i = 0;
var line = output[0];
var longest_line_name="";
while(line != null && i < 200){
    try{
        line = output[i];
        let result_array = line.split(' ');
        let result_array_split = result_array.slice(0, 5);
        var name = result_array[4];
        //host.diagnostics.debugLog("Intermediate line length: ", name, "\n");
        if(name.length >= longest_line_name.length){
            longest_line=line;
            longest_line_name = name;
        }
        if(name.includes("softonic") || name.includes("Windows") || name.includes("windows"))
        {
            longest_line=line;
            longest_line_name=name;
            i=201;
        }
    }catch(error){
        i = 201;
    }
    
    i=i+1;  
}

host.diagnostics.debugLog("Chosen line: ", longest_line, "\n");
line = longest_line;
// suddivide la prima riga in parole
let result_array = line.split(' ');

// Seleziona le prime tre parole utilizzando l'indice 0, 1 e 4 visto che c'è uno spazio grande al centro
let result_array_split = result_array.slice(0, 5);

var start = "0x"+result_array[0];
var finish = "0x"+result_array[1];
var name = result_array[4];
//imposta le 3 variabili
host.diagnostics.debugLog("  start: ", start, "\n");
host.diagnostics.debugLog("  finish: ", finish, "\n");
host.diagnostics.debugLog("  name: ", name, "\n");

//usa le variabili per chiamare comando "u" con valori custom
var command = "u "+start.toString()+" "+finish.toString();
var command_result
try{
	command_result = ctl.ExecuteCommand(".logopen /t D:\\scritturaTesiMagistrale\\dump\\text\\dump_"+name+".txt");
}catch(e){
	host.diagnostics.debugLog("Errore durante l'esecuzione del comando: " + e +"\n");
}

for (let i = parseInt(start, 16); i < parseInt(finish, 16)-0x1; i+=0x2) {
    command = "u "+i.toString(16)+" "+(i+0x1).toString(16);
    //host.diagnostics.debugLog("Comando: ", command.toString(), "\n");
    try {
        command_result = ctl.ExecuteCommand(command.toString());
    } catch (e) {
    // Visualizza l'errore
        host.diagnostics.debugLog("Errore durante l'esecuzione del comando: " + e +"\n");
        for (var prop in e) {
            host.diagnostics.debugLog(prop + ": " + e[prop] + "\n");
        }
    }
    for(var stringa of command_result){
        if (stringa != command_result[0]){
            host.diagnostics.debugLog(stringa, "\n");
        }
    }
}


for(var stringa of command_result){
        if (stringa != command_result[0]){
            host.diagnostics.debugLog(stringa, "\n");
        }
    }
command_result = ctl.ExecuteCommand(".logclose");
command_result = ctl.ExecuteCommand("qd");

host.diagnostics.debugLog("***> Exiting RunCommands Function \n");

}