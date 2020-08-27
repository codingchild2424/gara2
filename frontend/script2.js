var totalScore;
var percent = 0;
var nextButton = document.getElementById('nextButton');
var regionScore = 0;
var t1 = false;
var t2 = false;


$('#nextStage').css('display', 'none');
$('#progressBar').css('width', '0px');
function add() {
    t1 = true;
    regionScore += 1;
}

function minus() {
    t2 = true;
    regionScore = regionScore - 1;
}

nextButton.addEventListener('click', function () {
    localStorage.setItem("regionScore", regionScore.value);
    console.log(regionScore);

    $('#progressBar').addClass('progress-bar-striped active');

    if ((t1 == true) || (t2 == true)) {
        t1 = false;
        t2 = false;
        percent += 20;
        $('#progressBar').css('width', percent + '%');
        $('#progressBar').html(percent + '%');


        if (percent >= 100) {
            $('#progressBar').removeClass('progress-bar-striped active');
            $('#nextButton').css('display', 'none');
            $('#nextStage').css('display', 'inline');
            $('#nextStage').addClass('active');
        }

    } else {
        alert("한 쪽을 선택해주세요.");
    }

})
