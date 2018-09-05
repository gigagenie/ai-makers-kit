const { spawn } = require('child_process');
function readAIMKSEN001(callback){
	const prg= spawn('./am2301');
	let returnTemp;
	let returnHumid;
	let returnCode=200;
	prg.stdout.on('data', (data) => {
		returnStr=data.toString();
		let dataSplit=returnStr.split('\n');
		returnTemp=dataSplit[0].split('=')[1];
		returnHumid=dataSplit[1].split('=')[1];
	});
	prg.stderr.on('data', (data) => {
		returnCode=500;
	});
	prg.on('close', (code) => {
		callback(returnCode,returnTemp,returnHumid);
	});
};
readAIMKSEN001((rc,temp,humid)=>{
	console.log('Result:'+rc+', Temperature:'+temp+', humidity:'+humid);
});
