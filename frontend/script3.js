
var totalScore;
var percent = 0;
var nextButton = document.getElementById('nextButton');
var regionScore = 0;
var t1;
var t2;
var t3;

$('#nextStage').css('display', 'none');

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

    $('#firstAnswer').click(function () {
        t1 = true;

    })

    $('#secondAnswer').click(function () {
        t2 = true;
    })

    if ((t1 == true) || (t2 == true)) {
        
        percent += 20;
        $('#progressBar').css('width', percent + '%');
        $('#progressBar').html(percent + '%');


        if (percent >= 100) {
            $('#progressBar').removeClass('progress-bar-striped active');
            $('#nextButton').css('display', 'none');
            $('#nextStage').css('display', 'inline');
            $('#nextStage').addClass('active');

            t1, t2 = false;

        }

        button1
        document.getElementById("firstAnswer").innerHTML = button1;
        button2
        document.getElementById("button2").innerHTML = button2;

   
    } else {

        alert("한 쪽을 선택해주세요.");

            
        
    }
    
});


