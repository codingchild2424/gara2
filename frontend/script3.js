
var totalScore;
var percent = 0;
var nextButton = document.getElementById('nextButton');
var regionScore = 0;

function add() {
    regionScore += 1;
}

function minus() {
    regionScore = regionScore - 1;
}

nextButton.addEventListener('click', function () {
    localStorage.setItem("regionScore", regionScore.value);
    console.log(regionScore);

    $('#progressBar').css('width', '0px');
    $('#progressBar').addClass('progress-bar-striped active');


    
    percent += 20;
    $('#progressBar').css('width', percent + '%');
    $('#progressBar').html(percent + '%');


    if (percent >= 100) {
        $('#progressBar').removeClass('progress-bar-striped active');
        $('#nextButton').css('display', 'none');
        $('#nextStage').css('display', 'inline');

    }
});


