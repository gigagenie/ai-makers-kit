/********************************************
> Title: AIMK 유튜브 음악 다운로드 재생기
> 필수 설치 패키지

아래 명령어를 통해 mplayer, youtube-dl 필수 설치 요망.
sudo npm install mplayer
sudo npm install youtube-dl

*********************************************/

const request = require('request');
const youtubedl=require('youtube-dl');
const fs = require('fs');
const MPlayer = require('mplayer');
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

function music_player(file_name){
	return new Promise((resolve,reject)=>{
		let audio_player = new MPlayer();
		audio_player.openFile(file_name);
		audio_player.play()
		resolve('Music Play Start...');
	});		
};


function dl_yt(target_Url, file_name){
	return new Promise((resolve,reject)=>{
		let video = youtubedl(target_Url,
	  	// Optional arguments passed to youtube-dl.
	  	['--format=18'],
	  	// Additional options can be given for calling `child_process.execFile()`.
	  	{ cwd: __dirname });
 		// Will be called when the download starts.
		video.on('info', function(info) {
		  console.log('Download started');
		  console.log('filename: ' + info.filename);
		  console.log('size: ' + info.size);
		  console.log('\n\nNow Playing.... \n');
		  let result = music_player(file_name);
		});
		video.pipe(fs.createWriteStream(file_name));
		resolve('dl_yt resolved');
	});
};

const youtubePlayBaseUrl='https://www.youtube.com/watch?';
async function playYoutubeByText(inQuery){
	let urls=await getYoutubeSearchList(inQuery);
	let targetUrl=youtubePlayBaseUrl+urls[0];
	console.log('yt url:'+targetUrl);
	
	let filename='yt_stream.mp4'
	
	let ret_result = await dl_yt(targetUrl, filename);
	console.log(ret_result)
};

playYoutubeByText('Left Right Left');
