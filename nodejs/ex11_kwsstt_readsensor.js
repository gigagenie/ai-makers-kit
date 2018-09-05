const record=require('node-record-lpcm16');
const aikit=require('./aimakerskitutil');
const nodeVersion=process.version.split('.')[0];

//for sensing program
const { spawn } = require('child_process');

let ktkws=null;
if(nodeVersion==='v6') ktkws=require('./ktkws');
else if(nodeVersion==='v8') ktkws=require('./ktkws_v8');

//for playing pcm sound
const Speaker=require('speaker');
const fs=require('fs');
const soundBuffer=fs.readFileSync('../data/sample_sound.wav');
const pcmplay=new Speaker({
	channels:1,
	bitDepth:16,
	sampleRate:16000
});

const client_id='';
const client_key='';
const client_secret='';
const json_path='./clientKey.json';
const cert_path='../data/ca-bundle.pem';
const proto_path='../data/gigagenieRPC.proto';

const kwstext=['기가지니','지니야','친구야','자기야'];
const kwsflag=parseInt(process.argv[2]);

function initMic(){
        return record.start({
                sampleRateHertz: 16000,
                threshold: 0,
                verbose: false,
                recordProgram: 'arecord',
        })
};
ktkws.initialize('../data/kwsmodel.pack');
ktkws.startKws(kwsflag);
let mic=initMic();

//aikit.initialize(client_id,client_key,client_secret,cert_path,proto_path);
aikit.initializeJson(json_path,cert_path,proto_path);

let mode=0;//0:kws, 1:stt
let ktstt=null;
mic.on('data',(data)=>{
	if(mode===0){
		result=ktkws.pushBuffer(data);
		if(result===1) {
			console.log("KWS Detected");
			pcmplay.write(soundBuffer);
			setTimeout(startStt,500);
		}
	} else {
    		ktstt.write({audioContent:data});
	}
});
console.log('say :'+kwstext[kwsflag]);
function startStt(){
	ktstt=aikit.getVoice2Text();
	ktstt.on('error',(error)=>{
	    console.log('Error:'+error);
	});
	ktstt.on('data',(data)=>{
		console.log('stt result:'+JSON.stringify(data));
		if(data.resultCd!==200) {
			//added code
			if(data.resultCd===201){
				if(data.recognizedText.includes('온도') && data.recognizedText.includes('알려줘')){
					readAIMKSEN001((rc,temp,humid)=>{
						let ttsComment="센서가 정상 동작하지 않았습니다.";
						if(rc===200){
							ttsComment='방안의 온도는 '+temp+'이고 습도는 '+humid+' 페센트 입니다.';
						} 
						let kttts=aikit.getText2VoiceStream({text:ttsComment,lang:0,mode:0});
						kttts.on('error',(error)=>{
							console.log('TTS Error:'+error);
						});
						kttts.on('data',(data)=>{
							pcmplay.write(data.audioContent);
						});
					});
				};
			};
			//added code
			mode=0;
		}
	});
	ktstt.on('end',()=>{
		console.log('stt text stream end');
		mode=0;
	});
	ktstt.write({reqOptions:{mode:0,lang:0}});
	mode=1;
};

//for reading sensor
function readAIMKSEN001(callback){
	const prg = spawn('./am2301');
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
