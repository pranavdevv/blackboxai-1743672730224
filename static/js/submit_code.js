function setupFormSubmission() {
    var form = document.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        var formData = new FormData(form);
        var submitButton = form.querySelector('button[type="submit"]');
        var resultContainer = document.getElementById('result-container');
        var resultContent = document.getElementById('result-content');
        
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Submitting...';
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action);
        xhr.onload = function() {
            resultContainer.classList.remove('hidden');
            try {
                var result = JSON.parse(xhr.responseText);
                if (result.success) {
                    resultContainer.className = 'mt-4 p-3 bg-green-100 text-green-800 rounded';
                    resultContent.innerHTML = 
                        '<p><strong>Status:</strong> Success!</p>' +
                        '<p><strong>Execution Time:</strong> ' + result.execution_time.toFixed(2) + ' ms</p>' +
                        '<p><strong>Memory Usage:</strong> ' + (result.memory_usage / 1024 / 1024).toFixed(2) + ' MB</p>';
                } else {
                    resultContainer.className = 'mt-4 p-3 bg-red-100 text-red-800 rounded';
                    var errorContent = 
                        '<p><strong>Status:</strong> Error</p>' +
                        '<p><strong>Message:</strong> ' + result.error + '</p>';
                    if (result.output) {
                        errorContent += '<pre class="mt-2">' + result.output + '</pre>';
                    }
                    resultContent.innerHTML = errorContent;
                }
            } catch (e) {
                resultContainer.className = 'mt-4 p-3 bg-red-100 text-red-800 rounded';
                resultContent.innerHTML = '<p><strong>Error:</strong> Failed to parse response</p>';
            }
            submitButton.disabled = false;
            submitButton.innerHTML = '<i class="fas fa-paper-plane mr-2"></i>Submit';
        };
        xhr.onerror = function() {
            resultContainer.classList.remove('hidden');
            resultContainer.className = 'mt-4 p-3 bg-red-100 text-red-800 rounded';
            resultContent.innerHTML = '<p><strong>Error:</strong> Failed to submit code</p>';
            submitButton.disabled = false;
            submitButton.innerHTML = '<i class="fas fa-paper-plane mr-2"></i>Submit';
        };
        xhr.send(formData);
    });
}

// Timer functionality
function setupTimer(initialTime) {
    var timeLeft = initialTime;
    var timerElement = document.getElementById('timer');
    
    function updateTimer() {
        var minutes = Math.floor(timeLeft / 60);
        var seconds = timeLeft % 60;
        timerElement.textContent = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert('Time for this question has expired!');
        } else {
            timeLeft--;
        }
    }
    
    var timerInterval = setInterval(updateTimer, 1000);
    updateTimer();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupFormSubmission();
    var timeLimit = document.getElementById('timer').textContent.split(':')[0] * 60;
    setupTimer(timeLimit);
});