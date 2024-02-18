    var landingVideo = document.getElementById('landingVideo');

    // Listen for the 'ended' event and restart the video
    landingVideo.addEventListener('ended', function () {
        this.currentTime = 0;
        this.play();
    });
