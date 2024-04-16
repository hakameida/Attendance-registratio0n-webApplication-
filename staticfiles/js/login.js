// create a popup with button 
let camButton=document.querySelector(".cam");
camButton.addEventListener("click",(e) =>{
    let overlay=document.createElement("div");
    overlay.className="popup-overlay";
    document.body.appendChild(overlay);

    let popupBox=document.createElement("div");
    popupBox.className="popup-box";

    let popupCam=document.createElement("video");
    popupCam.id="videoCam";
    let stratButton=document.createElement("button")
    stratButton.className="startBtn";
    let btnText=document.createTextNode("Open Camera");
    let closeBtn=document.createElement("span");
    let closeBtnTxt=document.createTextNode("X");
    closeBtn.className="close-button";

    closeBtn.appendChild(closeBtnTxt);
    popupBox.appendChild(popupCam);
    popupBox.appendChild(stratButton);
    stratButton.appendChild(btnText);
    popupBox.appendChild(closeBtn);
    document.body.appendChild(popupBox);
    

    //close camera
    document.addEventListener("click", function (e){
      if(e.target.className === "close-button"){
          //Remove the camera 
          e.target.parentNode.remove();
          //Remove overlay
          document.querySelector(".popup-overlay").remove(); 
         //  stopCam();
      }
  });

   
   document.addEventListener("click", function (e){
      if(e.target.className === "startBtn"){
         openCam();
      }
});
  
});





function openCam(){
   //access to available devices
   //navigator contains information about user and browser
   //mediaDevices for accessing to available devices as camera or microphone
    let All_mediaDevices=navigator.mediaDevices
    //check if usermedia not available
    if (!All_mediaDevices || !All_mediaDevices.getUserMedia) {
       console.log("getUserMedia() not supported.");
       return;//to get out of the function if there is no media
    }
    //calling getUserMedia with object as a parameter todetect that there is user media
    All_mediaDevices.getUserMedia({
       audio: true,
       video: true
    })
    .then(function(vidStream) {
      //get video item
       var video = document.getElementById('videoCam');
       //check if srcObject property available in video item
       if ("srcObject" in video) {
         //detect srcObject directly by vidStream => view live video in video item without need to create URL
          video.srcObject = vidStream;
       } else {
         //srcObject not exist => create temporary URL for vidStream and detect it as a value for src of video
         // to use it for loading video and audio flow from vidStream of video in the page 
          video.src = window.URL.createObjectURL(vidStream);
       }
       //if video metadata successfully loaded play the video
       video.onloadedmetadata = function(e) {
          video.play();
       };
    })
    //Error in getting media
    .catch(function(e) {
       console.log(e.name + ": " + e.message);
    });
 };

// async function stopCam(){
//    const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
//    const videoTrack = mediaStream.getVideoTracks()[0];
//    videoTrack.stop();
//  }