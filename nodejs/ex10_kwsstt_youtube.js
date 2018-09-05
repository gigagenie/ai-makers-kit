const record=require('node-record-lpcm16');
const aikit=require('./aimakerskitutil');
const nodeVersion=process.version.split('.')[0];
const fs=require('fs');

let ktkws=null;
if(nodeVersion==='v6') ktkws=require('./ktkws');
else if(nodeVersion==='v8') ktkws=require('./ktkws_v8');

const request = require('request');
const youtubedl=require('youtube-dl');
const Cvlc=require('cvlc');
let player=new Cvlc();

const client_id='';
const client_key='';
const client_secret='';
const json_path='';
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
			player.play("../data/sample_sound.wav",()=>{
				console.log('sample sound played');
			});
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
			if(data.resultCd===201){
				if((data.recognizedText.includes('노래')) && 
					(data.recognizedText.includes('틀어줘') || data.recognizedText.includes('들려줘'))){
					let target=data.recognizedText.split('노래')[0];
					console.log('Play Target:'+target);
					const ttsComment='유튜부의 '+target+' 노래를 플레이합니다';
					let kttts=aikit.getText2VoiceStream({text:ttsComment,lang:0,mode:0});
					kttts.on('error',(error)=>{
						console.log('TTS Error:'+error);
					});
					kttts.on('data',(data)=>{
						fs.writeFileSync('./tts.wav',data.audioContent);
						player.play('./tts.wav',()=>{
							console.log('media played');
						});
					});
					playYoutubeByText(target);
				};
			};
			mode=0;
		};
	});
	ktstt.on('end',()=>{
		console.log('stt text stream end');
		mode=0;
	});
	ktstt.write({reqOptions:{mode:0,lang:0}});
	mode=1;
};

//Youtube Search & Play Related Code
const yturl= 'https://www.youtube.com/watch?v=NwhCsMepR3U';
const ytoptions=['--format=250'];
function getYoutubeSearchList(inQuery){
	const queryText=inQuery;
	return new Promise((resolve,reject)=>{
		console.log('QueryText:'+queryText);
		const searchurl='https://www.youtube.com/results?search_query=';
		const queryUrl=encodeURI(searchurl+queryText);
		request(queryUrl,(err,res,body)=>{
			let splitByWatch=body.split('href=\"\/watch?');
			let isFirst=true;
			let urlList=[];
			splitByWatch.forEach((splitText)=>{
				if(isFirst===true) isFirst=false;
				else {
					let splitByQuot=splitText.split('"');
					urlList.push(splitByQuot[0]);
				}
			});
			resolve(urlList);
		});
	});
};
function getPlayRealUrl(inUrl){
	const url=inUrl;
	return new Promise((resolve,reject)=>{
		youtubedl.getInfo(url,ytoptions,function(err,info){
			console.log('title:'+info.title);
			console.log('url:'+info.url);
			resolve({title:info.title,url:info.url});
		});
	});
};
const youtubePlayBaseUrl='https://www.youtube.com/watch?';
async function playYoutubeByText(inQuery){
	let urls=await getYoutubeSearchList(inQuery);
	let targetUrl=youtubePlayBaseUrl+urls[0];
	console.log('yt url:'+targetUrl);
	let realPlayUrl=await getPlayRealUrl(targetUrl);
	console.log('title:'+realPlayUrl.title+' url:'+realPlayUrl.url);

	player.cmd('stop');
	player.file_path='';
	player.play(realPlayUrl.url,()=>{
		console.log('Music Played');
	});
};
