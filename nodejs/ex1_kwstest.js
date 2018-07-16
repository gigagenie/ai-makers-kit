const record=require('node-record-lpcm16');
const kwstext=['기가지니','지니야','친구야','자기야'];
const Speaker=require('speaker');
const fs=require('fs');

//node version check
const nodeVersion=process.version.split('.')[0];
let ktkws=null;
if(nodeVersion==='v6') ktkws=require('./ktkws');
else if(nodeVersion==='v8') ktkws=require('./ktkws_v8');

//for play sample sound
const soundBuffer=fs.readFileSync('../data/sample_sound.wav');
const pcmplay=new Speaker({
	channels:1,
	bitDepth:16,
	sampleRate:16000
});


//for setting kws type
const kwsflag=parseInt(process.argv[2]);
let res=ktkws.initialize('../data/kwsmodel.pack');
console.log('Initialize KWS:'+res);

res=ktkws.startKws(kwsflag);

console.log('start KWS:'+res);

//for getting microphone input
function initMic(){
        return record.start({
                sampleRateHertz: 16000,
                threshold: 0,
                verbose: false,
                recordProgram: 'arecord',
        })
};
let mic=initMic();
mic.on('data',(data)=>{
	//push pcm data to ktkws library
	result=ktkws.pushBuffer(data);
	if(result===1) {
		console.log("KWS Detected");
		//play sample sound
		pcmplay.write(soundBuffer);
	}
});
console.log('say :'+kwstext[kwsflag]);
