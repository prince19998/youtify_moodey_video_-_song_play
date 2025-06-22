document.addEventListener('DOMContentLoaded', function() {
    // Player controls
    const playButton = document.querySelector('.controls button:nth-child(2)');
    const progressBar = document.getElementById('progress-bar');
    let isPlaying = false;
    
    playButton.addEventListener('click', function() {
        isPlaying = !isPlaying;
        playButton.innerHTML = isPlaying ? '<i class="fas fa-pause"></i>' : '<i class="fas fa-play"></i>';
    });
    
    // Update progress bar (mock functionality)
    setInterval(function() {
        if (isPlaying) {
            const currentValue = parseInt(progressBar.value);
            if (currentValue < 100) {
                progressBar.value = currentValue + 1;
                updateTimeDisplay();
            } else {
                isPlaying = false;
                playButton.innerHTML = '<i class="fas fa-play"></i>';
            }
        }
    }, 1000);
    
    function updateTimeDisplay() {
        const progress = parseInt(progressBar.value);
        const totalSeconds = 180; // 3 minutes
        const currentSeconds = Math.floor(totalSeconds * progress / 100);
        
        const minutes = Math.floor(currentSeconds / 60);
        const seconds = currentSeconds % 60;
        
        const timeDisplays = document.querySelectorAll('.progress .time');
        timeDisplays[0].textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        timeDisplays[1].textContent = `3:00`;
    }
    
    // Video click handler
    document.querySelectorAll('.video-card, .video-item').forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') return;
            
            const link = this.querySelector('a');
            if (link) {
                window.location.href = link.href;
            }
        });
    });
    
    // Update now playing info when a video is played
    if (window.location.pathname.startsWith('/watch')) {
        const videoTitle = document.querySelector('.video-info h1').textContent;
        const videoChannel = document.querySelector('.video-info .channel').textContent;
        const videoThumbnail = document.querySelector('.player-container iframe')
            .src.match(/embed\/([^?]+)/)[1];
        
        document.getElementById('now-playing-title').textContent = videoTitle;
        document.getElementById('now-playing-artist').textContent = videoChannel;
        document.getElementById('now-playing-thumb').src = `https://img.youtube.com/vi/${videoThumbnail}/default.jpg`;
    }
});