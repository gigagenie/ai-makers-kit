const record=require('node-record-lpcm16');
const mplayer=require('mplayer');
const ktkws=require('./ktkws');
const player=new mplayer();
const kwstext=['기가지니','지니야','친구야'];
const kwsflag=parseInt(process.argv[2]);
let pcm=null;
function initMic(){
        return record.start({
                sampleRateHertz: 16000,
                threshold: 0,
                verbose: false,
                recordProgram: 'arecord',
        })
};
process.env.LD_LIBRARY_PATH='./kwslib';
let res=ktkws.initialize('./kwslib/kwsmodel.pack');
console.log('Initialize:'+res);
res=ktkws.startKws(kwsflag);
console.log('startKws:'+res);
let mic=initMic();
mic.on('data',(data)=>{
	result=ktkws.pushBuffer(data);
	if(result===1) {
		console.log("KWS Detected");
		player.openFile('./sample_sound.wav');
	}
});
console.log('say :'+kwstext[kwsflag]);
